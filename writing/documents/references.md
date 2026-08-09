# Thesis Reference Collection

> Working list of references to cite in the thesis, gathered from: (1) the two supervisor
> papers already summarized in `supervisor_research_paper_new_approach_early_detection_vulnerabilities.md`
> and `supervisor_research_paper_recommender_systems_fault_rates.md`, (2) your own pre-picked
> list of 10, and (3) official standards/organization sources (VDA QMC, ISTQB, AUTOSAR,
> ISO/IEC). **~44 references**, grouped by topic and mapped to the chapter/section where each
> is most likely to be cited, with a one-line note on *how* to use it.
>
> **Status:** none of these are in `writing/bibliography.bib` yet (it currently only has the
> template's placeholder entries). Once you've reviewed/trimmed this list, the next step is
> converting the kept entries into real `.bib` entries with the citation keys suggested below
> (`@article{key, ...}`, `@inproceedings{key, ...}`, etc.) — ask me to do that batch
> conversion when ready.
>
> **Legend:** ✅ = from your pre-picked list of 10 · 🔵 = from the 2024 supervisor paper ·
> 🟣 = from the 2025 supervisor paper · 🌐 = official standard/organization source (not from
> either paper).

---

## A. ASPICE, Standards & Certification (Ch.2.1 Background, throughout)

**1.** ✅🌐 **VDA QMC**, *Automotive SPICE® Process Assessment Model (PAM), Version 4.0*.
Verband der Automobilindustrie (VDA) Quality Management Center, Germany, 2023.
Key: `vdaqmc2023pam`
→ **Use:** your primary standard citation, throughout — this is the same document already
distilled in `aspice.md`. Cite directly whenever quoting PAM definitions, BP text, capability
levels, or the measurement framework.

**2.** ✅ C. Murphy, "Automotive SPICE: 0-60 in No Time Flat," *IEEE Engineering Management
Review*, vol. 47, no. 2, pp. 26–28.
Key: `murphy_aspice_0to60`
→ **Use:** Ch.2.1/Ch.3 — a short, accessible IEEE-published primer on what ASPICE is and why
it matters industrially; good as an easy-to-read companion citation alongside the dense PAM
standard itself, e.g., in your opening paragraph introducing ASPICE.

**3.** 🌐 ISO/IEC 33001:2015, *Information technology — Process assessment — Concepts and
terminology*. ISO/IEC, 2015.
Key: `iso33001_2015`
→ **Use:** Ch.2.1.1/Ch.4 — cite when defining "information item," "process attribute," or
other PAM terminology sourced from this standard (per `aspice.md` §2/§5.1, the PAM explicitly
adopts these definitions from ISO/IEC 33001).

**4.** 🌐 ISO/IEC 33020:2019, *Information technology — Process assessment — Process
measurement framework for assessment of process capability*. ISO/IEC, 2019.
Key: `iso33020_2019`
→ **Use:** Ch.2.1.3/Ch.4.6 — cite when explaining the rating scale (N/P/L/F), process
attributes, or capability level model — the PAM measurement framework is explicitly "an
adaption of ISO/IEC 33020:2019" (`aspice.md` §4).

**5.** 🌐 ISO 26262:2018, *Road vehicles — Functional safety*, 2nd ed. ISO, 2018.
Key: `iso26262_2018`
→ **Use:** Ch.2.1 (peripheral) — only needed if you discuss functional safety alongside
process capability (the PAM's own Annex D lists this as a reference standard); optional,
include only if Ch.2 draws a safety/process-capability distinction.

**6.** 🌐 VDA QMC / Automotive SPICE, official website. [Online]. Available:
https://vda-qmc.de/en/automotive-spice/
Key: `vdaqmc_website`
→ **Use:** Ch.2.1/Ch.3 — cite for the *organizational* fact of ASPICE's existence/maintenance
body (both supervisor papers cite this exact URL as their ASPICE reference — see ref. [18] in
the 2024 paper / ref. [16] in the 2025 paper).

**7.** 🌐 AUTOSAR, official website. [Online]. Available: https://www.autosar.org/
Key: `autosar_website`
→ **Use:** Ch.2/Ch.3 (peripheral) — only if you mention AUTOSAR alongside ASPICE as a
standards-landscape contrast (both supervisor papers do this in their State-of-the-Art
sections).

**8.** 🌐 ISTQB (International Software Testing Qualifications Board), official website /
syllabus. [Online]. Available: https://www.istqb.org/
Key: `istqb_website`
→ **Use:** Ch.3 (State of the Art) — if you discuss testing/QA certification standards
alongside ASPICE, as both supervisor papers do (ref. [28] in 2024 paper / ref. [17] in 2025
paper).

---

## B. Automotive Software Engineering & Motivation Background (Ch.1.1/1.2, Ch.2)

**9.** 🔵🟣 J. Schäuffele and T. Zurawka, *Automotive Software Engineering*. Springer
Fachmedien Wiesbaden, 2016. DOI: 10.1007/978-3-658-11815-0.
Key: `schauffele2016automotive`
→ **Use:** Ch.2 background, cite heavily — this is the core automotive-SE textbook cited by
*both* supervisor papers (2024 ref. [16], 2025 ref. [29]) and is the source of the "product
life cycle of a vehicle" and "bug finding and fixing in relation to time" figures reproduced
in those papers' Fig. 1. Strongly recommended for your own Ch.1.1/Ch.2.1.4 defect-cost-curve
argument.

**10.** 🔵 *Automotive Systems and Software Engineering: State of the Art and Future Trends*.
Springer International Publishing, 2019. DOI: 10.1007/978-3-030-12157-0.
Key: `springer2019automotive_systems`
→ **Use:** Ch.2 background — companion citation to [9] above for broader automotive systems
engineering context, cited by the 2024 paper.

**11.** ✅🔵 Y. Zhang, T. Liu, H. Zhao, and C. Ma, "Risk analysis of can bus and ethernet
communication security for intelligent connected vehicles," in *2021 IEEE Int. Conf. on
Artificial Intelligence and Industrial Design (AIID)*, 2021, pp. 291–295.
Key: `zhang2021canbus`
→ **Use:** Ch.1.1 (Motivation) — supports the "rising complexity of ICVs" opening argument;
cited first by both you and the 2024 paper.

**12.** 🟣 M. L. Sichitiu and M. Kihl, "Inter-vehicle communication systems: a survey," *IEEE
Communications Surveys & Tutorials*, vol. 10, no. 2, pp. 88–105, 2008.
Key: `sichitiu2008intervehicle`
→ **Use:** Ch.1.1 — the inter-vehicle-network half of the complexity argument (paired with
[13] for intra-vehicle).

**13.** 🟣 S. Tuohy, M. Glavin, C. Hughes, E. Jones, M. Trivedi, and L. Kilmartin,
"Intra-vehicle networks: A review," *IEEE Trans. on Intelligent Transportation Systems*, vol.
16, no. 2, pp. 534–545, 2014.
Key: `tuohy2014intravehicle`
→ **Use:** Ch.1.1 — the onboard-communication half of the complexity argument.

**14.** 🟣 S. Fürst, "Challenges in the design of automotive software," in *2010 Design,
Automation & Test in Europe Conference & Exhibition (DATE 2010)*, IEEE, 2010, pp. 256–258.
Key: `furst2010challenges`
→ **Use:** Ch.1.1/Ch.2 — short, citable statement of automotive software design challenges;
good for an opening-paragraph citation cluster.

**15.** 🟣 A. Iwai and M. Aoyama, "Automotive cloud service systems based on service-oriented
architecture and its evaluation," in *2011 IEEE 4th Int. Conf. on Cloud Computing*, IEEE,
2011, pp. 638–645.
Key: `iwai2011automotivecloud`
→ **Use:** Ch.1.1 — supports the "back-end/cloud interconnection increases complexity" point.

**16.** 🔵 W. Zhou and Z. Li, "Implementation and evaluation of smt-based real-time
communication scheduling for ieee 802.1qbv in next-generation in-vehicle network," in *2020
2nd Int. Conf. on Information Technology and Computer Application (ITCA)*, 2020, pp. 457–461.
Key: `zhou2020smtscheduling`
→ **Use:** Ch.1.1 (peripheral) — supports the in-vehicle-network reliability/flexibility
point; optional if you want a denser motivation section.

---

## C. Software Metrics & Fault Prediction (Ch.3, contrast against your ASPICE-BP-based questions)

**17.** ✅🔵🟣 Z. H. Martinez, P. M. Moreno, J. A. Vergara Camacho, and G. C. Vega, "Study on
the use of defect metrics in the software development process. flaws and vulnerabilities," in
*2023 IEEE Int. Conf. on Engineering Veracruz (ICEV)*, 2023, pp. 1–7.
Key: `martinez2023defectmetrics`
→ **Use:** Ch.3 (State of the Art) — cited by you and both supervisor papers; use for the
"metrics prevent/detect faults" opening claim of your related-work section.

**18.** ✅🔵🟣 T. B. Alakus, R. Das, and I. Turkoglu, "An overview of quality metrics used in
estimating software faults," in *2019 Int. Artificial Intelligence and Data Processing
Symposium (IDAP)*, 2019, pp. 1–6.
Key: `alakus2019qualitymetrics`
→ **Use:** Ch.3 — companion citation to [17], same context.

**19.** ✅🔵 Y. Jiang, J. Lin, B. Cukic, S. Lin, and Z. Hu, "Replacing code metrics in software
fault prediction with early life cycle metrics," in *2013 IEEE Third Int. Conf. on Information
Science and Technology (ICIST)*, IEEE, 2013, pp. 516–523.
Key: `jiang2013earlylifecycle`
→ **Use:** Ch.3/Ch.1.2 (Motivation) — directly supports "early detection reduces cost" and
"early life-cycle metrics matter more than late-stage code metrics," which is close to your
own thesis's motivation for adaptive, session-based questioning rather than end-of-cycle
review.

**20.** 🔵🟣 J. Bansiya and C. G. Davis, "A hierarchical model for object-oriented design
quality assessment," *IEEE Trans. on Software Engineering*, vol. 28, no. 1, pp. 4–17, 2002.
Key: `bansiya2002qmood`
→ **Use:** Ch.3 — the QMOOD metric suite; part of the classic CK/MOOD/QMOOD trio contrasted
against ASPICE-BP-derived questions in your Ch.3.4 (Cross-Comparison of Approaches).

**21.** 🟣 S. R. Chidamber, D. P. Darcy, and C. F. Kemerer, "Managerial use of metrics for
object-oriented software: An exploratory analysis," *IEEE Trans. on Software Engineering*,
vol. 24, no. 8, pp. 629–639, 2002.
Key: `chidamber2002ckmetrics`
→ **Use:** Ch.3 — the CK metrics origin paper; second of the classic trio.

**22.** 🟣 R. Harrison, S. J. Counsell, and R. V. Nithi, "An evaluation of the mood set of
object-oriented software metrics," *IEEE Trans. on Software Engineering*, vol. 24, no. 6, pp.
491–496, 1998.
Key: `harrison1998mood`
→ **Use:** Ch.3 — third of the classic trio (MOOD).

**23.** 🟣 M. Shepperd and D. Ince, *Derivation and validation of software metrics*. Oxford
University Press, 1993.
Key: `shepperd1993derivation`
→ **Use:** Ch.3 — foundational methodology reference for *how* software metrics should be
validated; useful if you discuss the (documented) lack of expert-validated weights in your own
question bank as a limitation (cf. the callout in the 2025-paper `.md` file §III.C.1).

**24.** 🟣 N. F. Schneidewind, "Methodology for validating software metrics," 1992.
Key: `schneidewind1992methodology`
→ **Use:** Ch.3 — companion citation to [23].

**25.** 🟣 S. Pandey, R. Mishra, and A. Tripathi, "Machine learning based methods for software
fault prediction: A survey," *Expert Systems with Applications*, vol. 172, p. 114605, 2021.
Key: `pandey2021mlsurvey`
→ **Use:** Ch.3 (State of the Art) / Ch.4.9.4 — position your **rule-based weakness
classifier** as a deliberate MVP choice against the ML/DL-based fault-prediction literature
surveyed here; directly supports the argument already made in `Architecture.md` §8 ("Why
weighted scoring for the classifier rather than a trained ML model?").

**26.** 🟣 I. Batool and T. A. Khan, "Software fault prediction using data mining, machine
learning and deep learning techniques: A systematic literature review," *Computers &
Electrical Engineering*, vol. 99, p. 107739, 2022.
Key: `batool2022sfpreview`
→ **Use:** Ch.3 — companion survey citation to [25], same argument.

**27.** 🟣 V. Suma and T. Nair, "Defect management strategies in software development," *arXiv
preprint* arXiv:1209.5573, 2012.
Key: `suma2012defectmanagement`
→ **Use:** Ch.2/Ch.3 — supports the "defects are cheaper to fix early" framing alongside the
Fig. 1 bug-cost-curve reproduced in the 2025 paper's `.md` summary.

**28.** 🟣 I. A. Memon, Q. B. Jamali, A. S. Jamali, M. K. Abbasi, N. A. Jamali, and Z. H.
Jamali, "Defect reduction with the use of seven quality control tools for productivity
improvement at an automobile company," *Engineering, Technology & Applied Science Research*,
vol. 9, no. 2, pp. 4044–4047, 2019.
Key: `memon2019sevenqctools`
→ **Use:** Ch.2/Ch.3 (peripheral) — an automotive-specific defect-reduction case study; useful
if you want an industry example rather than only academic literature.

**29.** ✅🔵 A. Haghighatkhah, M. Oivo, A. Banijamali, and P. Kuvaja, "Improving the state of
automotive software engineering," *IEEE Software*, vol. 34, no. 5, pp. 82–86, 2017.
Key: `haghighatkhah2017improving`
→ **Use:** Ch.2.1.4/Ch.3 — supports both the "agile+V-model tension" and "automotive SE needs
improvement" arguments; cited by you and the 2024 paper.

---

## D. Recommender Systems — General (Ch.2.2 Background)

**30.** 🟣 L. Lü, M. Medo, C. H. Yeung, Y.-C. Zhang, Z.-K. Zhang, and T. Zhou, "Recommender
systems," *Physics Reports*, vol. 519, no. 1, pp. 1–49, 2012.
Key: `lu2012recommendersystems`
→ **Use:** Ch.2.2 (Recommender Systems Fundamentals) — a broad, highly-cited RS survey; good
as your general opening citation before narrowing to contextual bandits specifically.

**31.** 🟣 R. Bader, "Proactive recommender systems in automotive scenarios," Ph.D.
dissertation, Technische Universität München, 2013.
Key: `bader2013proactive`
→ **Use:** Ch.3 (State of the Art) — **the closest full-length prior work on
recommender-systems-in-automotive specifically** found in either supervisor paper's reference
list; worth reading the actual dissertation (not just this citation) since it may be the
single most important piece of prior art for your Ch.3.5/3.6 (Cross-Comparison / Research Gap)
sections.

**32.** 🟣 K. Rama, P. Kumar, and B. Bhasker, "Deep learning to address candidate generation
and cold start challenges in recommender systems: A research survey," *arXiv preprint*
arXiv:1907.08674, 2019.
Key: `rama2019coldstart`
→ **Use:** Ch.2.2/Ch.7.6 — cite for the **cold start** problem definition (your CMAB engine's
`A = I`, `b = 0` initialization is a direct cold-start mitigation, per `Implementation.md`
§2.2).

**33.** 🟣 S.-M. Choi, D. Lee, K. Jang, C. Park, and S. Lee, "Improving data sparsity in
recommender systems using matrix regeneration with item features," *Mathematics*, vol. 11,
no. 2, p. 292, 2023.
Key: `choi2023sparsity`
→ **Use:** Ch.2.2/Ch.7.6 — cite for the **data sparsity** problem definition.

**34.** 🟣 Y. Bechavod, K. Ligett, A. Roth, B. Waggoner, and S. Z. Wu, "Equal opportunity in
online classification with partial feedback," *Advances in Neural Information Processing
Systems*, vol. 32, 2019.
Key: `bechavod2019partialfeedback`
→ **Use:** Ch.2.2/Ch.2.3.1 — cite for the **partial feedback** problem definition, which is
the core justification for choosing a bandit approach over a supervised classifier (each
session only observes the reward for the one question actually asked).

---

## E. Multi-Armed Bandits, Contextual Bandits & Reinforcement Learning (Ch.2.3 — core algorithmic background)

**35.** ✅ L. Li, W. Chu, J. Langford, and R. E. Schapire, "A contextual-bandit approach to
personalized news article recommendation," in *Proc. 19th Int. Conf. on World Wide Web
(WWW)*, 2010, pp. 661–670.
Key: `li2010contextual`
→ **Use:** Ch.2.3.3 (LinUCB — Mathematical Foundations) — **the seminal LinUCB paper**; this
is arguably your single most important algorithmic citation in the entire thesis. Cite this
as the origin of the LinUCB algorithm your CMAB engine implements.

**36.** 🟣 K.-H. Huang and H.-T. Lin, "Linear upper confidence bound algorithm for contextual
bandit problem with piled rewards," in *Pacific-Asia Conf. on Knowledge Discovery and Data
Mining*, Springer, 2016, pp. 143–155.
Key: `huang2016linucb`
→ **Use:** Ch.2.3.3 — secondary/companion LinUCB citation (used by the 2025 supervisor paper
as their primary LinUCB reference).

**37.** 🔵 N. Gutowski, T. Amghar, O. Camp, and F. Chhel, "Context enhancement for linear
contextual multi-armed bandits," in *2018 IEEE 30th Int. Conf. on Tools with Artificial
Intelligence (ICTAI)*, 2018, pp. 1048–1055.
Key: `gutowski2018contextenhancement`
→ **Use:** Ch.2.3.3 — third LinUCB-adjacent citation (used by the 2024 supervisor paper);
useful if discussing context-vector design choices specifically (relevant to your own
23-dimensional context vector design in Ch.4.5.2).

**38.** ✅🔵 M. Naeem, S. T. H. Rizvi, and A. Coronato, "A gentle introduction to reinforcement
learning and its application in different fields," *IEEE Access*, vol. 8, pp. 209320–209344,
2020.
Key: `naeem2020gentleintro`
→ **Use:** Ch.2.3.1 (Exploration-Exploitation) — a broad, accessible RL survey; good as your
opening citation for Ch.2.3 before narrowing into bandits specifically.

**39.** 🔵 J. Langford and T. Zhang, "The epoch-greedy algorithm for contextual multi-armed
bandits," *Advances in Neural Information Processing Systems*, vol. 20, no. 1, pp. 96–1, 2007.
Key: `langford2007epochgreedy`
→ **Use:** Ch.2.3.4 (Alternative Algorithms) — the Epoch-Greedy algorithm, one of the
alternatives to LinUCB discussed/ruled out.

**40.** 🟣 S. Agrawal and N. Goyal, "Thompson sampling for contextual bandits with linear
payoffs," in *International Conf. on Machine Learning*, PMLR, 2013, pp. 127–135.
Key: `agrawal2013thompson`
→ **Use:** Ch.2.3.4/Ch.4.9.1 (LinUCB vs. Thompson Sampling) — the seminal contextual Thompson
Sampling paper; directly relevant since the 2025 supervisor paper found Thompson Sampling
competitive with/better than LinUCB in some scenarios (see Table I in that paper's summary).

**41.** 🔵 M. Tokic and G. Palm, "Value-difference based exploration: adaptive control between
epsilon-greedy and softmax," in *Annual Conf. on Artificial Intelligence*, Springer, 2011, pp.
335–346.
Key: `tokic2011valuedifference`
→ **Use:** Ch.2.3.4 — Softmax/epsilon-greedy exploration; relevant since e-Greedy was the
*best-performing* algorithm in the 2025 supervisor paper's results — worth explaining what
e-Greedy actually is via this citation even though your own thesis uses LinUCB.

**42.** ✅ S. Zhong, W. Ying, X. Chen, and Q. Fu, "An Adaptive Similarity-Measuring-Based CMAB
Model for Recommendation System," *IEEE Access*, vol. 8, pp. 42550–42561, 2020.
Key: `zhong2020adaptivecmab`
→ **Use:** Ch.2.2/Ch.3 — a concrete CMAB-based recommender-system application outside
automotive; good evidence for the "CMAB is used across many application domains" claim
(alongside the clinical-trials and advertising examples both supervisor papers mention).

**43.** 🔵 A. Agarwal, D. Hsu, S. Kale, J. Langford, L. Li, and R. E. Schapire, "Taming the
monster: A fast and simple algorithm for contextual bandits," 2014.
Key: `agarwal2014taming`
→ **Use:** Ch.2.3 (peripheral/optional) — algorithmic contextual-bandit reference cited by the
2024 supervisor paper for the clinical-trials application example.

**44.** 🔵 A. Agarwal, S. Bird, M. Cozowicz, L. Hoang, J. Langford, S. Lee, J. Li, D. Melamed,
G. Oshri, O. Ribas, S. Sen, and A. Slivkins, "Making contextual decisions with low technical
debt," 2016.
Key: `agarwal2016lowtechnicaldebt`
→ **Use:** Ch.2.3.2 (Contextual Bandits) — this is the **source of the "explore → join
service → learn online → deploy" workflow diagram** (Fig. 5) reproduced in the 2024 supervisor
paper; strongly recommended if you draw or discuss the online-serving-loop architecture of
your own CMAB engine.

---

## Notes on scope decisions

- **Deliberately excluded** narrow SFP-technique papers (RNN ensembles, whale optimization,
  diversity-aware imbalance learning, ANN-based defect prediction surveys) that appeared in the
  2025 paper's State-of-the-Art §C — these are one level deeper into a tangential subfield
  (ML-based software fault prediction) than this thesis needs; [25]/[26] above already give
  you a representative pair of survey citations for that literature if a reviewer expects to
  see it acknowledged.
- **Deliberately excluded** peripheral automotive-standards/tooling papers (OSEK/HIS, AUTOSAR
  case studies, BSA test-automation tool report, software-ecosystem architectural health,
  LEAN product-line engineering) — kept the *concept* citations (AUTOSAR website, V-Model
  background) but dropped the narrower application papers.
- **Not yet added:** classic bandit-theory foundations not cited by either supervisor paper
  but extremely standard in the field — e.g., Auer et al. (2002) "Using Confidence Bounds for
  Exploitation-Exploration Trade-offs" (the original UCB1 paper) and Sutton & Barto's
  *Reinforcement Learning: An Introduction* textbook. Neither was in your brief's source pool
  (papers + standards sites), so they're flagged here rather than silently added — worth
  considering for Ch.2.3.1/2.3.3 if your examiner would expect the textbook-level RL citation
  alongside the bandit-specific ones.
- **V-Model source:** both supervisor papers cite "V-modell xt bund" (official German federal
  V-Model standard, https://www.cio.bund.de/) and S. Mathur/S. Malik "Advancements in the
  v-model" (2010) — add whichever fits your Ch.2 background section if you discuss the V-model
  explicitly; omitted from the numbered list above only for space, not because they're
  unimportant — restore them if Ch.2.1.4 needs V-model grounding beyond what's already in your
  background text.

## Next steps

1. Review this list — trim anything you don't intend to actually cite (better to have 30 solid
   citations than 44 padding ones).
2. Once trimmed, ask me to convert the kept entries into real `@article`/`@inproceedings`/`@misc`
   BibTeX entries in `writing/bibliography.bib`, using the suggested keys above so they slot
   straight into `\cite{key}` calls in `Template.tex`.
3. Cross-check against the "Quick-reference" mapping tables at the bottom of the two supervisor
   paper `.md` files for any reference you want to pull in that wasn't included here.
