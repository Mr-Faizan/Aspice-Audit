# A New Approach for Early Detection of Vulnerabilities Across the Automotive Software Development

> **Source:** Dimitrios Datsogiannis, Ariane Heller, Wolfram Hardt — Professorship of Computer
> Engineering, **TU Chemnitz**. Published in *2024 International Symposium on Computer
> Science and Educational Technology (ISCSET)*. DOI: 10.1109/ISCSET58624.2024.10807908.
> IEEE, 979-8-3503-9080-3/24.
>
> **Why this file matters more than a typical related-work note:** this paper comes from the
> **same research group and same supervisor (Prof. Dr. W. Hardt)** as this thesis, and
> describes an almost structurally identical concept — a CMAB-based recommendation system
> that selects weighted questions derived from ASPICE (among other sources) and poses them to
> **seven development stakeholder roles**, producing a **traffic-light classification**
> (red/yellow/green) of process weaknesses. This is very likely the direct conceptual
> ancestor/companion paper this thesis is meant to build on, narrow (to SWE.1–SWE.6 only),
> and actually implement end-to-end as a working web application. Treat this as the
> **primary related-work citation** and the main source for Ch.3 (State of the Art) — full
> text and the complete reference list are kept below since most of its ~28 references are
> candidates for reuse in the thesis bibliography.

**Index terms:** Automotive, development, process, recommendation systems, software

---

## Abstract

This paper presents a new approach of evaluating automotive development processes, starting
from the early stages of development to the final product. The main objective of this paper
is to ensure transparency among stakeholders and provide accurate feedback throughout the
development cycle, with the ultimate goal of preventing software defects and conflicts that
can be reproduced. The concept aims to enable stakeholders to efficiently evaluate the status
and quality of software releases. The latter can be achieved by an intelligent recommendation
system that selects and poses a few precise questions from a large database during each
development cycle, minimizing time demands on development stakeholders while obtaining
important results. To accomplish this, we have extracted the most crucial development
metrics from the literature and transformed them into questions. To each question is
assigned a weight based on its importance, and each answer is given a corresponding value.
Through this process, we have created a dynamic pool of potential questions that can be
selected using the reinforcement learning algorithm of **Contextual Multi-Armed Bandits
(CMAB)**, which serves as a recommendation system to **seven key roles** among development
stakeholders. The software implementation of this method enables not only the escalation of
the number of components under evaluation but also the continuous improvement of its
performance over time.

---

## I. Introduction

Developing software for automotive systems has become increasingly challenging due to the
rising complexity, the variety of platform configurations, and the dependencies between the
electronic and electric components of intelligent connected vehicles (ICVs) [1]. The
in-vehicle networks must be flexible, extensible, and service-oriented to ensure secure and
reliable communication [2]. The degree of complexity also increases as the development of the
back-end environment is directly interconnected to the onboard one. Furthermore, the hardware
complexity through the various generations and its corresponding capabilities demands a more
accurate validation while enabling multiple tests and validation methods. Thus, detecting
faults among the relevant components is becoming difficult, particularly during the
development phase. Fixing issues at later stages of development is widely acknowledged to
incur higher expenditures. In general, preventing software faults or detecting them early
reduces time and costs and improves the project quality. In addition, the processes have been
adjusted to enable more frequent releases with shortened timelines. The vehicle development
processes have achieved high performance and robustness. However, these processes still
require longer development cycles than the current market demands (Fig. 1). Another
characteristic of Automotive Software Development (ASD) is that the evaluation results of
each software release are only visible after the relevant testing and validation teams create
the corresponding defect tickets. This approach can be complex as the software's continuous
development receives asynchronous feedback from diverse teams.

**Fig. 1 — Product life cycle of a vehicle [16]:** shows three overlapping stages on a
timeline — *Development* (short, at the start), *Software Updates* (dashed box, overlapping
development and continuing through production), *Production* (a mid-length bar), and
*Operation & Maintenance* (the longest bar, spanning roughly 3 to 10 years).

---

## II. State of the Art

This paper covers three main research areas: fault prediction in software development,
automotive software integration, and recommendation systems with reinforcement learning.

### A. Fault Prediction Models

