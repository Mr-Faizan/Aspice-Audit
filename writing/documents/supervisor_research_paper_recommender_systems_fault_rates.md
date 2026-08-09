# Recommender Systems for Reducing Software Fault Rates in Automotive Software Development

> **Source:** Dimitrios Datsogiannis, Wolfram Hardt — Professorship of Computer Engineering,
> **TU Chemnitz**. Published in *2025 International Symposium on Computer Science and
> Educational Technology (ISCSET)*. DOI: 10.1109/ISCSET65760.2025.11540532. IEEE,
> 979-8-3315-6503-9/25.
>
> **Relationship to the other supervisor paper:** this is the **direct follow-up/extension**
> of `supervisor_research_paper_new_approach_early_detection_vulnerabilities.md` (2024,
> Datsogiannis/Heller/Hardt) — the paper's own Introduction states: *"This paper extends the
> already presented concept in [8] and focuses on the application of the algorithms, the
> selected tuning parameters, and the performance of each applied algorithm within each
> selected scenario."* Reference [8] in this paper **is** the 2024 paper. Read them as a
> pair: 2024 = concept/architecture, 2025 = concrete algorithm comparison and simulated
> evaluation.
>
> **Why this file is the single most load-bearing related-work source for Ch.6–7:** this is
> the closest thing in the literature to the **exact evaluation your thesis needs to run or
> at least discuss** — a head-to-head comparison of **e-Greedy, LinUCB, and Thompson
> Sampling** on a CMAB-driven ASPICE-style question recommender, under four **simulated
> fault-change-rate scenarios**, measured via cumulative reward, average reward, and a
> four-band reward distribution. This directly matches (and partially fulfills in advance)
> the "Simulation-Based Benchmarking of LinUCB against Baselines" item you already listed as
> future work in Ch.8.4.2 — see the callouts throughout.

**Keywords:** Automotive, development, process, recommender systems, software

---

## Abstract

This paper presents the research results of using a recommendation system (RS) to evaluate
automotive development processes from the initial design phases to the final software
release. The model uses a dynamic questionnaire managed by a recommender system, which aims
to detect deficiencies and faults during the development while increasing transparency among
stakeholders. **The question pool with 137 questions**, consists of weighted questions,
derived from key development metrics and serves as the basis for this evaluation. Questions
are selected during each development cycle with **Contextual Multi-Armed Bandit (CMAB)**
algorithms, allowing for minimal stakeholder effort while maximizing feedback relevance. The
current study explores the system's performance across **four behavioral change scenarios**
that simulate different rates of software fault occurrence. **Three reinforcement learning
algorithms, e-Greedy, LinUCB, and Thompson Sampling**, were applied and compared. The tuning
of the algorithms is also part of the performance assessment. The results are assessed based
on the defined performance indicators. The findings indicate that the system is not only
scalable but also achieves improved performance over time as it continues to operate and
adapt to changing development conditions.

> **Scale comparison:** this paper's question pool has **137 questions** across (implicitly)
> a broader ASPICE scope than yours; your seeded question bank has **42 questions / 210
> options** across SWE.1–SWE.6 only. Cite this directly when framing your question-bank
> scale in Ch.5.4/Ch.7 — you cover one process group in depth (7 questions/process ×
> 6 processes ≈ 42) vs. their broader-but-shallower coverage.

---

## I. Introduction

The growing complexity of automotive software development originates from the increasing
number of electronic and electrical components [1]. On the one hand, the automotive
architecture is distributed in inter-vehicle networks, which ensures that the vehicle remains
connected to the cloud components that play a fundamental role in most of the essential
activities [2]. On the other hand, there is intra-vehicle communication with the onboard
components [3]. Both aspects of vehicle development are very demanding as they must handle
very high levels of complexity, especially when all components are in the design and
development phase. Moreover, the vehicles have to ensure compatibility with 3rd-party
components and software deliveries [4]. The complexity further increases as onboard and
back-end systems become more closely linked [5], while evolving hardware generations demand
more precise validation through diverse testing methods [6]. The software integration levels
are responsible for validation, verification, and testing of the software deliveries, until
the final integration of all software components into the vehicle. Additionally, the
development stakeholders have to manage the development of new features while tackling bugs
identified from the previous software release.

The main challenge is to identify faults in the early development phases. This is becoming
increasingly difficult, while addressing issues later in the development cycle leads to
higher costs. In contrast, early detection reduces expenses and improves quality. As the
development basis is based on the **V-model** [7] and its variations, this paper examines a
different approach to evaluation, **defining the milestones of the V-model as handovers in
which information between stakeholders is exchanged**. This paper extends the already
presented concept in [8] and focuses on the application of the algorithms, the selected
tuning parameters, and the performance of each applied algorithm within each selected
scenario.

---

## II. State of the Art

This paper covers five main research areas: ISO standards and norms, the definition of
software metrics, automatic software module evaluation and fault prediction, defect
management of software faults, and finally, recommendation systems with reinforcement
learning, which are examined in relation to the scope and limitations of this study.

