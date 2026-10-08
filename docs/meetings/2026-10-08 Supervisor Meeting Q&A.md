# AURORA: Supervisor Meeting Q&A, October 8, 2026

Spoken answers to the supervisors' questions, with every open point from the earlier prep file resolved. Each answer was checked against the repo (github.com/ismaelouadria/AURORA, as of commit `4c8dfc8`, Oct 7). A short "Checked" line under each answer says what backs it up.

---

## Before the meeting: what we have actually run

The "Data, Simulation and Feasibility" section of the short proposal is commented out with the note "a lot of fake claims, made up data, and false info". **Most of that section is backed by files in the repo.** A few points were stated too strongly.

| Claim in the commented-out section | Status | Evidence in the repo |
|---|---|---|
| OPM Flow ran the full Egg model (120 steps of 30 days, 3,600 days) | **True** | `docs/feasibility/F3_opm_egg_execution_test.md`: exit status 0, OPM Flow 2026.04 in Docker, pinned image digest |
| Injector 1 lowered from 79.5 to 60 m³/d, field injection 636.0 → 616.5, total oil −0.35%, total water −3.82% | **True** | `evidence/F3/baseline_vs_perturbed_comparison.txt` (FOPT −0.353843%, FWPT −3.816935%; injectors 2 to 8 unchanged) |
| Egg settings: 79.5 m³/d per injector, 420 bar limit, producers at 395 bar | **True** | Values from the Egg deck (`evidence/F2/egg_audit_summary.txt`, F2 report §8). The units come from the Egg paper. |
| "All 100 versions load correctly" | **Partly true** | All 100 rock-property files were checked and are valid (F2). Only the base case has been run in OPM. |
| Volve: 7 wells (2 injectors, 5 producers), about 15,600 daily records, about 43% missing downhole pressure | **True** | I recounted it from `data/volve/original/Volve production data.xlsx`: 15,634 daily rows, 7 well bores, 42.6% of downhole pressure missing |
| "The injectors have almost no pressure data" | **Stronger than that** | Injectors F-4 and F-5 have **no** downhole pressure at all (100% missing, `evidence/F7/volve_missingness_by_well.csv`) |
| Some wells switch roles; a few negative volumes | **True** | F-5 has 160 production rows besides its injection rows; 4 rows have negative water volume (`evidence/F7/`) |
| CRM fitted to monthly Volve data, tested on the last 30%, beat "next month = this month" for only 1 of 5 producers | **Backed by a results file** | `evidence/F7/volve_crmip_corrected_validation.csv`: 64 training and 28 test months; error below the simple forecast only for F-1 C. The script that produced it was not kept (the feasibility README says so). |
| Feasibility checks F1 to F7 all passed | **Overstated** | Reports F1 to F7 exist. F3, F4 and F7 are a plain PASS. F1, F2, F5 and F6 are a **conditional** pass. The consolidated go/no-go file `G0_final_go_no_go.md` is empty. |

**What has not been done yet:** timing OPM one decision at a time, comparing our Egg run with Egg's published reference results, and reading pressure values out of OPM's saved state files. The answers below present those as next steps.

**What you can safely say in the meeting:** "Before writing the proposal we ran a feasibility study, and it's in the repo. OPM runs the Egg model end to end, and when we changed one injector, OPM applied the change and production responded. We also audited the Volve data. What we haven't done yet is time OPM, and that's our first task."

---

## 1. "How does the hardware fit in, or is it just an add-on?"

"We took it out. You were right that it was an add-on: it didn't help answer our research question, and you asked that every part be needed for that question. Robustness is now tested in software. Timur's part injects faults into the running system: stale, missing or invalid sensor data, dropouts and model drift. A supervisor detects them and falls back to a safe mode. That tests the same idea, keeping the system safe when inputs go wrong, without any hardware."

## 2. "How is the AI actually useful here?"