Several studies define metrics to prevent faults or provide early detection of them [3], [4].
As software development remains a complex activity, bugs are still delivered when a software
build is created. These bugs can be clustered into different categories according to their
causes. Fault prediction models try to minimize the fault-prone and, consequently, define
metrics for this purpose [1], [2], [5]. Many researchers have provided a group of metrics such
as the one of Chidamber and Kemerer (**CK Metrics**) [4], **MOOD** from Abreu and Carapuca
Metrics, **QMOOD** from Bansiya and Davis [6].

Moreover, **Key Performance Indicators (KPI)** provide further evidence for the developed
software. KPIs are useful for measuring the parameters of the software under evaluation. Some
examples are **Mean Time to Acknowledge (MTTA)**, **Mean Time Between Failures (MTBF)**,
**Mean Time to Repair (MTTR)**, and **First-Time Fix Rate (FTFR)** [7]. As faults affect
straightly the software quality [3], [8], applying metrics helps to provide a comprehensive
rating of the software component to prevent quality reductions. Furthermore, it is worthwhile
noting that there are a lot of approaches [9] which have been tried to find the correlation of
the performance indicators according to the productivity and robustness based on
architectural aspects of the software infrastructure [2], [9], [10], [11].

### B. Automotive Software Integration

Agile practices have been highly integrated into the automotive development processes in the
last decade. These are steadily nominated because they provide more flexibility in the
implementation plan, timelines, and deliverable features [12]. The question about how good
agile methods can be combined with the **V-model** [13] has been examined in various papers
[8], [12], [14]. On the one hand, agile methods can benefit the development team. Nevertheless,
they have to cope with heterogeneous, distributed software with strong dependencies, an
extensive portfolio of vehicle configurations, and the maintenance of legacy software
platforms and components. Hence, regression faults are possible and a complete coverage
testing approach is not feasible [8], [15]. During the development and testing phases, various
steps must be performed to successfully achieve the targets of the specification [10].
Continuous Integration and DevOps, alongside test automation in general, are elementary
milestones of the software development, integration, and testing before the software
component is tested on the final platform, the vehicle [10], [11].

The development processes for the automotive sector's Electrics and Electronic (E/E) systems
are more difficult collectively, as they combine prompt software development with more
long-term automotive processes. The most demanding part of the process is managing and
avoiding faults in a continuous development process that can accommodate the interactions
between the in-vehicle software and hardware components and the off-board cloud components
and services. Due to the heterogeneity of the components and the individual characteristics of
their development, the complexity is likewise expanded.

The proper process should cover every step from the beginning, such as the specification and
the requirements, until the final product and the acceptance criteria. Furthermore, these
processes are based on principles such as **Capability-Maturity-Model-Integration (CMMI)**
[4], [7], [17], **ASPICE** [18] and **AUTOSAR** [3] or **OSEK and HIS** [19].

The **V-model** [13] plays the most crucial role as it is the main instance of the
development, which is combined with other agile methods and adjusted accordingly to the
corresponding projects when necessary. Moreover, continuous development over the complete
V-model [9], [20] can only be achieved with great effort and costs. The processes must be
efficient and precise according to time and costs, lead to robust results, avoid overlaps
based on **LEAN principles** [21], and avoid inconsistencies. Processes are based on dynamic,
steadily changing factors; thus, they should also be appropriately revised. **ASPICE** [18]
serves as a framework for evaluating software processes' efficiency and developmental
maturity within automotive OEMs and suppliers.

### C. Recommendation Systems

This study uses a **Contextual Multi-Armed Bandits (CMAB)** algorithm to evaluate the
automotive processes. CMAB is a very efficient and simplified reinforcement learning
algorithm. An agent collects rewards while trying to alternate reasonably, according to the
algorithm and the context, to make decisions. CMABs are used in many crucial applications,
such as medicine for clinical trials [22], decision-making systems for online
recommendations, and widely for advertisements.

The main reason for selecting the CMAB is the **Partial Feedback** [23], as it is not possible
to evaluate the rewards of all possibilities an agent could have. The primary question that
the agent tries to answer with every move is when would be the appropriate moment to exploit
and when to explore. Only one action per decision could take place, and this should proceed
without knowing the result of the alternative. This is well-known to the researchers as an
**"exploration-exploitation" dilemma** [24].

