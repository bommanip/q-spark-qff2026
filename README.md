# Q-Spark 🚀
### Explore the World of Quantum Computing — One Qubit at a Time

**Q-Spark** is an interactive, beginner-friendly quantum computing learning platform designed to make complex quantum concepts easier to understand through visual demonstrations, hands-on experiments, quizzes, and real quantum circuit simulations powered by Qiskit.

Whether you're completely new to quantum computing or curious about how quantum computers work, Q-Spark takes you on a guided learning journey from classical bits to quantum algorithms.

---

## ✨ Key Features

- **5 Interactive Learning Modules** — Learn quantum computing step by step.
- **Multilingual Support** — Available in English, Kannada, Hindi, and Telugu.
- **Interactive Experiments** — Explore quantum gates, superposition, and entanglement.
- **Qiskit Integration** — Run quantum circuit simulations using Qiskit and Qiskit Aer.
- **Knowledge Quizzes** — Test your understanding after each module.
- **Progress Tracking** — Track completed modules and quiz scores.
- **Module Unlocking System** — Progress through the learning journey by completing quizzes.
- **Certificate Generation** — Generate and print a certificate after completing all five modules and meeting the quiz requirements.
- **Responsive Interface** — Designed for an engaging learning experience across screen sizes.

---

## 📚 Learning Modules

| Module | Topic | What You'll Learn |
|---|---|---|
| 01 | Quantum Fundamentals | Computers, classical bits, quantum computers, and qubits |
| 02 | Superposition & Entanglement | Understand two fundamental quantum phenomena |
| 03 | Quantum Gates | Explore X, H, Z, CNOT, and combined gate operations |
| 04 | Grover's Algorithm | Discover how quantum search works |
| 05 | Quantum Computing Review | Test your knowledge and earn your certificate |

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Responsive web design
- Browser Local Storage

### Backend
- Python
- Flask
- Flask-CORS
- Qiskit
- Qiskit Aer

---

## 🌍 Language Support

Q-Spark supports four languages:

- 🇬🇧 English
- 🇮🇳 Kannada
- 🇮🇳 Hindi
- 🇮🇳 Telugu

The selected language is saved so learners can continue using their preferred language while navigating the platform.

---

## Run Q-Spark locally

