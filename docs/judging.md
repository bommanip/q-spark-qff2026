# Q-Spark judging guide

## Three-minute recording

| Time | Show | Say |
| --- | --- | --- |
| 0:00–0:20 | Slide 1 | “Quantum computing is hard to picture, especially when lessons assume advanced math or English fluency. Q-Spark gives beginners something familiar to predict, try, and explain.” |
| 0:20–0:45 | Slide 2 and Kannada lesson | “Start in any of four languages. Each concept has a short narration and caption. Five modules connect the lessons to quizzes, and the arcade turns the ideas into experiments.” |
| 0:45–1:35 | Slide 3 and live Treasure Hunt | “There are four boxes. A blind guess has a one-in-four chance. Pick Crystal Valley, run the search, and look at the histogram. Qiskit marks the target, then interference amplifies it. Try another box if time allows.” |
| 1:35–2:05 | Slide 4 | “The browser sends the selected move to Flask. We build the circuit in Qiskit, run it locally on Aer, and return the actual measurement counts and circuit diagram. No quantum account is needed for the simulator.” |
| 2:05–2:35 | Slide 5 | “We ran 4,096 trials per method across all four boxes. Blind guesses succeeded 23.78% of the time, ideal Aer 100%, and our illustrative noisy simulation 97.07%. This shows the effect on first-pick probability in a four-box example.” |
| 2:35–3:00 | Slide 6 | “Our goal is to help beginners explain what they just observed. Here’s the repository to reproduce the demo.” Add observed learner outcomes only after running the test. |

For finals, use two extra minutes for a before-and-after Coin Lab run and a question about why the noisy result drops. The playbook gives finalists five minutes for the live pitch and three minutes for Q&A.

## Scoring priorities

| Weight | Criterion | Show the judges |
| ---: | --- | --- |
| 30% | Technical rigor | Change a learner input, run a real Qiskit circuit live, and point to its measured counts, pinned dependencies, and reproducible benchmark. |
| 25% | Humanitarian impact | Identify beginner students as the audience. Switch to Kannada or Telugu and play narration. Report what real learners understood before and after. |
| 25% | Innovation and feasibility | Connect the analogy to the circuit, compare with the classical baseline, and explain the noise-model result and its limits. |
| 20% | Pitch and presentation | Show one full experiment within three minutes. Use one architecture slide and keep the local demo and a recorded clip available. |

## Quick learner test

Ask at least three beginners to try the app. Use anonymous participant IDs and their language choice. Ask the same two questions before and after a lesson, using the same rubric.

1. What are the possible results of measuring a qubit prepared with equal odds?
2. Why might the measured counts differ from exactly half on each side?

Give one point per correct explanation. Record the before and after score out of two, one observed stumbling point, and any feedback the learner agrees can be quoted. Report the sample size and actual counts. Do not infer a population-wide result from a small sample.

## Submission checklist

- [x] Public repository, license, setup, runnable circuit, screenshots, and baseline comparison.
- [x] Three or more guided lessons with quizzes, four language options, and a local simulator.
- [x] Circuit depth and an illustrative noise simulation.
- [ ] Complete and summarize an anonymous learner test.
- [ ] Record the three-minute pitch and add its shareable link to the README and form.
- [ ] Submit the repository and video links with the confirmed team name, members, and Education track before **26 November 2026, 23:59 IST**.