### A. Software Metrics for Quality and Process Evaluation

Software metrics serve as quantitative tools for evaluating software development, including
the development process and the final software product [9], [10]. Through objective
evaluation, these metrics contribute to enhancing the efficiency, quality, and predictability
of the software development life cycle. Generally, software metrics are classified into two
main categories: **product metrics** and **process metrics**. Product metrics focus on
characteristics of the software, such as functionality, performance, complexity, and
testability, providing a basis for assessing software quality. In contrast, process metrics
evaluate development activities, aiming to measure the efficiency and effectiveness of the
underlying processes. Many researchers have proposed sets of metrics, such as the
**Chidamber and Kemerer (CK) metrics** [11], **MOOD metrics** by Abreu and Carapuca [12], and
**QMOOD** by Bansiya and Davis [13].

### B. ISO Standards and Norms

As modern automotive systems incorporate increasingly complex software and hardware with a
high degree of dependencies, the demand for standardized software architectures and
interfaces has intensified. In response, alliances have emerged to establish open standards
and development guidelines. Among the most significant frameworks relevant to this work are
**AUTOSAR** [14], which provides a standardized framework developed to support the
development of embedded software in vehicles [15], **ASPICE** [16], aligned with the
ISO/IEC 330xx standards and used to assess the maturity of specific processes, and **ISTQB**
[17], which contributes significantly to software quality assurance in the automotive sector
by promoting standardized testing methodologies and certification programs. Each of these
plays a pivotal role in shaping software development practices within the automotive
industry.

For this study, these frameworks were analyzed to extract principles and metrics that can
later be transformed into questions for integration into the model [8].

### C. Automatic Software Module Evaluation and Fault Prediction with Artificial Intelligence

Several studies define metrics aimed at preventing faults or enabling their early detection
[18], [19]. Fault prediction models seek to minimize fault-prone components by identifying
potential issues before they appear in later stages of development.

Recent papers in **software fault prediction (SFP)** have highlighted the effectiveness of
machine learning (ML) and deep learning (DL) models for identifying faulty software modules.
Surveys by Pandey et al. [20] and Batool and Khan [21] outline the evolution of SFP
techniques, noting the transition from traditional statistical methods to sophisticated ML
and DL approaches. Ensemble models [22] have been proven to exceed the performance of unique
models due to their ability to include diverse decision patterns. Borandag [23] further
demonstrates the advantages of combining recurrent neural networks (RNNs) with ensemble
strategies, leading to improved predictive performance. Furthermore, optimization-driven
methods were also applied [24]. Finally, another approach is to tackle the frequently
observed software fault resulting from data imbalance in SFP, proposing diversity-aware
strategies that stabilize predictions across varying data distributions [25].

### D. Defect Management of Software Faults

As software development remains a complex activity, bugs are still delivered when a software
build is created.

**Fig. 1** illustrates the development process for handling defects identified during
validation and verification testing. Once defect analysis is conducted and the corresponding
bugs are identified, the faults must be corrected. If the faults are due to inconsistencies in
specifications or architecture, all related dependencies must be reviewed, and additional
modifications to software or hardware components may be necessary. **It is also evident that
the later a defect is addressed, the greater the effort required for its resolution and
subsequent confirmation through testing** [26], [27].

**Fig. 1 — "Process of bug finding and fixing in relation to time" [29]:** a horizontal
swimlane diagram with a Time arrow at top and bottom. Five sequential stage columns —
*Architecture*, *SW Development*, *Module Tests*, *Integration Tests*, *Functional Tests*,
*System Tests* — each showing a repeating "Defect found → Defect creation → Defect analysis"
loop. A "Bugfixing" label with a decision diamond ("Architecture issue? Yes/No") sits at the
left, feeding back into earlier stages when the answer is "Yes" — visually reinforcing that
the further right (later) a defect is caught, the more upstream rework it triggers. *(Source
citation: Schäuffele & Zurawka, Automotive Software Engineering, 2016 — ref. [29], same
textbook as ref. [16]/[20] in the 2024 paper.)*

Artificial intelligence offers considerable potential for enhancing various aspects of
automotive software engineering. It can improve classification performance, enable automated
fault detection and analysis, and help maintain high quality standards [28]. Given the
inherent complexity of ASD, effective fault management represents a major challenge and
demands substantial effort from stakeholders to ensure system reliability and transparency. A
wide range of tools are used in the industry to manage testing and software defects. These
platforms have become increasingly essential for tracking and evaluating the progress of
software releases, particularly in the absence of robust alternatives.