Clone the [repository](https://github.com/bommanip/q-spark-qff2026) and run these commands from `q-spark-qff2026` with Python 3.14 installed.

### macOS or Linux

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m waitress --listen=127.0.0.1:8056 --threads=2 backend.app:app
```

### Windows PowerShell

```powershell
py -3.14 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m waitress --listen=127.0.0.1:8056 --threads=2 backend.app:app
```

Open <http://127.0.0.1:8056/>. The same server handles the pages, audio, and simulator. Press Ctrl+C to stop it.

## 🔬 Quantum Experiments

Q-Spark provides hands-on quantum experiments through its Flask backend.

| Experiment | Description |
|---|---|
| Superposition | Explore the Hadamard gate |
| Entanglement | Simulate an entangled Bell state |
| X Gate | Explore quantum bit flipping |
| Z Gate | Understand phase flipping |
| CNOT Gate | Explore controlled quantum operations |
| Combined Gates | Experiment with multiple quantum gates |
| Grover's Algorithm | Explore quantum search |

Quantum simulations use Qiskit and Qiskit Aer.

---

## 🎓 Learning & Certification

Q-Spark uses an interactive progression system:

1. Start with Module 1.
2. Learn the concepts and complete the quiz.
3. Unlock the next module by achieving the required score.
4. Complete all five modules.
5. Achieve the required final quiz score.
6. Generate your completion certificate.

Learning progress and quiz scores are stored in browser Local Storage.

---

## 📁 Project Structure

```text
Q-spark/
│
├── frontend/
│   ├── index.html
│   ├── module1.html
│   ├── module2.html
│   ├── module3.html
│   ├── module4.html
│   └── module5.html
│
├── backend/
│   └── app.py
│
└── README.md
```

---

## 🎯 Project Objective

The primary objective of Q-Spark is to make quantum computing more accessible to beginners through interactive education.

Instead of relying only on theoretical explanations, the platform combines learning content, visual demonstrations, quantum simulations, and assessments to create an engaging learning experience.

---

## 🚀 Future Enhancements

- Additional advanced quantum computing modules.
- More interactive quantum circuit visualizations.
- Additional regional language support.
- Expanded quantum algorithm experiments.
- Learner dashboards and detailed performance analytics.

---

## Narration

The five steps each have a separate play/pause control in English (`en`), Kannada (`kn`), Telugu (`te`), and Hindi (`hi`). The browser plays the bundled MP3s from [frontend/fundamentals/audio](frontend/fundamentals/audio). Playback runs locally with no model install, account, or API key.

Edit [narration.js](frontend/fundamentals/narration.js) to update both the visible caption and the source for synthesis. Keep the order **classical**, **qubit**, **interference**, **tilt**, **entanglement**. The audio filename is `<language>-<step number>.mp3`, starting at 1. When you edit a caption, regenerate its clip and check the pronunciation before sharing it.

### Regenerate clips

Use a separate Python 3.12 virtual environment and install FFmpeg with `libmp3lame` available on PATH. These commands use an activated environment. On macOS or Linux, activate it with `source .venv-audio/bin/activate` after creating it with `python3.12 -m venv .venv-audio`. On Windows, use `py -3.12 -m venv .venv-audio` and `.\.venv-audio\Scripts\Activate.ps1`.

```sh
python -m pip install "torch>=2.4" "transformers>=5,<6" safetensors sentencepiece numpy soundfile "misaki[en]>=0.9.4" espeakng-loader phonemizer-fork "spacy>=3.8" num2words
python -m spacy download en_core_web_sm
hf download Oomni/mithi-v2-flash --revision 1fc0dd68496a2483508ec764d310146c41ff90be --local-dir ../mithi-v2-flash --exclude "assets/*"
```

The model is [Mithi v2 Flash](https://huggingface.co/Oomni/mithi-v2-flash) under Apache-2.0. The script loads the pinned model's Python runtime from `--model-dir`, uses its built-in **Vaidehi** voice on CPU, and encodes mono MP3s at 64 kbps. Keep the downloaded model and weights outside the app repository.

```sh
# Update only the Kannada interference clip
python tools/generate_coin_audio.py --model-dir ../mithi-v2-flash --language kn --step interference

# Regenerate all 20 clips
python tools/generate_coin_audio.py --model-dir ../mithi-v2-flash
```

The five modules and three arcade games also have one localized guide each. Edit [their caption scripts](frontend/narration/scripts.js) in page order: Modules 1–5, Coin Lab, Linked Dice, Treasure Hunt. Use `--scope pages` to regenerate all 32 page clips, or limit the command to a specific language and page.

```sh
python tools/generate_coin_audio.py --scope pages --model-dir ../mithi-v2-flash --language te --step linked-dice
```

For page narration the default output is `frontend/narration/audio`, with filenames such as `te-linked-dice.mp3`.

Each module also has a separate clip for every concept or activity section. Edit [the concept scripts](frontend/narration/concepts.js) under the matching concept key and language. Use `--scope concepts` to regenerate all 88 concept clips, or add filters for the clip you changed. The generator writes them to `frontend/narration/audio` using the concept key, such as `kn-module2-bell.mp3`.

```sh
python tools/generate_coin_audio.py --scope concepts --model-dir ../mithi-v2-flash --language kn --step module2-bell
```

Use `--output-dir` to preview generated files in a separate directory. The generator replaces only the selected clips in the output directory.

## 👩‍💻 About the Project

**Q-Spark** is an educational technology project focused on making quantum computing accessible, interactive, and enjoyable for beginners.

**Built with curiosity. Powered by quantum computing. Designed for learning.**

---

⭐ If you find this project interesting, consider starring the repository!