"Every 90 days someone has to decide how much water each of the 8 injectors gets. That's 40 decisions over the reservoir's 3,600-day life. It's hard to do by hand for three reasons:
- **You can't see underground.** You only see measurements at the wells.
- **Effects are delayed.** Pushing harder now can flood the producers with water later.
- **The accurate simulator is too slow** to try every option.

RL learns a decision policy by trial and error in simulation. We don't just assume it helps: we compare it against Egg's fixed rates (C0) and a hand-written rule (C1). If it doesn't beat them, we report that.

Our real contribution isn't the AI itself. It's making the AI's decisions safe. The safety filter checks every decision with a fast model, and our margin accounts for how wrong that fast model is."

*Checked:* 90-day step and 40 decisions are in `proposal/main_short.tex` (decision interval row). The F6 novelty report also says the contribution must be the integration and the measured-error margin, not RL itself.

## 3. "How big is your data, where is it from, and what's in it?"

"Most of our data we generate ourselves, by running a simulator, so the limit is computing time, not data.
- **Egg model.** A published benchmark reservoir from TU Delft (Jansen and colleagues, 2014). It has 100 versions that differ in their rock properties, a 60×60×7 grid with 18,553 active cells, 8 injectors and 4 producers, and a 420 bar injector pressure limit. We've checked all 100 rock files and run the base version in OPM.
- **OPM Flow.** An open-source simulator. Each run gives rates for every well at every step, and the saved state holds pressure and water saturation in every cell.
- **Volume.** We plan about 2,000 short paired runs to measure the fast model's error, and about 840 full simulations for the final test.
- **Volve.** Real data from Equinor's Volve field in the North Sea, released for research. The daily table has 15,634 records from 7 wells, 2 injectors and 5 producers, from 2008 to 2016. It's messy: downhole pressure is missing in about 43% of records and completely missing for both injectors. We use it to see what real data problems look like, and that shapes Timur's fault scenarios. We don't test controllers on it, because a recording can't show what would have happened under different decisions."

*Checked:* Egg facts in `evidence/F2/egg_audit_summary.txt` and F3 §3. Volve recounted from the spreadsheet (see the table above). Production runs from Feb 2008 to Sep 2016; injector rows in the table run from Sep 2007 to Dec 2016.

## 4. "Can you tell if the output is right or wrong? Who's the subject expert?"

"Nobody on the team is a reservoir engineer, and we say so in the proposal. So we've designed the project so that it doesn't depend on an expert checking every run. We check at four levels:
1. **Each part on known answers.** For example, the fast model must recover settings we planted, and the filter must leave an already-safe decision unchanged.
2. **The experiment ran as planned.** We use logged runs and checks we can predict in advance. A margin of zero must behave exactly like the plain filter, and a bigger margin must never cause more violations.
3. **Physical sense at every step.** No negative flows, water cut between 0 and 1, totals that add up, and changes going in the right direction. We'll also compare our base Egg run with Egg's published reference results.
4. **We write down what each possible result would mean before we see the results.**

OPM is the reference for every number, not our own model.

For expert input, we've already written a short review packet listing the specific reservoir assumptions we'd want checked. It isn't a request to check every run. Could you suggest someone we could send it to, maybe in Earth Sciences, for one or two reviews at milestones?"

*Checked:* the packet is `docs/reservoir-knowledge/EXPERT_REVIEW_PACKET.md`. No expert has been contacted, so the answer asks for one instead of claiming a scheduled review. Note that the proposal contradicts itself here: it says "we cannot ask an expert to review our system", but its risk table and summary table list a "scheduled expert review".

## 5. "How will you demo this to the second reader and at the fair?"

"Not numbers in a terminal. We'll build an interactive dashboard that replays any run step by step:
- the well map;
- what the AI proposed against what was applied;
- a pressure gauge against the limit;
- the fast model's error;
- a live fault panel.

Mahdi owns the dashboard. Each of us presents our own part:
- **Aziz:** runs one OPM step live and shows a decision change taking effect. We've already shown OPM applies a changed injector rate exactly.
- **Ismael:** replays a step where the plain filter lets a violation through and ours doesn't.
- **Abdurrahman:** shows the training curves.
- **Timur:** triggers a frozen-sensor fault from his fault panel and shows the supervisor switching to the safe fallback.
- **Mahdi:** traces a result back to its run record.