> **Direct citation for your Ch.1.1/1.2 Motivation:** this "later = costlier" defect-cost
> curve (Fig. 1) plus the "in the absence of robust alternatives" line is another strong,
> directly citable justification for why continuous/early ASPICE-style feedback (your
> thesis's whole premise) beats waiting for defect-tracking-system tickets to accumulate.

### E. Recommender Systems Applications and Limitations

Recommender systems (RS) are widely used in areas such as online advertising, social media,
news, online learning, travel, and many other applications [30]. **However, their
application for identifying software faults and process deficiencies is not yet common.**
This study outlines the fundamental requirements and introduces a corresponding concept for
applying RS in the automotive domain [31]. To investigate RS in the context of this study, we
first analyzed the specific characteristics and limitations of our approach. The challenges
that guided the selection of an appropriate RS methodology for this work are as follows:

- **Cold Start:** The cold start problem indicates the difficulty of generating accurate
  recommendations due to limited or missing interaction data for new users or items [32].
- **Data Sparsity:** *(printed as "Data Parsity" in source — likely a typo for "sparsity")*
  is the challenge of making accurate recommendations when user-item interaction data is
  limited or unevenly distributed [33].
- **Partial Feedback:** occurs when user responses are only available for displayed items,
  making it difficult to learn preferences for unseen options and potentially biasing the
  model [34].

> **Directly relevant to your Ch.4.5.7/Ch.7.6/Ch.8.3:** this three-way framing (cold start /
> data sparsity / partial feedback) is the clean academic vocabulary for exactly the
> constraints your own CMAB engine faces — e.g., every new question starts with `A = I`,
> `b = 0` (cold start, cf. `Implementation.md` §2.2), and each session only observes the
> reward for the *one* question actually asked (partial feedback — the core justification for
> using a bandit rather than a supervised classifier in the first place). Cite [32]/[33]/[34]
> directly if you want a peer-reviewed citation for each of these three specific limitations
> rather than restating them without support.

The concept developed in this study takes these limitations into account and introduces a
recommender system that is approached as a **Contextual Multi-Armed Bandits (CMAB)** problem
to evaluate the automotive processes. CMAB is a very efficient and simplified reinforcement
learning approach which addresses the exploration–exploitation dilemma.

Numerous studies have researched the challenge of balancing exploration and exploitation in
decision-making processes. Among the most significant approaches are the **Epoch-Greedy
algorithm** [35], the **Linear Upper Confidence Bound (LinUCB) method** [36], and **Thompson
Sampling** [37]. These strategies are often integrated with contextual multi-armed bandit
algorithms, enabling agents to identify optimal actions based on situational variables and
expected outcomes. This form of contextualized exploration helps mitigate biases introduced
by prior decisions and is particularly effective in dynamic environments.

---

## III. Concept Summary

The framework of this work is analyzed and presented in detail in [8] *(the 2024 companion
paper)*. In summary, an RS is implemented to manage a dynamic questionnaire. The questions,
stored in a database, represent evaluation parameters and metrics derived from a systematic
literature review. The methodology used for the literature review is illustrated in **Fig.
2**. It outlines the process followed to extract relevant data, which was subsequently
transformed into evaluation questions for the model. Each question is paired with predefined
answer options. These answers are assigned a score, which serves as a reward for the RL
agent. Additionally, **each question is assigned a weight, ensuring that its importance
influences the selection process**. This weighting mechanism plays a key role as the agent
balances exploration and exploitation [8]. The questions are addressed only to specific
stakeholders who are directly involved with the content of each question. **The RL agent is
configured to select five questions per round for each stakeholder [8].** The overall study
is based on the V-model, in which each milestone is interpreted as a handover point involving
both responsibility and information exchange. These milestones also serve as the temporal
reference points for applying the evaluation concept developed in this study.

**Fig. 2 — "Literature review and findings extraction for the evaluation framework":** a
top-level "Literature Review" banner feeds four parallel category columns, each with several
sub-topic boxes stacked beneath it, all funneling down into a single "Database for the
Collection of Metrics and Principles" banner at the bottom:

| Software Development | Automotive Software Development | Automotive Special Topics | Standards and Norms |
|---|---|---|---|
| Systems Engineering Principles | Automotive Software Releases Principles | Inter-Vehicle Development Principles | AUTOSAR |
| Requirement Engineering Principles | Automotive Specification and Architecture Principles | Vehicle Ecosystems | ASPICE |
| Software Development Principles | Automotive Software Development Principles | Software Updates after Production | ISTQB |
| Software Development Metrics | Automotive Software Development Metrics | | |
| Software Development Key Performance Indicators | Test Management Metrics & Principles | | |
| | Defect Management Metrics & Principles | | |

> **This is the fullest picture yet of where the underlying "137 questions" came from** —
> useful for Ch.3 (State of the Art) or Ch.5.4 if you want to contrast your own, narrower
> question-sourcing methodology (ASPICE SWE.1–6 base practices only, per
> `aspice.md` §6) against this paper's four-pronged literature-derived sourcing (general SE
> principles + automotive-specific SE + automotive "special topics" like OTA updates/vehicle
> ecosystems + formal standards AUTOSAR/ASPICE/ISTQB).

