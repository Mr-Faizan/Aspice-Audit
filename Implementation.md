# Implementation Notes — ASPICE Audit Tool

> Reference material for the thesis writing phase. Each section maps to a thesis chapter or subsection.

---

## 1. System Overview

The system is a web-based tool that helps software teams assess their maturity against the **ASPICE (Automotive SPICE) standard**, specifically the six software engineering processes: **SWE.1 through SWE.6**.

Instead of presenting every team member with the same fixed set of questions, the tool uses a **learning algorithm** (called a Contextual Multi-Armed Bandit) to personalise and adapt the question sequence for each user. After answering a series of questions, the user receives a **weakness report** — a heatmap showing which ASPICE processes and capability levels are most at risk.

---

## 2. The CMAB Engine — Core Algorithm

This is the most important technical contribution of the thesis.

### 2.1 Why a Bandit Algorithm?

Traditional audit tools present the same question list to every user. This is inefficient because:
- A **software developer** and an **ASPICE assessor** have very different knowledge — the same question carries different diagnostic value for each.
- Some questions are only relevant if earlier answers suggest a weakness in that area.
- A short session (12 questions) should maximise the information gained, not waste questions on areas already clearly understood.

A **Multi-Armed Bandit (MAB)** is a reinforcement learning algorithm that solves the **exploration vs. exploitation trade-off**: it tries different questions (exploration) while also favouring questions that have proven informative (exploitation). The "contextual" variant (CMAB) additionally uses contextual features — such as user role and session progress — to make smarter decisions.

### 2.2 The LinUCB Algorithm

The specific algorithm used is **LinUCB** (Linear Upper Confidence Bound), which assumes that the expected reward of asking a question is a linear function of the context vector.

**Core formula:**

```
UCB_score(question) = θᵀ · x  +  α · √(xᵀ · A⁻¹ · x)
```

Where:
- `x` is the **context vector** (23-dimensional description of the current situation)
- `θ = A⁻¹ · b` is the **learned weight vector** for this question
- `A` is a 23×23 matrix (starts as identity, grows with each pull)
- `b` is a 23-dimensional vector (accumulates reward-weighted contexts)
- `α = 1.0` is the **exploration coefficient** (higher = more exploration)

The first term (`θᵀ · x`) is the **exploitation** component — how well this question is expected to perform based on past experience.

The second term (`α · √(xᵀ · A⁻¹ · x)`) is the **exploration bonus** — questions that have been asked less or in different contexts get a higher bonus, encouraging the system to gather new information.

Each question has its own `A` matrix and `b` vector. When a question has never been asked, `A` is initialised as the **identity matrix** and `b` as a **zero vector**. This means all unasked questions start with equal scores, and the exploration bonus dominates early on.

### 2.3 The Context Vector (23 dimensions)

Before selecting the next question, the system builds a numerical description of the current situation. This vector is what makes the algorithm "contextual" — it can learn that certain questions are more valuable for certain types of users at certain stages of the audit.

| Dimensions | Content | How computed |
|---|---|---|
| 0–6 | Stakeholder role (one-hot encoding) | 1.0 at the user's role position, 0 elsewhere |
| 7 | Session progress | `questions_asked / max_questions` (0.0 to 1.0) |
| 8–13 | Per-process coverage flags (SWE1–SWE6) | 1.0 if at least one question from that process was already asked |
| 14–16 | Per-level coverage flags (L1, L2, L3) | 1.0 if at least one question at that level was already asked |
| 17–22 | Running mean weakness score per process | Average of normalised answer weights for each process so far |

**Why one-hot encoding for role?**
The algorithm works with numbers, not categories. One-hot encoding creates a separate dimension for each role, so the learned weights can be independently strong or weak for each role without implying any ordering between them (e.g., it does not assume an assessor is "more than" a developer in any numerical sense).

**Why include session progress?**
Questions about process management (L2/L3 capability) are more informative later in the session, once L1 questions have already revealed the baseline capability. Including progress allows the algorithm to learn this timing naturally.

**Why include running weakness scores?**
If a user gives high-risk answers on SWE.1, the algorithm should prioritise more SWE.1 questions to confirm the pattern. Including per-process weakness scores in the context allows the bandit to develop this adaptive behaviour.

### 2.4 The Reward Signal

After a user answers a question, the system computes a **reward** between 0.0 and 1.0:

```
reward = (option.weight / 4.0)  +  coverage_bonus
reward = clamp(reward, 0.0, 1.0)
```