Many studies have been conducted to solve the exploitation versus the exploration problem. The
most fundamental are the **Epoch-Greedy algorithm** [25], the **EXP4 algorithm**, **Linear
Upper Confidence Bound** [26], **Thompson Sampling**, and **Softmax Action Selection** [27].
These algorithms can be combined with the multi-armed bandits' algorithm with context to
provide the agent with a plethora of solutions for finding the most suitable one according to
the circumstances and the expectations. Consequently, as the agent applies exploration based
on contextual bandits, it avoids adopting the latent bias on the previous decisions. The
approach is more effective while the environment is changing.

> **Direct relevance:** this section is effectively the state-of-the-art justification for
> choosing **LinUCB** (one of the exact algorithms named here, [26]) that this thesis also
> uses — cite this paper for the broader "why CMAB, why not plain MAB" argument, and use it
> to introduce Epoch-Greedy / EXP4 / Thompson Sampling / Softmax as the alternatives your
> Ch.2.3.4 and Ch.4.9.1 sections already plan to discuss and rule out.

---

## III. Concept and Methodology

### A. Concept

All research approaches focus on specific parts of automotive development. The software
metric approaches target mainly the software itself and not so intensively the integration
levels until the final configuration, which is the vehicle. On the other hand, defined KPIs
can primarily be extracted only at later process steps. In addition, the framework of ASPICE
[18] is an essential certification for OEMs. **However, a significant drawback of ASPICE is
the lack of a direct way to assess operations post-certification and ensure stakeholder
compliance.** After the organization's certification, the monitoring is based on project
management tools or software defect-tracking systems for faults created by software releases.
These approaches limit the capabilities of continuous and clear feedback.

> **This single sentence is arguably the most citable line in the whole paper for your Ch.1
> Motivation / Ch.3 Research Gap** — it is exactly the manual-assessment pain point your
> thesis's digitization angle is built on.

This study focuses on providing early feedback and transparency regarding the status of
software releases. It introduces a **dynamic survey model using a recommendation system**,
which steadily tries to ask the right questions that can reveal a vulnerability in
development.

Regarding our method, we have developed a new framework for applying continuous evaluation to
all development stages. We evaluate each software release and the operational process steps
using metrics derived from the literature. For each evaluation, a list of score values is
calculated, indicating whether or where vulnerabilities exist in the software releases or
processes.

**Equation (1):**
```
∀R, R(SWM, PS) → v1...vi
```
- *R* represents the software release
- *SWM* is the model for the software evaluation
- *PS* are the process steps
- *v1...vi* the output values of the corresponding evaluation

These values are grouped into three categories representing different **traffic light
statuses**. Red values represent the answers where vulnerabilities have been found, yellow
for uncritical weaknesses, and green, where everything is fine. This classification helps to
visualize the results later.

**Equation (2):**
```
f(Qi) =
    green   if vi < Tmin
    yellow  if Tmin < vi < Tmax
    red     if vi > Tmax
```
- *f* is the function that calculates the score of the evaluation
- *Qi* the corresponding question
- *T* is the threshold with a minimum and a maximum value

> **Direct structural parallel to your own design:** Equation (2)'s three-band traffic-light
> classifier (green/yellow/red via `Tmin`/`Tmax`) is the two-threshold ancestor of your own
> **four-band** classifier in `Architecture.md` §5 (Compliant/Minor Weakness/Significant
> Gap/Critical Gap at 0.25/0.50/0.75 cut points). Worth an explicit comparison in Ch.4.6 or
> Ch.4.9: you refined a 3-band scheme into a 4-band one for finer-grained ASPICE capability
> reporting.

Therefore, we have developed a controller that manages the evaluation and is connected to a
Reinforcement Learning (RL) agent responsible for selecting questions from a database. The
concept architecture (Fig. 2) depicts the interactions between the stakeholders via the
Graphical User Interface, the Controller, the RL Agent, and the corresponding database. The
procedure employed for its realization is delineated below.

**Fig. 2 — Concept architecture:** a block diagram with three columns feeding a central
**GUI**: *Development Stakeholders* (people icon), *Manager* (person icon), and *Software
Versions* — all connected bidirectionally to the GUI. The GUI connects bidirectionally to a
**Model Controller** (center), which also connects to an **Evaluation Model** box below it.
The Model Controller connects bidirectionally to the **Recommendation System / RL Agent**
(dashed box, right), which exchanges *context*, *action*, *reward*, and *models* with a
**Database** below it. The Database itself is broken into four sub-components: *Q-Values*,
*Question Pool*, *Weights & Values*, *LUT (Look-Up Table)*, *Evaluation Score*, and *Context*.
A *Results* box sits above the GUI, closing the loop back to stakeholders.