**Key parameter carried over from [8] and reused here:** the RL agent selects **five
questions per round** per stakeholder (contrast with your tool's session budget of
**12 questions total** per session, per `Architecture.md` §4).

---

## IV. Experimental Setup

The experimental setup is the main focus of this study, followed by the presentation of the
results and the evaluation of the concept.

### A. Algorithms for CMAB Selection

Considering the requirements and limitations for selecting a suitable recommender system for
this study, the problem can be effectively approached as a CMAB model. **Each question is
handled as an arm**, and the RL agent is responsible for selecting them during each
interaction.

To address the exploration and exploitation dilemma, **three algorithms are employed:
e-Greedy, LinUCB, and Thompson Sampling**, as presented in [8]. The tuning parameters of
these algorithms were extensively tested and subsequently selected; their configuration is
detailed in the results section of this work.

### B. Fault Changing Rate Scenarios

A simulated testing environment is developed specifically for the purposes of this study. Its
primary objective is to cover the real behavior of software development and release processes
within the automotive domain.

To achieve this, fault and deficiency change rate scenarios were introduced. These scenarios
are differentiated based on the variation in deficiencies observed across evaluation rounds.
**Four scenarios are examined:**

1. The first assumes that the deficiency behavior **remains stable** throughout the
   evaluation (CR = 0.0%).
2. The second introduces a **10% change** in deficiencies per round (CR = 10%).
3. The third a **30% changing rate** (CR = 30%).
4. The fourth represents an extreme case with a **50% changing rate** during each evaluation
   round (CR = 50%).

**Fig. 3 — "Example of comparison of the 0% and the 30% use case scenarios":** two parallel
timelines, "Project X" (top, 0% changing behavior) and "Project Y" (bottom, 30% changing
behavior), each showing three sequential "Results found after [first/second/third] round of
evaluation" boxes listing ~10 numbered deficiencies (e.g., "Deficiency 1" ... "Deficiency
10"). In **Project X**, the same 10 deficiencies (marked with X) recur identically across all
three rounds — labeled "Case 1: Always the same deficiencies → 0% changing behaviour." In
**Project Y**, some deficiency numbers change between rounds (e.g., new deficiency IDs like
12, 11, 19, 22 appear, others drop out) — labeled "Case 2: Not always the same deficiencies →
30% changing behaviour."