- **Base reward** (`weight / 4.0`): A high-risk answer (weight 4) gives reward 1.0. A best-practice answer (weight 0) gives reward 0.0. The rationale is that high-risk answers are most informative — they confirm that a real weakness exists and warrant follow-up.
- **Coverage bonus** (`+0.2`): If the answered question is the **first question from a new ASPICE process** in this session, the reward is boosted by 0.2. This incentivises the algorithm to spread coverage across all six processes early in the session, rather than spending all 12 questions on a single process.

### 2.5 The Learning Update (LinUCB Update Rule)

After receiving the reward, the question's matrices are updated:

```
A  ←  A + x · xᵀ       (outer product update)
b  ←  b + reward · x   (reward-weighted context)
```

- `A` accumulates information about which contexts have been explored. The more a question is used in a particular context, the more confident the estimate becomes.
- `b` accumulates reward signals weighted by context. If a question consistently gets high rewards when asked to a certain stakeholder role, `b` grows in that role's direction.

Over many sessions, `θ = A⁻¹b` converges to the weight vector that best predicts the reward for each question given the context — effectively learning which questions are most revealing for which type of user.

---

## 3. Question Bank Design

### 3.1 Structure

Each audit question belongs to exactly one **ASPICE process** (SWE.1–SWE.6) and one **capability level** (L1 = Performed, L2 = Managed, L3 = Established). Each question has exactly **5 answer options** (A–E), ranging from best practice (weight 0) to most concerning (weight 4).

The `base_practice_id` field records which ASPICE base practice the question is assessing (e.g., `SWE.1.BP1` = Software Requirements Analysis, Base Practice 1). This ensures full traceability — every question can be mapped back to a specific requirement in the ASPICE PAM (Process Assessment Model).

### 3.2 Stakeholder Targeting

Each question records which stakeholder roles are expected to give meaningful answers (e.g., a question about unit testing is most relevant to test engineers and software developers). This allows the system to filter eligible questions per session — ensuring users are only asked questions within their area of competence, which improves both answer quality and user experience.

### 3.3 Question Bank Coverage

The initial question bank contains **42 questions and 210 options**, covering:
- 6 processes × approximately 7 questions per process
- Each process covers at least L1 and L2, with selected L3 questions for processes where organisational-level maturity is a common assessor finding

---

## 4. Session Flow (How an Audit Works)

1. **User starts a session** — the system creates an audit session record and builds an initial context vector from the user's profile.
2. **First question selected** — the CMAB engine scores all eligible questions using the UCB formula and picks the highest-scoring one.
3. **User answers** — the answer is recorded, a reward is computed, and the bandit arm for that question is updated.
4. **Next question selected** — the context vector is rebuilt (now reflecting the answered question's process and the user's response), and the next question is chosen.
5. **Steps 3–4 repeat** for up to 12 questions.
6. **Session completed** — the weakness classifier computes scores for all 18 (process × level) combinations, identifies the top weaknesses, and stores the result.
7. **User sees results** — a radar chart across SWE.1–SWE.6, a heatmap of L1/L2/L3 per process, and a list of the top 3 weakness areas with recommendations.

---

## 5. Key Design Decisions

### Why 12 questions maximum?
A full question bank covers 6 processes × 3 levels = 18 combinations. Asking 12 questions (67% coverage) provides a meaningful signal while keeping the audit short enough for a real stakeholder to complete in a single sitting. The bandit algorithm is specifically designed to maximise information gain within this fixed budget — it is not a random sample.

### Why weight 0–4 instead of a larger scale?
The reward formula normalises the weight by dividing by the maximum (`weight / 4.0`), producing 5 clean reward levels: 0.0, 0.25, 0.5, 0.75, 1.0. A finer scale (e.g., 0–10) would introduce unnecessary precision given the subjective nature of the answer choices, and would require more sessions to learn reliable reward estimates.

### Why store the full A matrix per question?
An alternative design would recompute the matrix from the full response history on every question selection. Storing the matrix is the standard LinUCB approach and allows O(1) retrieval of the learned state. As the system accumulates thousands of sessions, replaying history on every request would become a performance bottleneck.

### Why keep question and answer options as separate records?
Storing options inside the question row as a JSON array was considered but rejected: the option's weight value must be queried independently — it is the core input to both the reward function and the weakness score computation. Treating options as first-class database records makes these queries efficient and type-safe.
