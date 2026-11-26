(() => {
    const pages = ["module1", "module2", "module3", "module4", "module5", "coin-lab", "linked-dice", "treasure-hunt"];
    const labels = {
        en: ["Concept guide", "How to play", "Play audio", "Pause audio", "Audio couldn’t play. Read the explanation below."],
        kn: ["ಪರಿಕಲ್ಪನೆಯ ವಿವರಣೆ", "ಆಡುವ ವಿಧಾನ", "ವಿವರಣೆ ಕೇಳಿ", "ವಿವರಣೆಯನ್ನು ತಡೆಹಿಡಿಯಿರಿ", "ಧ್ವನಿ ಪ್ಲೇ ಆಗಲಿಲ್ಲ. ಕೆಳಗಿನ ವಿವರಣೆಯನ್ನು ಓದಿ."],
        te: ["భావన వివరణ", "ఎలా ఆడాలి", "వివరణ వినండి", "వివరణను ఆపండి", "ఆడియో ప్లే కాలేదు. కింది వివరణ చదవండి."],
        hi: ["अवधारणा की व्याख्या", "कैसे खेलें", "ऑडियो सुनें", "ऑडियो रोकें", "ऑडियो नहीं चल पाया। नीचे दी गई व्याख्या पढ़ें।"]
    };
    let activeAudio;

    const players = [...document.querySelectorAll(".page-narration")].map(guide => {
        const page = guide.dataset.narrationPage;
        const concept = guide.dataset.narrationConcept;
        const conceptHeading = concept && document.getElementById(guide.dataset.conceptHeading);
        const index = pages.indexOf(page);
        const key = concept || page;
        const audio = guide.querySelector("audio");
        const heading = guide.querySelector("h3");
        const button = guide.querySelector("button");
        const caption = guide.querySelector(".narration-caption");
        const status = guide.querySelector(".narration-status");
        let language;

        function renderButton() {
            const label = labels[language][audio.paused ? 2 : 3];
            button.textContent = label;
            if (conceptHeading) button.setAttribute("aria-label", `${label}: ${conceptHeading.textContent.trim()}`);
        }

        function applyLanguage() {
            const requested = document.documentElement.lang;
            const next = Object.hasOwn(labels, requested) ? requested : "en";
            if (language === next) return;
            language = next;
            audio.pause();
            audio.src = `narration/audio/${language}-${key}.mp3`;
            heading.textContent = labels[language][concept || index < 5 ? 0 : 1];
            caption.textContent = concept ? conceptNarration[concept][language] : pageNarration[language][index];
            status.textContent = "";
            renderButton();
        }

        button.addEventListener("click", async () => {
            if (!audio.paused) {
                audio.pause();
                return;
            }
            if (activeAudio && activeAudio !== audio) activeAudio.pause();
            activeAudio = audio;
            const source = audio.src;
            status.textContent = "";
            try {
                await audio.play();
            } catch (error) {
                if (audio.src === source && error.name !== "AbortError") status.textContent = labels[language][4];
            }
        });
        for (const event of ["play", "pause", "ended"]) audio.addEventListener(event, renderButton);
        applyLanguage();
        guide.hidden = false;
        return applyLanguage;
    });

    window.addEventListener("pagehide", () => activeAudio?.pause());
    new MutationObserver(() => players.forEach(update => update())).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["lang"]
    });
})();