After having approached the literature concerning automotive software development metrics
[1], [2], [5], automotive processes [16], [20], and development and validation standards, the
collected data were documented as metrics. Consequently, all collected metrics were
transformed into questions to identify the status of the software releases.

Furthermore, we extensively examined the various development roles of the automotive
stakeholders. After clustering them according to their significant characteristics, we
decided that **seven fundamental roles** are the most representative of the complete
development chain. Consequently, we explored their interaction and dependencies through the
development processes. Next, all collected question metrics were assigned to the
corresponding development roles according to relevance.

Each question has **two groups of assignments**. The first assigned group is the one to be
asked this question. The second group is the **"under-evaluation" development roles**, which
are affected by this question if it fails. This group of roles represents the weak spot as
they are representative stakeholders of the V-model workflow. The possible answers are
predefined and assigned values to accomplish an evaluation through the questions. **The
values increase as the question tends to fail.**

> **This is the exact inverse-reward design your `Implementation.md` documents**: "A
> high-risk answer (weight 4) gives reward 1.0... high-risk answers are most informative —
> they confirm that a real weakness exists and warrant follow-up." This paper is the direct
> conceptual source for that design choice — cite it explicitly when justifying the
> "inverse/greatest-reward-for-worst-answer" reward function in Ch.4.5.5.

The question metrics are collected into a database pool, and the CMAB algorithm selects which
question should be asked to each role every time. This approach allows stakeholders to obtain
an accurate and robust view of the current status within only a few questions. The following
steps provide more details about the evaluation process.

> **Note on the "seven fundamental roles":** this paper's seven roles are not enumerated by
> name in the extracted text (only referenced as "seven key roles" / "seven fundamental
> roles"). Your own `Architecture.md` lists exactly seven stakeholder roles: **Software
> Developer, Software Architect, Project Manager, QA Engineer, Test Engineer, Team Lead,
> ASPICE Assessor.** Given the shared authorship/supervisor, it's worth explicitly stating in
> the thesis (Ch.3.6 Research Gap, or a footnote) whether your role list was adopted
> directly from this paper or independently derived — this affects how you frame the
> contribution/novelty claim.

### B. Dataset Collection

The question-metrics dataset was gathered using **five principles**: software development
metrics, automotive software development-specific studies, ASPICE [18], ISTQB [28], and
documented OEM Electric/Electronic processes.

**1) Software development metrics:** After the collection process of the metrics, the latter
were evaluated for their relevance to automotive demands. The automotive domain has many
different and unique characteristics compared to classical software development, which limits
straightforward integration. The automotive software ecosystem is more dependable and
combines hardware development with vehicle development. These two have different
development life-cycles, making the process more complex.

**2) Automotive software development:** As stated before, the automotive development
characteristics [16], [20] were investigated, and the results are documented. All these
unique characteristics are also respectively converted into question metrics.

**3) Automotive-SPICE:** ASPICE [18] ensures software automotive systems' safety, quality, and
competitiveness. **For this study, we analyzed the System Engineering process group
SYS.1-SYS.5, SWE.1-SWE.6, VAL.1 and PIM.3** (Fig. 3).

> **Direct scope comparison:** this paper's ASPICE scope is *broader* than your thesis's
> (SYS.1–5 + SWE.1–6 + VAL.1 + PIM.3 vs. your SWE.1–6 only). This is a clean, citable basis
> for framing your thesis's **deliberately narrower scope** in Ch.1.5/Ch.3.6 — you trade
> breadth for depth: a fully implemented, single-process-group tool with a working web
> application and real question bank, versus this paper's broader-but-conceptual four-group
> coverage (the paper states training/results are still pending — see §E below).

**Fig. 3 — Automotive SPICE process groups [18]** *(a table reproduced from the ASPICE
standard, restricted to the four groups analyzed in this paper)*:

| Process Group | Processes |
|---|---|
| System Engineering Process Group (SYS) | SYS.1 Requirements Elicitation; SYS.2 System Requirements Analysis; SYS.3 System Architectural Design; SYS.4 System Integration and Integration Verification; SYS.5 System Verification |
| Software Engineering Process Group (SWE) | SWE.1 Software Requirements Analysis; SWE.2 Software Architectural Design; SWE.3 Software Detailed Design and Unit Construction; SWE.4 Software Unit Verification; SWE.5 Software Component Verification and Integration Verification; SWE.6 Software Verification |
| Validation Process Group (VAL) | VAL.1 Validation |
| Process Improvement Process Group (PIM) | PMI.3 Process Improvement *(sic in source; correct ASPICE ID is PIM.3)* |

**4) ISTQB:** The syllabus of ISTQB [28] was analyzed to extract the most crucial principles
of quality assurance and competitive advantages. The criteria that have been extracted can
ensure the qualitative and reliable results of the software evaluation.

**5) OEM defined Processes:** Finally, the official development processes of a premium OEM
were examined. These processes were well described, and it was possible to extract
considerable insights for this study. A very interesting aspect would be the comparison
between the target and the processes' actual status. This will be investigated at the real
execution of the concept.

### C. Data Processing

To connect the question metrics to the algorithm, they were further processed and evaluated
in the following aspects:

**1) Weights according to the importance:** Interviews with automotive experts were conducted
to examine the questions' importance and relevance to the processes. The experts were asked
to evaluate the questions based on their knowledge and experience. This procedure helped to
collect essential information and feedback according to the criteria and required connecting
the questions with the derived weights based on relevance and significance. **The
interrelated weights of the questions play an essential role in the CMAB agent's rewards.**

> **Methodological note relevant to your Ch.5.4 (Question Bank Design):** this paper derived
> its question *weights* from **expert interviews** — a validation step your own thesis's
> question bank (42 questions, weights 0–4 per option) does not document having performed.
> If your weights were assigned by you/your supervisor rather than through an expert
> elicitation process, that is worth naming explicitly as a **limitation** in Ch.7.6/Ch.8.3,
> with this paper cited as the methodological benchmark for how weight assignment *should*
> ideally be validated (cf. also your existing Ch.8.4.4 future-work item on
> "Expert/Assessor-Validated Reward Signal").

**2) Answers with different values:** After evaluating the questions, the answers were
provided as predefined and linked to a specific value. **Each question has four possible
answers and one free text field.** The four values are associated and sorted from the worst
possible answer to the best one. Through this correlation, it is considered that the worst
answer means that there is a problem or that it is not meeting the requirements of the
development process. Hence, the CMAB agent looks into this while exploring the database. A
high-level view of the evaluation packets exchanged between the database, the model
controller, and the database is depicted in Fig. 4.

> **Structural difference worth naming:** this paper uses **4 predefined answers + 1 free
> text field** per question; your tool uses **5 predefined answers (A–E, weights 0–4)** with
> no free-text option. Both are valid design choices — cite this contrast in Ch.4.9 if
> discussing why a purely quantitative 5-point scale (no free text to parse) was chosen for
> a tractable, fully-automatable reward signal.

**Fig. 4 — Structure of an evaluation packet:** a row of connected boxes: *Question ID* →
*Roles to be asked* → *Question-Weight* → *Question-Payload* → *Answer Payloads* → *Values of
Answers* → *Targets of Question* → *(dashed) Given Answer*.

### D. Reinforcement Learning Framework

This study proposes a new approach to pinpoint software development weaknesses leading to
software faults. The concept is necessary for a decision-making and recommendation system
**with inverse functionality**. In this approach, the greatest reward is associated with
questions that could have the **"worst" possible answers** and are labeled with the highest
values. Consequently, **the agent seeks out questions prone to failure.**

The motivation behind the selection of the CMAB is the summary of the approach's
characteristics combined with the advantages provided by this algorithm. **Partial Feedback**
[13, *sic — likely meant to cite [23]*] is a limiting factor, as the agent cannot be aware of
the answers and rewards of the other questions when it selects one. As long as a question
once posed receives Feedback from the corresponding role, the agent cannot retract it to
attempt another. Moreover, as new software releases are evaluated over time, the environment
and faults remain unchanged. Thus, selecting the following question can only sometimes be
based on history. Therefore, the CMAB agent must balance between exploiting and exploring. In
addition, **each development role is aligned with a distinct context, reflecting its unique
expertise and knowledge field.** The corresponding workflow of the CMAB algorithm is shown in
Fig. 5.

