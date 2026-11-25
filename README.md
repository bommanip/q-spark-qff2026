# Q-Spark

**IBM Qiskit Fall Fest 2026 · Quantum for Humanity · Education track**

Q-Spark is a tabletop-style learning project for students and first-time quantum learners. Players flip coins, link a pair of magic dice, and search four treasure boxes. The interactive circuit modules run real Qiskit circuits and show the measurement results. The guided game and quizzes are planned in English and Kannada.

## Run the app locally

Clone the repository and run the commands below from its root. Use Python 3.14 and a platform with a Qiskit Aer wheel. Setup was verified on Apple Silicon macOS. Windows and Linux commands are provided below.

**macOS or Linux**

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m waitress --listen=127.0.0.1:8056 --threads=2 backend.app:app
```

**Windows PowerShell**

```powershell
py -3.14 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m waitress --listen=127.0.0.1:8056 --threads=2 backend.app:app
```

Open http://127.0.0.1:8056. The same server delivers all five modules and their simulator APIs. The static project landing page remains available at [docs/index.html](docs/index.html).

## Share a temporary demo

Start the local app first. [Install cloudflared](https://developers.cloudflare.com/tunnel/downloads/) and run this in a second terminal.

```sh
cloudflared tunnel --url http://127.0.0.1:8056
```

Share the HTTPS URL printed by the command. Anyone with the link can use the simulator while your computer, the app, and the tunnel are running. Press Ctrl+C in the tunnel terminal to stop sharing. Quick Tunnels require no Cloudflare account or domain, generate a new URL on restart, cap simultaneous in-flight requests at 200, and carry no uptime guarantee. [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/)

## The pitch — Quantum computing as a board game

> We turn quantum rules into a puzzle game using coins, magic dice, and treasure boxes. Make a prediction, play a move, and use the results to explain what happened.

1. **The levitating coin.** A regular coin on the table shows heads or tails. In our game, a levitating coin represents a qubit prepared so either result is equally likely. Catch the coin to reveal one outcome. Catch a fresh batch of identically prepared coins to see the two outcomes show up roughly equally.
2. **Tilt the spin.** Play a Tilt move and catch a fresh batch. One setting can make heads appear about 85% of the time. Then try the phase move. Imagine two waves that can reinforce each other or cancel. Change their timing and then bring them together with a final move. The histogram shows how that changes which result you’re likely to catch.
3. **The magic linked dice.** First roll two unlinked dice that each show heads or tails. Then play Entangle and roll again. In the game’s ideal linked setup, the results match every time when both dice are read the same way. Each die on its own still looks random. Run the same experiment on a real machine and see how often noise breaks the pattern.
4. **The four-box treasure hunt.** One box contains gold. Start with all four equally likely. Play **Scanner** to secretly mark the winning box, then **Nudge** to make the empty-box possibilities cancel and the gold-box possibility reinforce itself. Reveal one box. In the ideal four-box puzzle with one treasure, the correct pair of moves makes gold appear every time. Try skipping Nudge and see what changes.

## What we’ll build

Three guided lessons, each with a prediction, a learner-controlled move, a histogram, and a quiz with feedback. Reveal the Qiskit circuit on demand so a curious player can connect the move to the underlying gate.

| Lesson | Player experiment | Qiskit implementation |
| --- | --- | --- |
| 1. Coin Lab | Flip, float, tilt, and compare with and without the phase move | Start at `0`; use X for a classical flip, H for the balanced state, a calibrated RY from `0` for Tilt, and H–Z–H versus H–H to show interference |
| 2. Linked Dice | Compare independent random rolls with entangled pairs | H on both qubits for the independent run; H then CX for the Bell pair; measure both qubits in the computational basis |
| 3. Treasure Hunt | Compare a blind guess, Scanner alone, and Scanner plus Nudge | Two-qubit uniform state, one marked-state phase oracle, and one Grover diffusion step |

Players use a single local Flask page with plain HTML, CSS, and JavaScript. One Python circuit module serves both the game and a terminal runner. The runner and game return the same lesson ID, selected moves, source, shot count, and outcome counts. Use Qiskit Aer for the default execution path. Defer a free-form circuit editor, Q-Sphere, and cloud hosting until the guided demo is complete. [IBM guide to Qiskit Aer](https://quantum.cloud.ibm.com/docs/guides/simulate-with-qiskit-aer)

### Benchmark and hardware plan

Compare first-pick success across all four treasure positions using the same number of trials per position. Use a uniform random classical first guess and report an exhaustive classical search separately if demonstrating repeated guesses. Grover uses one marking oracle call plus diffusion in this example. Include oracle and circuit overhead when discussing the result. This exercise demonstrates amplitude amplification in a tiny search space.

| Mode | Expected first-pick gold rate | Measured rate |
| --- | ---: | --- |
| Classical uniform guess | 25% | Pending |
| Ideal Aer, Scanner only | 25% | Pending |
| Ideal Aer, Scanner + Nudge | 100% | Pending |
| IBM device, Scanner + Nudge | Device dependent | Pending |

Validate the Bell circuit and all four marked boxes on Aer. Check that the counts sum to the shot budget and that displayed box labels map correctly to Qiskit bit strings. Queue the short Bell circuit on an IBM device early, then submit the treasure circuit after validation. Transpile to the selected backend and run with Qiskit IBM Runtime SamplerV2. Keep credentials local. Record backend, job ID, shot count, transpiled depth, raw counts, and any mitigation applied. Use completed hardware results in the pitch and keep the live demo on Aer. If the queue runs past freeze, report a labeled noise-model run and the hardware job status. [IBM SamplerV2 documentation](https://quantum.cloud.ibm.com/docs/api/qiskit-ibm-runtime/sampler-v2)

## Hackathon execution

The playbook gives the midpoint review as **26 November at 16:30 IST**, code freeze as **26 November at 23:59 IST**, and finals as **27 November at 09:30 IST**.

| When | Work and exit criteria |
| --- | --- |
| 25 Nov | Build one complete Coin Lab flow from terminal to browser. In parallel, draft all three lessons and Kannada copy, implement the classical baseline, and validate and queue the Bell hardware job. |
| 26 Nov, before midpoint | Finish the linked dice and treasure lessons and review both languages. Verify fresh installs on macOS and Windows. Ask at least three learners to try a lesson, record anonymous before-and-after answers, and capture where they got stuck. |
| 26 Nov, after midpoint | Fix issues that block the demo. Fill the comparison table with observed results, add the architecture diagram and hardware evidence, record the three-minute pitch, and submit before freeze. |
| 27 Nov, if selected | Rehearse the five-minute live pitch and three-minute Q&A. Keep a local simulator demo and a recording ready. |

Assign owners for **Qiskit and hardware**, **terminal and classical benchmark**, **game and integration**, and **bilingual lessons, learner testing and pitch**. A three-person team can combine the terminal and game responsibilities. Agree on the result format before parallel work begins.

### Three-minute judging pitch

- **0:00–0:30** — Explain the learning barrier and show the English and Kannada switch.
- **0:30–1:30** — Ask for a prediction, change a move, run the circuit, and explain what changed in the histogram.
- **1:30–2:30** — Play Scanner and Nudge, compare with the classical first guess, and show hardware results or the labeled noise-model fallback.
- **2:30–3:00** — Share what the learner test showed and how judges can run the project.

### Submission checklist

- [ ] Public GitHub repo with an open-source license, library credits, and pinned dependencies.
- [ ] Runnable Qiskit code, verified setup commands, and three guided lessons with quizzes in both languages.
- [ ] Measured classical comparison, circuit statistics, and honest limitations.
- [ ] Anonymous learner-test findings and one-slide architecture diagram.
- [ ] Repo and three-minute video links submitted with team name, team members, and Education track.

F1Qubit and LGSquash served as references for concise local setup instructions and documenting what has been verified. Write the Q-Spark implementation during the hackathon and credit external libraries in line with the playbook.

## License

Q-Spark is available under the [MIT License](LICENSE).
