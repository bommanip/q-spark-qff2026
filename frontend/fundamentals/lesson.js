(() => {
    const lesson = document.querySelector(".coin-lesson");
    const picker = document.getElementById("languageSelect");
    const audio = lesson.querySelector("audio");
    const cards = [...lesson.querySelectorAll(".coin-step")];
    const copy = {
        en: {
            title: "Quantum Coin Trail", intro: "Flip a bit, measure a qubit, and explore how quantum circuits change the odds.",
            play: "Play explanation", pause: "Pause", replay: "Replay explanation",
            note: "The spinning coin is an analogy. The sphere arrow represents the qubit state. The two poles represent the two possible measurement results.",
            unavailable: "Audio couldn’t play. You can still read the explanation below."
        },
        kn: {
            title: "ಕ್ವಾಂಟಮ್ ನಾಣ್ಯದ ಪಯಣ", intro: "ಬಿಟ್ ತಿರುಗಿಸಿ, ಕ್ಯೂಬಿಟ್ ಅಳೆಯಿರಿ ಮತ್ತು ಕ್ವಾಂಟಮ್ ಸರ್ಕ್ಯೂಟ್‌ಗಳು ಸಾಧ್ಯತೆಗಳನ್ನು ಹೇಗೆ ಬದಲಾಯಿಸುತ್ತವೆ ಎಂದು ನೋಡಿ.",
            play: "ವಿವರಣೆಯನ್ನು ಕೇಳಿ", pause: "ವಿರಾಮ", replay: "ವಿವರಣೆಯನ್ನು ಮತ್ತೆ ಕೇಳಿ",
            note: "ತಿರುಗುವ ನಾಣ್ಯ ಒಂದು ಹೋಲಿಕೆ. ಗೋಳದ ಮೇಲಿನ ಬಾಣ ಕ್ಯೂಬಿಟ್‌ನ ಸ್ಥಿತಿಯನ್ನು ತೋರಿಸುತ್ತದೆ. ಎರಡು ಧ್ರುವಗಳು ಮಾಪನದ ಎರಡು ಸಾಧ್ಯ ಫಲಿತಾಂಶಗಳನ್ನು ತೋರಿಸುತ್ತವೆ.",
            unavailable: "ಧ್ವನಿಯನ್ನು ಪ್ಲೇ ಮಾಡಲು ಆಗಲಿಲ್ಲ. ಕೆಳಗಿನ ವಿವರಣೆಯನ್ನು ಓದಬಹುದು."
        },
        te: {
            title: "క్వాంటం నాణెం ప్రయాణం", intro: "బిట్‌ను తిప్పండి, క్యూబిట్‌ను కొలవండి, క్వాంటం సర్క్యూట్లు అవకాశాలను ఎలా మారుస్తాయో చూడండి.",
            play: "వివరణ వినండి", pause: "ఆపండి", replay: "వివరణ మళ్లీ వినండి",
            note: "తిరుగుతున్న నాణెం ఒక పోలిక. గోళంపై బాణం క్యూబిట్ స్థితిని చూపుతుంది. రెండు ధ్రువాలు కొలతలో వచ్చే రెండు ఫలితాలను సూచిస్తాయి.",
            unavailable: "ఆడియో ప్లే కాలేదు. కింద ఇచ్చిన వివరణను చదవండి."
        },
        hi: {
            title: "क्वांटम सिक्के का सफ़र", intro: "बिट पलटें, क्यूबिट मापें और देखें कि क्वांटम सर्किट संभावनाएँ कैसे बदलते हैं।",
            play: "व्याख्या सुनें", pause: "रोकें", replay: "व्याख्या फिर सुनें",
            note: "घूमता सिक्का एक उपमा है। गोले पर तीर क्यूबिट की अवस्था दिखाता है। दोनों ध्रुव मापन के दो संभावित नतीजे दिखाते हैं।",
            unavailable: "ऑडियो नहीं चल पाया। आप नीचे व्याख्या पढ़ सकते हैं।"
        }
    };
    const experimentCopy = {
        en: {
            keepPhase: "Keep phase", flipPhase: "Flip phase", phaseHint: "Both circuits start with 50/50 odds. Recombining after a phase flip changes which face wins.", faces: "0 = heads · 1 = tails", pairOnce: "Measure one pair",
            phase: "Interference", experiment: "Tilt experiment", pair: "Two qubits", reset: "Prepare again", pairRun: "Measure 100 pairs", dice: "Try Linked Dice", prepare: "Set the tilt", expected: "Expected odds",
            classical: "Classical bit", quantum: "Qubit", flip: "Flip the bit",
            measure: "Measure once", sample: "Run 100 measurements", state: "Current bit", outcome: "Measured result",
            observed: "Observed in 100 measurements", busy: "Running Qiskit Aer…", error: "Simulation failed. Try again."
        },
        kn: {
            keepPhase: "ಹಂತವನ್ನು ಉಳಿಸಿ", flipPhase: "ಹಂತವನ್ನು ತಿರುಗಿಸಿ", phaseHint: "ಎರಡೂ ಸರ್ಕ್ಯೂಟ್‌ಗಳು ಸಮಾನ ಸಾಧ್ಯತೆಗಳಿಂದ ಪ್ರಾರಂಭವಾಗುತ್ತವೆ. ಹಂತವನ್ನು ತಿರುಗಿಸಿದ ಬಳಿಕ ಮತ್ತೆ ಸೇರಿಸಿದಾಗ ಫಲಿತಾಂಶ ಬದಲಾಗುತ್ತದೆ.", faces: "0 = ತಲೆ · 1 = ಬಾಲ", pairOnce: "ಒಂದು ಜೋಡಿಯನ್ನು ಅಳೆಯಿರಿ",
            phase: "ಕ್ವಾಂಟಮ್ ಹಸ್ತಕ್ಷೇಪ", experiment: "ಓರೆ ಪ್ರಯೋಗ", pair: "ಎರಡು ಕ್ಯೂಬಿಟ್‌ಗಳು", reset: "ಮತ್ತೆ ಸಿದ್ಧಪಡಿಸಿ", pairRun: "100 ಜೋಡಿಗಳನ್ನು ಅಳೆಯಿರಿ", dice: "ಜೋಡಿ ದಾಳಗಳನ್ನು ಪ್ರಯತ್ನಿಸಿ", prepare: "ಕೋನ ಹೊಂದಿಸಿ", expected: "ನಿರೀಕ್ಷಿತ ಸಾಧ್ಯತೆಗಳು",
            classical: "ಸಾಂಪ್ರದಾಯಿಕ ಬಿಟ್", quantum: "ಕ್ಯೂಬಿಟ್", flip: "ಬಿಟ್ ತಿರುಗಿಸಿ",
            measure: "ಒಮ್ಮೆ ಅಳೆಯಿರಿ", sample: "100 ಬಾರಿ ಅಳೆಯಿರಿ", state: "ಈಗಿನ ಬಿಟ್", outcome: "ಮಾಪನದ ಫಲಿತಾಂಶ",
            observed: "100 ಮಾಪನಗಳ ಫಲಿತಾಂಶ", busy: "Qiskit Aer ಚಾಲನೆಯಲ್ಲಿದೆ…", error: "ಸಿಮ್ಯುಲೇಶನ್ ವಿಫಲವಾಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."
        },
        te: {
            keepPhase: "దశను అలాగే ఉంచండి", flipPhase: "దశను తిప్పండి", phaseHint: "రెండు సర్క్యూట్లు సమాన అవకాశాలతో మొదలవుతాయి. దశను తిప్పి తిరిగి కలిపితే ఫలితం మారుతుంది.", faces: "0 = బొమ్మ · 1 = బొరుసు", pairOnce: "ఒక జతను కొలవండి",
            phase: "క్వాంటం వ్యతికరణం", experiment: "వంపు ప్రయోగం", pair: "రెండు క్యూబిట్‌లు", reset: "మళ్లీ సిద్ధం చేయండి", pairRun: "100 జతలను కొలవండి", dice: "జోడీ పాచికలు ఆడండి", prepare: "కోణాన్ని మార్చండి", expected: "ఆశించిన సంభావ్యతలు",
            classical: "క్లాసికల్ బిట్", quantum: "క్యూబిట్", flip: "బిట్‌ను తిప్పండి",
            measure: "ఒకసారి కొలవండి", sample: "100 సార్లు కొలవండి", state: "ప్రస్తుత బిట్", outcome: "కొలత ఫలితం",
            observed: "100 కొలతల్లో ఫలితాలు", busy: "Qiskit Aer నడుస్తోంది…", error: "సిమ్యులేషన్ విఫలమైంది. మళ్లీ ప్రయత్నించండి."
        },
        hi: {
            keepPhase: "फेज़ वही रखें", flipPhase: "फेज़ पलटें", phaseHint: "दोनों सर्किट बराबर संभावनाओं से शुरू होते हैं। फेज़ पलटकर फिर जोड़ने से नतीजा बदल जाता है।", faces: "0 = चित · 1 = पट", pairOnce: "एक जोड़ी मापें",
            phase: "इंटरफेरेंस", experiment: "झुकाव का प्रयोग", pair: "दो क्यूबिट", reset: "फिर तैयार करें", pairRun: "100 जोड़ियाँ मापें", dice: "जुड़े पासे आज़माएँ", prepare: "झुकाव का कोण चुनें", expected: "अपेक्षित संभावनाएँ",
            classical: "क्लासिकल बिट", quantum: "क्यूबिट", flip: "बिट पलटें",
            measure: "एक बार मापें", sample: "100 बार मापें", state: "वर्तमान बिट", outcome: "मापन का नतीजा",
            observed: "100 मापों के नतीजे", busy: "Qiskit Aer चल रहा है…", error: "सिमुलेशन विफल रहा। फिर कोशिश करें।"
        }
    };
    const tabs = [...lesson.querySelectorAll('[role="tab"]')];
    const controls = cards.map(card => card.querySelector(".coin-play"));
    const reports = new Map();
    const byId = id => document.getElementById(id);
    const angle = byId("coin-preparation");
    const firstMeasure = byId("qubit-measure");
    const reset = byId("qubit-reset");
    let language;
    let current = 0;
    let narrated = -1;
    let bit = 0;

    function renderAudio() {
        controls.forEach((button, index) => {
            const words = copy[language];
            button.textContent = index === narrated && !audio.paused ? words.pause : words.play;
        });
    }

    function showTab(index) {
        audio.pause();
        current = index;
        tabs.forEach((tab, position) => {
            const isCurrent = position === index;
            tab.setAttribute("aria-selected", String(isCurrent));
            tab.tabIndex = isCurrent ? 0 : -1;
            byId(tab.getAttribute("aria-controls")).hidden = !isCurrent;
        });
    }

    function report(id, content) {
        reports.set(id, content);
        byId(id).textContent = content(experimentCopy[language]);
    }

    async function run({ url, data, output, buttons, onResult }) {
        buttons.forEach(button => { button.disabled = true; });
        report(output, words => words.busy);
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error("Simulation failed");
            const result = await response.json();
            if (result.shots !== data.shots ||
                Object.values(result.counts).reduce((sum, count) => sum + count, 0) !== data.shots) {
                throw new Error("Unexpected counts");
            }
            onResult(result);
            return true;
        } catch {
            report(output, words => words.error);
            return false;
        } finally {
            buttons.forEach(button => { button.disabled = false; });
        }
    }

    function updateTilt() {
        const degrees = Number(angle.value);
        const radians = degrees * Math.PI / 180;
        const expectedZero = Math.cos(radians / 2) ** 2;
        const percent = new Intl.NumberFormat(language, { style: "percent", maximumFractionDigits: 1 });
        byId("coin-odds").textContent =
            `${degrees}° · ${experimentCopy[language].expected}: 0: ${percent.format(expectedZero)} · 1: ${percent.format(1 - expectedZero)}`;
        const card = cards[3];
        const settled = card.dataset.result;
        const stateAngle = settled === undefined ? radians : Number(settled) * Math.PI;
        const y = 52 - 36 * Math.cos(stateAngle);
        const x = 52 + 36 * Math.sin(stateAngle);
        const arrow = card.querySelector(".coin-state-tilt");
        arrow.querySelector("line").setAttribute("x2", x);
        arrow.querySelector("line").setAttribute("y2", y);
        arrow.querySelector(".point").setAttribute("cx", x);
        arrow.querySelector(".point").setAttribute("cy", y);
        card.style.setProperty("--coin-tilt", `${(degrees - 90) / 2}deg`);
    }

    function applyLanguage() {
        language = Object.hasOwn(copy, picker.value) ? picker.value : "en";
        audio.pause();
        narrated = -1;
        const words = copy[language];
        const experiment = experimentCopy[language];
        lesson.querySelectorAll("[data-coin-copy]").forEach(element => {
            const key = element.dataset.coinCopy;
            element.textContent = words[key] || experiment[key];
        });
        cards.forEach((card, index) => {
            card.querySelector(".coin-caption").textContent = coinNarration[language][index];
            card.querySelector(".coin-audio-status").textContent = "";
        });
        report("classical-outcome", text => `${text.state}: ${bit}`);
        reports.forEach((content, id) => report(id, content));
        updateTilt();
        renderAudio();
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => { if (index !== current) showTab(index); });
        tab.addEventListener("keydown", event => {
            const next = {
                ArrowLeft: (index + tabs.length - 1) % tabs.length,
                ArrowRight: (index + 1) % tabs.length,
                Home: 0,
                End: tabs.length - 1
            }[event.key];
            if (next === undefined) return;
            event.preventDefault();
            showTab(next);
            tabs[next].focus();
        });
    });

    controls.forEach((button, index) => button.addEventListener("click", async () => {
        if (narrated === index && !audio.paused) {
            audio.pause();
            return;
        }
        const status = cards[index].querySelector(".coin-audio-status");
        status.textContent = "";
        if (narrated !== index) {
            narrated = index;
            audio.src = `fundamentals/audio/${language}-${index + 1}.mp3`;
        }
        try {
            await audio.play();
        } catch (error) {
            if (error.name !== "AbortError") status.textContent = copy[language].unavailable;
        }
    }));
    for (const event of ["play", "pause", "ended"]) audio.addEventListener(event, renderAudio);

    byId("classical-flip").addEventListener("click", () => {
        bit = 1 - bit;
        cards[0].classList.toggle("is-one", bit === 1);
        report("classical-outcome", words => `${words.state}: ${bit}`);
    });
    firstMeasure.addEventListener("click", async () => {
        const success = await run({
            url: "/run-coin-lab", data: { tilt_degrees: 90, shots: 1 },
            output: "qubit-outcome", buttons: [firstMeasure],
            onResult(result) {
                cards[1].dataset.result = String(result.counts["1"] || 0);
                report("qubit-outcome", words => `${words.outcome}: ${cards[1].dataset.result}`);
            }
        });
        firstMeasure.disabled = success;
        reset.disabled = !success;
    });
    reset.addEventListener("click", () => {
        delete cards[1].dataset.result;
        report("qubit-outcome", () => "");
        firstMeasure.disabled = false;
        reset.disabled = true;
    });

    const phaseButtons = [...lesson.querySelectorAll("[data-phase]")];
    phaseButtons.forEach(button => button.addEventListener("click", () => {
        delete cards[2].dataset.result;
        run({
            url: "/run-module3", data: { gate: button.dataset.phase, shots: 100 },
            output: "phase-outcome", buttons: phaseButtons,
            onResult(result) {
                const zero = result.counts["00"] || 0;
                const one = result.counts["01"] || 0;
                if (zero === 100 || one === 100) cards[2].dataset.result = one === 100 ? "1" : "0";
                report("phase-outcome", words =>
                    `${words[button.dataset.coinCopy]} · ${words.observed}: 0: ${zero}% · 1: ${one}%`);
            }
        });
    }));

    const measure = byId("coin-measure-once");
    const sample = byId("coin-sample");
    angle.addEventListener("input", () => {
        delete cards[3].dataset.result;
        report("quantum-outcome", () => "");
        updateTilt();
    });
    for (const [button, shots] of [[measure, 1], [sample, 100]]) {
        button.addEventListener("click", () => {
            delete cards[3].dataset.result;
            updateTilt();
            run({
                url: "/run-coin-lab", data: { tilt_degrees: Number(angle.value), shots },
                output: "quantum-outcome", buttons: [angle, measure, sample],
                onResult(result) {
                    const one = result.counts["1"] || 0;
                    if (shots === 1) {
                        cards[3].dataset.result = String(one);
                        updateTilt();
                    }
                    report("quantum-outcome", words => shots === 1
                        ? `${words.outcome}: ${one}`
                        : `${words.observed}: 0: ${100 - one}% · 1: ${one}%`);
                }
            });
        });
    }

    const pairOnce = byId("coin-pair-once");
    const pairRun = byId("coin-pair-run");
    for (const [button, shots] of [[pairOnce, 1], [pairRun, 100]]) {
        button.addEventListener("click", () => {
            delete cards[4].dataset.result;
            run({
                url: "/run-entanglement", data: { shots }, output: "pair-outcome",
                buttons: [pairOnce, pairRun],
                onResult({ counts }) {
                    if (shots === 1) {
                        const outcome = Object.keys(counts)[0];
                        if (outcome === "00" || outcome === "11") cards[4].dataset.result = outcome[0];
                        report("pair-outcome", words => `${words.outcome}: ${outcome}`);
                    } else {
                        report("pair-outcome", words => `${words.observed}: ${["00", "01", "10", "11"]
                            .map(state => `${state}: ${counts[state] || 0}%`).join(" · ")}`);
                    }
                }
            });
        });
    }
    picker.addEventListener("change", applyLanguage);
    applyLanguage();
})();