> **Direct parallel:** "each development role is aligned with a distinct context" is
> conceptually identical to your own **one-hot role encoding** in the 23-dimensional context
> vector (`role_software_developer, role_software_architect, ...` — dims 0–6 in
> `Implementation.md` §2.3). Cite this paper as prior justification for role-as-context.

**Fig. 5 — Contextual Multi-Armed Bandits workflow [23]:** a cyclic block diagram. A *Web
Based Interface* box on the left exchanges *context* (incoming) and *action* / *reward*
(outgoing) with an *Explore* box. *Explore* passes *context* and *data* into a *Join Service*
box below it. *Join Service* passes *data* to a *Learn Online* box, which produces *models*
that feed a *Deploy* box, which feeds back *models* into *Explore*, closing the loop. A
*Context / Feature* box beneath *Join Service* supplies context data into the pipeline. (This
is a standard **online contextual-bandit serving loop**: explore → log context+action+reward
→ learn a new model online → deploy the updated model → explore again.)

### E. Model Training

As the software releases can be considered individual and everyone's findings can be assumed
to be unique, there is no better way to train our model than to **train it live**. This CMAB
algorithm allows the agent to explore a lot before he starts exploiting, as the complete pool
of questions can be selected at least once. Though, the model is trained with **simulated
answers on virtual issues of hypothetical software releases** so that the algorithm's
performance can be sensed. **As the approach is still in the concept phase, the training will
occur later, and the results will be published.**

> **Critical status note for your Ch.3 (State of the Art) framing:** at the time of this
> paper's publication, the authors explicitly state their model has **not yet been trained
> or evaluated on real data** — only simulated/hypothetical data, with real results deferred
> to a *future paper*. This is important for your thesis's positioning: if no follow-up
> publication with real results exists yet (worth a literature search to confirm), your
> thesis is likely **the first fully implemented, end-to-end, and — per your own
> Ch.6–7 methodology — pilot-tested realization of this class of approach**, which is a
> legitimate and citable contribution claim for Ch.1.4 (Contributions) / Ch.3.6 (Research
> Gap): "prior work in this space [cite this paper] proposed the concept but deferred
> real-world training/evaluation to future work; this thesis delivers a working
> implementation with real pilot-session data."

### F. Graphical User Interface

We developed a **web-based Graphic User Interface (GUI)** connected to the SQL databases for
this concept. The GUI is designed to be used from every device and is as straightforward as
possible so that feedback is received without any barriers.

> Your own stack (React + TanStack Router, responsive, PostgreSQL via SQLModel) satisfies
> this same requirement — a legitimate one-line comparison point for Ch.4.8/Ch.5.3.

---

## IV. Conclusion

This paper introduced a novel approach for evaluating software releases based on the software
quality and the software across the development processes. After a broad literature review of
automotive software metrics regarding quality and processes, our model uses a recommendation
system that selects questions derived from metrics and asks them to the major development
stakeholders. The system intelligently and accurately selects only a few questions from
hundreds, ensuring it is not time-consuming for the development stakeholders. The evaluation's
outputs refer to weaknesses in software development and can be used to enhance the
development chain. It helps to avoid reproducible faults based on operation and improves
established processes. Moreover, it could reduce time and costs as the output is not based on
created defect tickets but on precise metrics extracted in real time. **A future paper will
provide the results after implementing and testing the model in real scenarios.**

---

## References (full list — candidates for reuse in the thesis bibliography)

`[1]` Y. Zhang, T. Liu, H. Zhao, and C. Ma, "Risk analysis of can bus and ethernet
communication security for intelligent connected vehicles," in *2021 IEEE International
Conference on Artificial Intelligence and Industrial Design (AIID)*, 2021, pp. 291–295.

`[2]` W. Zhou and Z. Li, "Implementation and evaluation of smt-based real-time communication
scheduling for ieee 802.1qbv in next-generation in-vehicle network," in *2020 2nd
International Conference on Information Technology and Computer Application (ITCA)*, 2020,
pp. 457–461.

`[3]` Z. H. Martinez, P. M. Moreno, J. A. Vergara Camacho, and G. C. Vega, "Study on the use of
defect metrics in the software development process. flaws and vulnerabilities," in *2023 IEEE
International Conference on Engineering Veracruz (ICEV)*, 2023, pp. 1–7.