> **Directly actionable for your Ch.8.4.2 future-work item** ("Simulation-Based Benchmarking
> of LinUCB against Baselines"): this is the *exact* simulation design you'd need to
> replicate or adapt — a synthetic "ground truth" deficiency set per simulated project that
> either stays fixed or churns by a defined percentage each round, letting you measure how
> well each algorithm re-discovers/tracks the (possibly moving) set of true weaknesses.
> Consider citing this paper's four-scenario design (0/10/30/50% churn) as the template if
> you ever build that simulation harness — or, alternatively, explicitly note in Ch.8.4.2
> that this exact benchmarking design already exists in the literature (cite this paper) and
> that your own real-pilot-data approach is the complementary, non-simulated alternative.

---

## V. Results and Discussion

The main results of the application of the algorithms are presented, and their impact on the
research objectives is assessed and outlined.

### A. Tuning Parameters for each Algorithm

Initially, each of the three algorithms was evaluated using a range of tuning parameters.
Four distinct parameter configurations were selected for each algorithm to capture a broad
spectrum between exploratory and exploitative behavior. For each algorithm, the best
performing parameter setting was retained for the subsequent evaluation steps.

**Fig. 4 — "Selection of RS tuning parameter for each use case":** a decision-tree-style
diagram. "Evaluation tool" branches into 4 use cases (changing rate 0%, 10%, 30%, 50%), each
of which branches into the 3 algorithms (ε-Greedy, LinUCB, Thompson Sampling), each showing
its selected optimal tuning value:

| Use case | ε-Greedy | LinUCB | Thompson Sampling |
|---|---|---|---|
| 1 (CR 0.0%) | ε = 0.5 | α = 0.1 | α = 0.5 |
| 2 (CR 10%) | ε = 0.3 | α = 0.1 | α = 5.0 |
| 3 (CR 30%) | ε = 0.5 | α = 2.0 | α = 5.0 |
| 4 (CR 50%) | ε = 0.3 | α = 0.1 | α = 5.0 |

> **Directly relevant to your `cmab_engine.py`:** your own LinUCB implementation uses a fixed
> **α = 1.0** (per `Architecture.md`/`README.md`: *"LinUCB α = 1.0 — balanced
> exploration/exploitation; tunable via the alpha parameter"*). This table shows that in the
> most comparable scenario to a stable ASPICE process (CR = 0%, i.e., deficiencies don't
> shift between sessions), the optimal α found by grid search was **0.1**, not 1.0 — and
> even in noisier scenarios it only rose to 2.0. This is directly citable evidence for a
> **Future Work or Discussion point in Ch.7.5/Ch.8.4**: your fixed α = 1.0 is a reasonable
> default but is not empirically tuned, and prior work suggests the optimal value may be
> considerably lower for a low-churn process like SWE.1–6 assessment.

### B. Evaluation of each Algorithm and Performance Indicators

After selecting the best performing tuning parameter for each algorithm and use case, the
three algorithms were subsequently compared based on their performance within each scenario.
**Three performance indicators** were defined to measure and compare the effectiveness of the
algorithms:

- **Cumulative rewards** that the agent collected over the evaluation rounds.
- **Average rewards** that the agent collected from each round.
- **Distribution of rewards** for a scale 0 to 1, clustered into four categories.

The execution of the evaluation was set to **1000 rounds**.

**Fig. 5 — "Cumulative rewards for CR = 0.0% with e-Greedy":** a line chart, x-axis "Rounds"
(0–1000), y-axis "Cumulative Rewards" (0–3500+), plotting four lines for ε = 0.2, 0.5, 0.8, 0.9
— all rising roughly linearly, with ε = 0.5 (highlighted/annotated) tracking slightly above
the others by round 1000.

**Fig. 6 — "Average rewards for CR = 0.0% with e-Greedy":** a line chart, x-axis "Rounds"
(0–1000), y-axis "Average Rewards" (0.30–0.70), showing a single line for ε = 0.5 that starts
noisy/volatile in the first ~100 rounds, then stabilizes and climbs smoothly to plateau around
~0.65–0.68 by round 1000 — illustrating **how many rounds the agent needs to reach stable
performance**.

The average reward is calculated based on the agent selecting **five questions per round**.
**Each reward is determined by multiplying the weight of the selected question by the score
assigned to the corresponding answer.**

> **Important formula difference from your own reward function:** this paper's reward =
> `question_weight × answer_score` (a **multiplicative** combination of two independent
> factors). Your own reward function (per `Implementation.md` §2.4) is
> `reward = (option.weight / 4.0) + coverage_bonus`, clamped to [0,1] — an **additive**
> combination of a normalized answer weight plus a coverage bonus, with **no separate
> per-question importance weight** feeding into the reward at all (importance instead lives
> implicitly in which questions get selected via LinUCB's learned θ). This is a substantive,
> citable **design contrast** worth an explicit paragraph in Ch.4.9 or Ch.4.5.5: your
> approach folds "process-coverage incentive" into the reward instead of a literal
> question-importance multiplier, trading direct question-weighting for encouraging spread
> across ASPICE processes.

**Fig. 7 — "Count of rewards for CR = 0.0% with e-Greedy":** a pie chart with four slices:
**Above 0.75: 47.2%**, **0.5 to 0.75: 16.1%**, **0.25 to 0.5: 14.5%**, **Up to 0.25: 22.3%**.
The cluster above 0.75 represents the most important questions paired with the highest-scoring
answers.

### C. Evaluation Results and Discussion

To determine which algorithm and tuning parameter combination performs best for each use
case, the results are summarized in **Table I**. The table shows that **e-Greedy outperforms
the other algorithms in most scenarios**; however, its tuning parameter must be carefully
adjusted depending on the specific use case. The evaluation platform developed for this study
supports the identification of the current use case based on observed results and allows for
refinement of the tuning parameters when applied in real-world scenarios.

**Table I — Evaluation Results for Each Use Case:**

| Use case | Algorithm | Tuning parameter | Rewards above 0.75 | Rewards between 0.5 and 0.75 | Rewards between 0.25 and 0.5 |
|---|---|---|---|---|---|
| **CR: 0.0%** | ε-Greedy | ε = 0.5 | **47.2%** | 16.1% | 14.5% |
| | LinUCB | α = 0.1 | 34.4% | 24.4% | 21.8% |
| | Thompson Sampling | α = 0.5 | 36.7% | 29.6% | 20.8% |
| **CR: 10%** | ε-Greedy | ε = 0.3 | **30.5%** | 24.6% | 21.5% |
| | LinUCB | α = 0.1 | 25.1% | 24.9% | 24.1% |
| | Thompson Sampling | α = 5.0 | 24.3% | 26.3% | 25.9% |
| **CR: 30%** | ε-Greedy | ε = 0.5 | **26.6%** | 26.2% | 24.6% |
| | LinUCB | α = 2.0 | 24.3% | 25.5% | 24.8% |
| | Thompson Sampling | α = 5.0 | 24.1% | 25.8% | 25.2% |
| **CR: 50%** | ε-Greedy | ε = 0.5 | **25.3%** | 25.2% | 24.9% |
| | LinUCB | α = 0.1 | 24.3% | 25.3% | 25.7% |
| | Thompson Sampling | α = 5.0 | 23.9% | 25.9% | 25.0% |

> **Critical, directly citable finding for your thesis's Discussion/Limitations section:**
> the headline empirical result of this companion paper is that **e-Greedy — not LinUCB —
> won on every single one of the four scenarios**, and the margin over LinUCB/Thompson
> Sampling *shrinks toward near-parity as the churn rate rises* (47.2% → 25.3% for e-Greedy
> vs. 34.4%→24.3% for LinUCB at CR 0%→50%: the "advantage" nearly vanishes at high churn).
> Since **your thesis chose LinUCB, not e-Greedy**, this is exactly the kind of finding you
> need to address head-on rather than ignore:
> - It's a legitimate basis for a **Ch.7.6 Threats to Validity** point: "the closest
>   comparable prior work [cite this paper] found e-Greedy to outperform LinUCB under
>   simulated churn; this thesis did not benchmark LinUCB against alternative algorithms on
>   real data, so whether LinUCB is in fact the best choice for this specific SWE.1–6 use
>   case remains an open empirical question" (this maps directly onto your existing Ch.8.4.2
>   future-work item — you can now cite a concrete number instead of describing it in the
>   abstract).
> - Alternatively, you can note that LinUCB's specific advantage (per `Architecture.md`) is
>   **determinism and reproducibility for thesis experiments**, not necessarily raw reward
>   maximization — a legitimate methodological reason to prefer LinUCB even if e-Greedy
>   showed a slight edge in a different paper's simulated setting. Either framing is valid;
>   just don't leave this contradiction unaddressed if a reviewer/examiner has read both
>   papers.

---

## VI. Conclusion

This work analyzes the findings of the framework previously introduced in [8], which
evaluates software releases based on software quality and development process performance.
The model is developed from a set of questions resulting from a systematic literature review
on automotive software metrics related to quality and process assessment. These questions are
managed by a recommender system that intelligently selects and assigns them to key
development stakeholders. By selecting only a small subset of questions from a larger pool,
the system minimizes the effort required from stakeholders while maintaining evaluation
effectiveness. The model employs Contextual Multi-Armed Bandit algorithms, enabling the
reinforcement learning agent to efficiently identify deficiencies in software releases and
development processes. **The approach was extensively evaluated in a simulated environment
across four distinct behavioral scenarios. A next publication will provide the evaluation
results of applying this approach in real-world automotive development environments.**

> **This closing sentence is the single most important line in this file for your thesis's
> novelty claim.** As of this paper (2025), the supervisor's own research line has evaluated
> the concept **only in simulation** — real-world deployment/evaluation is explicitly framed
> as a *future, not-yet-published* piece of work. If that "next publication" doesn't yet
> exist (worth checking Google Scholar / IEEE Xplore for a 2026 Datsogiannis/Hardt paper
> before finalizing your Ch.3 Research Gap), **your thesis may be the first real-pilot-data
> evaluation in this entire research line** — a very strong, precisely-scoped contribution
> claim for Ch.1.4 and Ch.3.6: "this thesis provides the first implementation and real-world
> (non-simulated) pilot evaluation of the CMAB-based ASPICE recommender concept introduced by
> [cite 2024 paper] and benchmarked only in simulation by [cite this 2025 paper]."

---

## References (full list — candidates for reuse in the thesis bibliography)

`[1]` Y. Zhang, T. Liu, H. Zhao, and C. Ma, "Risk analysis of can bus and ethernet
communication security for intelligent connected vehicles," in *2021 IEEE International
Conference on Artificial Intelligence and Industrial Design (AIID)*, 2021, pp. 291–295.
*(same as ref. [1] in the 2024 paper.)*

`[2]` M. L. Sichitiu and M. Kihl, "Inter-vehicle communication systems: a survey," *IEEE
Communications Surveys & Tutorials*, vol. 10, no. 2, pp. 88–105, 2008.

`[3]` S. Tuohy, M. Glavin, C. Hughes, E. Jones, M. Trivedi, and L. Kilmartin, "Intra-vehicle
networks: A review," *IEEE transactions on intelligent transportation systems*, vol. 16, no.
2, pp. 534–545, 2014.

`[4]` S. Fürst, "Challenges in the design of automotive software," in *2010 Design,
Automation & Test in Europe Conference & Exhibition (DATE 2010)*. IEEE, 2010, pp. 256–258.

`[5]` A. Iwai and M. Aoyama, "Automotive cloud service systems based on service-oriented
architecture and its evaluation," in *2011 IEEE 4th International Conference on Cloud
Computing*. IEEE, 2011, pp. 638–645.

`[6]` J. Schäuffele and T. Zurawka, *Automotive software engineering*. Springer, 2010.
*(earlier edition of the same textbook cited as [16]/[20] in the 2024 paper and [29] below.)*

`[7]` S. Mathur and S. Malik, "Advancements in the v-model," *International Journal of
Computer Applications*, vol. 1, no. 12, pp. 29–34, 2010.

`[8]` D. Datsogiannis, A. Heller, and W. Hardt, "A new approach for early detection of
vulnerabilities across the automotive software development," in *2024 International Symposium
on Computer Science and Educational Technology (ISCSET)*. IEEE, 2024, pp. 1–5. **← the 2024
companion paper, already captured in full in
`supervisor_research_paper_new_approach_early_detection_vulnerabilities.md`.**

`[9]` M. Shepperd and D. Ince, *Derivation and validation of software metrics*. Oxford
University Press, 1993.

`[10]` N. F. Schneidewind, "Methodology for validating software metrics," 1992.

`[11]` S. R. Chidamber, D. P. Darcy, and C. F. Kemerer, "Managerial use of metrics for
object-oriented software: An exploratory analysis," *IEEE Transactions on software
Engineering*, vol. 24, no. 8, pp. 629–639, 2002.

`[12]` R. Harrison, S. J. Counsell, and R. V. Nithi, "An evaluation of the mood set of
object-oriented software metrics," *IEEE Transactions on Software Engineering*, vol. 24, no.
6, pp. 491–496, 1998.

`[13]` J. Bansiya and C. G. Davis, "A hierarchical model for object-oriented design quality
assessment," *IEEE Transactions on software engineering*, vol. 28, no. 1, pp. 4–17, 2002.
*(same as ref. [6] in the 2024 paper.)*

`[14]` "Automotive open system architecture." [Online]. Available: https://www.autosar.org/
(2024)

`[15]` T. Hermans, P. Ramaekers, J. Denil, P. De Meulenaere, and J. Anthonis, "Incorporation
of autosar in an embedded systems development process: A case study," in *2011 37th
EUROMICRO Conference on Software Engineering and Advanced Applications*. IEEE, 2011, pp.
247–250.

`[16]` "Automotive-spice." [Online]. Available: https://vda-qmc.de/en/automotive-spice/
(2024) *(same as ref. [18] in the 2024 paper.)*

`[17]` "International software testing qualifications board." [Online]. Available:
https://www.istqb.org/ *(same as ref. [28] in the 2024 paper.)*

`[18]` Z. H. Martinez, P. M. Moreno, J. A. Vergara Camacho, and G. C. Vega, "Study on the use
of defect metrics in the software development process. flaws and vulnerabilities," in *2023
IEEE International Conference on Engineering Veracruz (ICEV)*, 2023, pp. 1–7. *(same as ref.
[3] in the 2024 paper.)*

`[19]` T. B. Alakus, R. Das, and I. Turkoglu, "An overview of quality metrics used in
estimating software faults," in *2019 International Artificial Intelligence and Data
Processing Symposium (IDAP)*, 2019, pp. 1–6. *(same as ref. [4] in the 2024 paper.)*

`[20]` S. Pandey, R. Mishra, and A. Tripathi, "Machine learning based methods for software
fault prediction: A survey," *Expert Systems with Applications*, vol. 172, p. 114605, 2021.

`[21]` I. Batool and T. A. Khan, "Software fault prediction using data mining, machine
learning and deep learning techniques: A systematic literature review," *Computers &
Electrical Engineering*, vol. 99, p. 107739, 2022.

`[22]` S. Rathore and S. Kumar, "An empirical study of ensemble techniques for software fault
prediction," *Applied Intelligence*, vol. 51, pp. 8324–8344, 2021.

`[23]` E. Borandag, "Software fault prediction using an rnn-based deep learning approach and
ensemble machine learning techniques," *Applied Sciences*, vol. 13, no. 3, p. 1422, 2023.

`[24]` Y. Hassouneh, H. Turabieh, T. Thaher, and I. Tumar, "Boosted whale optimization
algorithm with natural selection operators for software fault prediction," *IEEE Access*,
vol. 9, pp. 129962–129982, 2021.

`[25]` P. Manchala and M. Bisi, "Diversity based imbalance learning approach for software
fault prediction using machine learning models," *Applied Soft Computing*, vol. 122, p.
108796, 2022.

`[26]` V. Suma and T. Nair, "Defect management strategies in software development," *arXiv
preprint arXiv:1209.5573*, 2012.

`[27]` I. A. Memon, Q. B. Jamali, A. S. Jamali, M. K. Abbasi, N. A. Jamali, and Z. H. Jamali,
"Defect reduction with the use of seven quality control tools for productivity improvement at
an automobile company," *Engineering, Technology & Applied Science Research*, vol. 9, no. 2,
pp. 4044–4047, 2019.

`[28]` M. A. Khan, N. S. Elmitwally, S. Abbas, S. Aftab, M. Ahmad, M. Fayaz, and F. Khan,
"Software defect prediction using artificial neural networks: A systematic literature
review," *Scientific Programming*, vol. 2022, no. 1, p. 2117339, 2022.

`[29]` J. Schäuffele and T. Zurawka, *Automotive Software Engineering*. Springer Fachmedien
Wiesbaden, 2016. [Online]. Available: http://dx.doi.org/10.1007/978-3-658-11815-0 *(same book
as ref. [16]/[20] in the 2024 paper — this is clearly the group's core automotive-SE textbook
citation; make sure it's in your `bibliography.bib`.)*

`[30]` L. Lü, M. Medo, C. H. Yeung, Y.-C. Zhang, Z.-K. Zhang, and T. Zhou, "Recommender
systems," *Physics reports*, vol. 519, no. 1, pp. 1–49, 2012.

`[31]` R. Bader, "Proactive recommender systems in automotive scenarios," Ph.D. dissertation,
Technische Universität München, 2013.

`[32]` K. Rama, P. Kumar, and B. Bhasker, "Deep learning to address candidate generation and
cold start challenges in recommender systems: A research survey," *arXiv preprint
arXiv:1907.08674*, 2019.

`[33]` S.-M. Choi, D. Lee, K. Jang, C. Park, and S. Lee, "Improving data sparsity in
recommender systems using matrix regeneration with item features," *Mathematics*, vol. 11,
no. 2, p. 292, 2023.

`[34]` Y. Bechavod, K. Ligett, A. Roth, B. Waggoner, and S. Z. Wu, "Equal opportunity in
online classification with partial feedback," *Advances in Neural Information Processing
Systems*, vol. 32, 2019.

`[35]` J. Langford and T. Zhang, "The epoch-greedy algorithm for contextual multi-armed
bandits," *Advances in neural information processing systems*, vol. 20, no. 1, pp. 96–1,
2007.

`[36]` K.-H. Huang and H.-T. Lin, "Linear upper confidence bound algorithm for contextual
bandit problem with piled rewards," in *Pacific-Asia Conference on Knowledge Discovery and
Data Mining*. Springer, 2016, pp. 143–155. **← the most directly relevant LinUCB citation
across both papers; use this (or the 2024 paper's Gutowski et al. [26]) as your primary
LinUCB algorithmic citation in Ch.2.3.3.**

`[37]` S. Agrawal and N. Goyal, "Thompson sampling for contextual bandits with linear
payoffs," in *International conference on machine learning*. PMLR, 2013, pp. 127–135.

---

## Quick-reference: which references map to which of your thesis chapters

| Refs | Topic | Likely thesis home |
|---|---|---|
| [1], [2], [3], [4], [5], [6] | ICV complexity, inter-/intra-vehicle networks, 3rd-party integration, cloud/back-end linkage | Ch.1.1/1.2 (Motivation) |
| [7] | V-model foundations | Ch.2.1 background |
| [8] | The 2024 companion paper itself | Cite throughout as primary related work |
| [9], [10] | Foundational software-metrics validation methodology | Ch.3 (State of the Art) |
| [11], [12], [13] | CK / MOOD / QMOOD object-oriented metrics | Ch.3 — contrast against ASPICE-BP-based questions |
| [14], [15] | AUTOSAR | Ch.2/Ch.3 background (peripheral unless you discuss standards landscape) |
| [16] | ASPICE (VDA QMC) | Ch.2.1, throughout |
| [17] | ISTQB | Ch.3 (state of the art) |
| [18], [19] | Defect/fault metrics | Ch.3 |
| [20], [21] | SFP survey papers (ML/DL for fault prediction) | Ch.3 — position your rule-based classifier against ML-based SFP as deliberate MVP scope (cf. `Architecture.md` §8 "Why weighted scoring... rather than a trained ML model") |
| [22], [23], [24], [25] | Ensemble/RNN/optimization/imbalance-aware SFP techniques | Ch.3 (peripheral, unless deep-diving SFP alternatives) |
| [26], [27] | Defect management strategies, 7 QC tools | Ch.2/Ch.3 background |
| [28] | ANN-based defect prediction survey | Ch.3 |
| [29] | Schäuffele & Zurawka, *Automotive Software Engineering* — Fig. 1 source | Ch.2 background — same core textbook as the 2024 paper |
| [30] | Recommender systems survey (Lü et al.) | Ch.2.2 (Recommender Systems background) — good general RS citation |
| [31] | Bader PhD thesis — "Proactive recommender systems in automotive scenarios" | Ch.3 (State of the Art) — **check this one specifically**, it may be the closest full-length prior work on automotive RS and worth reading directly |
| [32], [33], [34] | Cold start / data sparsity / partial feedback | Ch.2.2/Ch.7.6 — cite for the three named RS limitations |
| [35] | Epoch-Greedy (Langford & Zhang) | Ch.2.3.4 (alternative algorithms) |
| [36] | LinUCB (Huang & Lin) | Ch.2.3.3 — primary LinUCB citation |
| [37] | Thompson Sampling (Agrawal & Goyal) | Ch.2.3.4 / Ch.4.9.1 (LinUCB vs. Thompson Sampling comparison) |

**Overlap with the 2024 paper's references:** [1], [6]≈[16 in 2024], [16]≈[18], [17]≈[28],
[18]≈[3], [19]≈[4] are the same underlying sources cited in both papers — when building your
`bibliography.bib`, add each **once** and cite it from wherever in the thesis it's needed,
rather than duplicating entries.