At the fair, the dashboard replays recorded runs next to the poster."

*Checked:* the ownership table, requirement FR-23 and the schedule all give the dashboard to Mahdi. Timur owns the "live fault panel" (ownership table) and shares FR-24 (trigger a fault from the dashboard) with Mahdi. The skills table marking Timur as visualization lead is the inconsistent cell, so it should be fixed. Timur's demo item matches his fixed role (software fault injection and safe fallback).

## 6. "How many wells, how different are they, and would the AI need each well's specs to avoid bias?"

"Egg has 12 wells: 8 injectors and 4 producers, all vertical and open through all 7 layers. The wells themselves are identical in setup. What changes between the 100 versions is the rock underneath, meaning where the high-flow channels run. So two versions can behave very differently with the same wells.

We deliberately don't give the AI the rock properties or tell it which version it's on, because a real operator doesn't know those either. Each well has its own input slot, so the AI can learn how each well behaves from its measurements.

To check for bias:
- we test on 20 reservoir versions the AI has never seen;
- we report the fast model's accuracy for each well;
- we compute a separate safety margin for each injector.

If by specs you mean fixed facts like each well's position, adding those as inputs is cheap, and it's fair because an operator knows them. We'll try it as a variant once the baseline controller works and keep it if it helps on the unseen versions."

*Checked:* well count and setup in F2 §7 and `evidence/F2/egg_wells.csv`. The well-position variant is a suggested answer, not something in the proposal.

## 7. "Did the whole team discuss this, or did Ismael design it alone?"

"Ismael proposed the idea, did the first feasibility study and wrote up the overall architecture. That's his assigned role, and you can see it in the repo history. Since then the work has been split into five parts, each with a named owner and a backup: Ismael has the fast model and safety filter, Aziz has OPM and Egg, Abdurrahman has the RL controller, Mahdi has logging, experiments and the dashboard, and Timur has fault injection and the supervisor. The changes after your last feedback, dropping the hardware and moving Timur to software fault injection, were team decisions. Mahdi compiled and revised the proposal. From here on, each owner designs the inside of their own part, and our commits and weekly reports will show that."

*Checked:* 15 of the 19 commits are Ismael's (architecture, feasibility and governance docs, Sep 29 to 30), and 4 are Mahdi's (proposal, Oct 7). No commits from Aziz, Abdurrahman or Timur yet. Ownership is written down in `docs/team/README.md`, in `.github/workflows/primary-owner-routing.yml` (issues routed to Ismael, Aziz, Abdurrahman and Mahdi) and in the proposal's ownership table. So the answer doesn't claim everyone has already designed their part. If the professors open the repo, the history matches what you said.

## 8. "If Ismael gets sick, can the rest of the team take over?"

"Yes. Every part has an owner and a backup who reviews every change to it, so nobody's code goes unseen. The backups form a ring:
- Aziz backs up Ismael;
- Ismael backs up Aziz;
- Mahdi backs up Abdurrahman;
- Timur backs up Mahdi;
- Abdurrahman backs up Timur.

Ismael's design and feasibility work is already written down in the repo, and we plan so that no essential work during exams depends on one person. Those are risks R12 and R14 in our risk list."

*Checked:* ring and R12/R14 match `proposal/main_short.tex` (ownership table and risk table).

## 9. "Is the team feasible: enough knowledge and data to do what you claim?"

"We've kept the claim narrow. We're not inventing a new algorithm. We combine established, open-source pieces and test the combination in simulation only:
- OPM Flow for simulation;
- PPO from Stable-Baselines3 for the controller;
- a quadratic-programming filter;
- conformal statistics for the margin.

We checked feasibility before writing the proposal. OPM already runs the Egg model end to end, and when we changed one injector's rate, OPM applied it exactly and production responded. Data isn't a constraint because we generate it ourselves. The total cost is $0 to $210.