`[4]` T. B. Alakus, R. Das, and I. Turkoglu, "An overview of quality metrics used in
estimating software faults," in *2019 International Artificial Intelligence and Data
Processing Symposium (IDAP)*, 2019, pp. 1–6.

`[5]` N. Jayalakshmi and N. Satheesh, "Software quality assessment in object based
architecture," *International Journal of Computer Science and Mobile Computing*, vol. 3, no.
3, pp. 941–946, 2014.

`[6]` J. Bansiya and C. G. Davis, "A hierarchical model for object-oriented design quality
assessment," *IEEE Transactions on software engineering*, vol. 28, no. 1, pp. 4–17, 2002.

`[7]` P. Alavian, Y. Eun, K. Liu, S. M. Meerkov, and L. Zhang, "The (α, β)-precise estimates of
mtbf and mttr: Definition, calculation, and observation time," *IEEE Transactions on
Automation Science and Engineering*, vol. 18, no. 3, pp. 1469–1477, 2020.

`[8]` A. Haghighatkhah, M. Oivo, A. Banijamali, and P. Kuvaja, "Improving the state of
automotive software engineering," *IEEE Software*, vol. 34, no. 5, pp. 82–86, 2017.

`[9]` S. d. S. Amorim, J. D. McGregor, E. S. de Almeida, and C. v. F. G. Chavez, "Software
ecosystems' architectural health: Another view," in *2017 IEEE/ACM Joint 5th International
Workshop on Software Engineering for Systems-of-Systems and 11th Workshop on Distributed
Software Development, Software Ecosystems and Systems-of-Systems (JSOS)*, 2017, pp. 66–69.

`[10]` K. Sneha and G. M. Malle, "Research on software testing techniques and software
automation testing tools," in *2017 International Conference on Energy, Communication, Data
Analytics and Soft Computing (ICECDS)*, 2017, pp. 77–81.

`[11]` A. C. Chagas, D. Gonzaga, L. Albuquerque, F. Oliveira, R. Castro, and L. Chaves, "Bsa
tool: An experience report of software automation to perform sanity tests in a global
software development environment," in *2023 3rd International Conference on Information
Communication and Software Engineering (ICICSE)*, 2023, pp. 15–20.

`[12]` S. K. Anjum and C. Wolff, "Integration of agile methods in automotive software
development processes," in *2020 IEEE 3rd International Conference and Workshop in Óbuda on
Electrical and Power Engineering (CANDO-EPE)*, 2020, pp. 000151–000154.

`[13]` "V-modell xt bund." [Online]. Available: https://www.cio.bund.de/

`[14]` M. Schmidtner, H. Timinger, M. Blust, C. Doering, and D. Hilpoltsteiner, "Towards an
adaptive reference model for agile and hybrid frameworks in automotive development," in *2020
IEEE International Conference on Engineering, Technology and Innovation (ICE/ITMC)*, 2020,
pp. 1–10.

`[15]` S. K. Anjum and C. Wolff, "Agile principles in automotive software development:
Analysis of potential levers," in *2021 IEEE European Technology and Engineering Management
Summit (E-TEMS)*, 2021, pp. 141–147.

`[16]` J. Schäuffele and T. Zurawka, *Automotive Software Engineering*. Springer Fachmedien
Wiesbaden, 2016. [Online]. Available: http://dx.doi.org/10.1007/978-3-658-11815-0

`[17]` Y. Jiang, J. Lin, B. Cukic, S. Lin, and Z. Hu, "Replacing code metrics in software fault
prediction with early life cycle metrics," in *2013 IEEE Third International Conference on
Information Science and Technology (ICIST)*. IEEE, 2013, pp. 516–523.

`[18]` "Automotive-spice." [Online]. Available: https://vda-qmc.de/en/automotive-spice/

`[19]` M. Homann, *OSEK: Betriebssystem-Standard für Automotive und Embedded Systems*.
mitp-Verlag, 2005.

`[20]` *Automotive Systems and Software Engineering: State of the Art and Future Trends*.
Springer International Publishing, 2019. [Online]. Available:
http://dx.doi.org/10.1007/978-3-030-12157-0

`[21]` B. Blau and T. Hildenbrand, "Product line engineering in large-scale lean and agile
software product development environments - towards a hybrid approach to decentral control
and managed reuse," in *2011 Sixth International Conference on Availability, Reliability and
Security*, 2011, pp. 404–408.

`[22]` A. Agarwal, D. Hsu, S. Kale, J. Langford, L. Li, and R. E. Schapire, "Taming the
monster: A fast and simple algorithm for contextual bandits," 2014.

`[23]` A. Agarwal, S. Bird, M. Cozowicz, L. Hoang, J. Langford, S. Lee, J. Li, D. Melamed, G.
Oshri, O. Ribas, S. Sen, and A. Slivkins, "Making contextual decisions with low technical
debt," 2016.

`[24]` M. Naeem, S. T. H. Rizvi, and A. Coronato, "A gentle introduction to reinforcement
learning and its application in different fields," *IEEE access*, vol. 8, pp. 209320–209344,
2020.

`[25]` S. Shahrampour, A. Rakhlin, and A. Jadbabaie, "Multi-armed bandits in multi-agent
networks," in *2017 IEEE International Conference on Acoustics, Speech and Signal Processing
(ICASSP)*, 2017, pp. 2786–2790.

`[26]` N. Gutowski, T. Amghar, O. Camp, and F. Chhel, "Context enhancement for linear
contextual multi-armed bandits," in *2018 IEEE 30th International Conference on Tools with
Artificial Intelligence (ICTAI)*, 2018, pp. 1048–1055.

`[27]` M. Tokic and G. Palm, "Value-difference based exploration: adaptive control between
epsilon-greedy and softmax," in *Annual conference on artificial intelligence*. Springer,
2011, pp. 335–346.

`[28]` "International software testing qualifications board." [Online]. Available:
https://www.istqb.org/

---

## Quick-reference: which references map to which of your thesis chapters

| Refs | Topic | Likely thesis home |
|---|---|---|
| [1], [2] | ICV / in-vehicle network complexity | Ch.1.1/1.2 (Motivation) |
| [3], [4], [5], [6], [17] | Fault prediction models, CK/MOOD/QMOOD metrics, code metrics | Ch.3 (State of the Art) — contrast against your ASPICE-BP-based question design |
| [7] | MTTA/MTBF/MTTR/FTFR KPI definitions | Ch.3 (State of the Art), possibly Ch.2 background on metrics |
| [8], [12], [14], [15] | Agile + V-model integration in automotive | Ch.2.1.4 (Traditional manual assessment) / Ch.3 |
| [9], [10], [11] | Software ecosystem architecture health, test automation tooling | Ch.3 (peripheral) |
| [13] | V-Modell XT (German federal V-model standard) | Ch.2.1 background on lifecycle models |
| [16], [20] | Automotive Software Engineering (Schäuffele & Zurawka) — likely THE core automotive SE textbook | Ch.2 background, cite heavily |
| [18] | Automotive SPICE (VDA QMC) | Ch.2.1, throughout — same as your `Automotive-SPICE-PAM-v40.pdf` source |
| [19] | OSEK/HIS embedded OS standard | peripheral, likely skip |
| [21] | LEAN principles | Ch.2 background (peripheral) |
| [22] | Contextual bandits for clinical trials (Agarwal et al.) | Ch.2.3 (MAB background), example application domain |
| [23] | "Making contextual decisions with low technical debt" (Agarwal et al., Microsoft) — Fig. 5 workflow source | Ch.2.3.2/2.3.3 — likely your best citation for the online-serving-loop diagram |
| [24] | RL gentle introduction survey | Ch.2.3.1 (exploration-exploitation) |
| [25] | Multi-armed bandits in multi-agent networks (Epoch-Greedy context) | Ch.2.3.4 (alternative algorithms) |
| [26] | Context enhancement for **linear contextual MAB** — closest citation to LinUCB itself | Ch.2.3.3 (LinUCB foundations) — important |
| [27] | Softmax / epsilon-greedy exploration | Ch.2.3.4 (alternative algorithms) |
| [28] | ISTQB | Ch.3 (state of the art), if discussing QA/testing-certification standards alongside ASPICE |

**Note:** none of these references is yet in your `bibliography.bib` — cross-check against it
before the next writing session and add the ones you decide to cite.