The biggest open risk is OPM speed: we've run it, but we haven't timed it one decision at a time. That's literally our first task. If one full run takes more than 30 minutes, we train mostly on the fast model, make decisions less often and run simulations in parallel.

Every risk has a fallback planned in advance. Even if the margin doesn't help, a clear 'no' backed by evidence is still a valid result."

*Checked:* F3 evidence records no run time, so "we haven't timed it" is accurate. The 30-minute trigger is risk R8, owned by Aziz. The cost total is in the proposal's cost table.

---

## The three warnings

**"You can't ask the expert after every run."**
"Agreed. That's why the checks in Q4 are automated and why we decide in advance what each result means. Expert input is for an occasional, targeted review of our assumptions, and we've written that review packet already."

**"Reading the dataset manual isn't enough."**
"Agreed, and we've started. We've already run Egg in OPM, changed one injector and checked the reservoir responded the way it should: less water injected, less water produced. Our plan from here:
- compare our base run with Egg's published reference results;
- make one change at a time and check the direction of each response;
- run physical checks on every step.

The repo also has our own domain notes: a reservoir guide, a waterflooding and well-controls guide, and a glossary. Each new member reads those first. We learn the reservoir by running it, not just by reading about it."

*Checked:* `docs/reservoir-knowledge/` holds `RESERVOIR_DOMAIN_GUIDE.md`, `WATERFLOOD_AND_WELL_CONTROLS.md`, `GLOSSARY.md` and others. The comparison with Egg's published reference results has not been done yet, so it is presented as a plan.

**"Justify every tool, with the alternatives you rejected."**

| Choice | Alternatives rejected | Main reason |
|---|---|---|
| OPM Flow | MRST, commercial simulators | Free, open source, and we've run Egg in it as published |
| Egg | SPE10, OLYMPUS, a Volve model | 100 versions allow a clean train/calibration/test split, and runs are quick |
| CRM fast model | Simpler CRM, neural network | Its parameters have a physical meaning, and it keeps the filter a simple optimization |
| PPO with memory | PPO fed its last few observations, SAC | Learns what to remember; the simpler version is the fallback |
| Safety filter | Penalty in the reward, constrained RL | Checks every decision and shows why it changed one |
| Conformal margin | Assume bell-curve errors, use the worst error seen | No assumption about how the errors are distributed |

Say it from this table in the meeting. The written proposal should get its "Alternatives considered" table back: it's still in `main_short.tex`, just commented out.

---

## What I couldn't verify, and what I assumed

- **Who ran the OPM test.** The F3 run was recorded on Sep 22 on an Apple Silicon Mac and moved into the repo by Ismael on Sep 29. The repo doesn't say whose machine it was. Since Aziz presents OPM, he should be able to rerun it (the Docker image digest is in `evidence/F3/opm_environment.txt`) before saying "we ran it" with confidence.
- **Why Mahdi called the data section fake.** The evidence supports nearly all of it, so he may have meant something the repo doesn't show. Ask him before the meeting. If nothing else comes up, the section can be restored with the corrections in the first table.
- **The Volve CRM result.** It comes from a saved results file, but the script that made it wasn't kept. Call it "an exploratory fit", not a finished result.
- **Units.** The deck stores raw numbers. m³/d and bar come from the Egg paper, and the F3 report lists the exact units as still to be confirmed against the OPM manual.
- **Assumed for Q7:** that the hardware removal and Timur's new role were team decisions. Project notes say Aziz chose Timur's role on Sep 30. Change the wording if it was decided differently.
- **Assumed for Q4:** that asking the supervisors for an expert contact is acceptable. No expert has been approached.
- **Assumed for Q6:** that trying well positions as an extra input is fine to offer. It isn't in the proposal.
- **Not checked:** the published Egg facts against the Egg paper itself, beyond what the repo's F2 and F5 reports cite (Jansen 2014, Geoscience Data Journal, DOI 10.1002/gdj3.21).
