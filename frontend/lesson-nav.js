(() => {
    const back = document.querySelector("[data-course-back]");
    const moduleNumber = Number(document.body.dataset.module);
    const names = {
        en: ["Learning Journey", "Quantum Arcade", "Modules", "Module", "Previous", "Next", "All modules"],
        kn: ["ಕಲಿಕೆಯ ಪಯಣ", "ಕ್ವಾಂಟಮ್ ಆರ್ಕೇಡ್", "ಘಟಕಗಳು", "ಘಟಕ", "ಹಿಂದಿನದು", "ಮುಂದಿನದು", "ಎಲ್ಲ ಘಟಕಗಳು"],
        te: ["అభ్యాస ప్రయాణం", "క్వాంటం ఆర్కేడ్", "మాడ్యూల్స్", "మాడ్యూల్", "మునుపటిది", "తదుపరిది", "అన్ని మాడ్యూల్స్"],
        hi: ["सीखने का सफ़र", "क्वांटम आर्केड", "मॉड्यूल", "मॉड्यूल", "पिछला", "अगला", "सभी मॉड्यूल"]
    };

    const statsLabels = {
        en: ["Learning Concepts", "Interactive Activities", "Quiz Questions"],
        kn: ["ಕಲಿಕೆಯ ವಿಷಯಗಳು", "ಸಂವಾದಾತ್ಮಕ ಚಟುವಟಿಕೆಗಳು", "ರಸಪ್ರಶ್ನೆಯ ಪ್ರಶ್ನೆಗಳು"],
        te: ["అభ్యాస అంశాలు", "ఇంటరాక్టివ్ కార్యకలాపాలు", "క్విజ్ ప్రశ్నలు"],
        hi: ["सीखने के विषय", "इंटरैक्टिव गतिविधियाँ", "क्विज़ के प्रश्न"]
    };

    function renderStats() {
        const locale = document.documentElement.lang;
        const labels = statsLabels[locale] || statsLabels.en;
        const number = new Intl.NumberFormat(locale);
        const badges = [
            ["📘", "[data-course-concept]"],
            ["⚡", "[data-course-activity]"],
            ["📝", ".course-question"]
        ];
        document.querySelector(".course-stats").replaceChildren(...badges.map(([icon, selector], index) => {
            const badge = document.createElement("li");
            const decoration = document.createElement("span");
            decoration.setAttribute("aria-hidden", "true");
            decoration.textContent = icon;
            const count = document.querySelectorAll(selector).length;
            const label = locale === "en" && count === 1 ? ["Learning Concept", "Interactive Activity", "Quiz Question"][index] : labels[index];
            badge.append(decoration, ` ${number.format(count)} ${label}`);
            return badge;
        }));
    }

    function link(href, text) {
        const anchor = document.createElement("a");
        anchor.href = href;
        anchor.textContent = text;
        return anchor;
    }

    function render() {
        const [journey, arcade, modules, module, previous, next, all] =
            names[document.documentElement.lang] || names.en;
        back.textContent = "← " + (moduleNumber ? journey : arcade);
        if (!moduleNumber) return;
        renderStats();

        const jump = document.querySelector(".module-jump");
        jump.setAttribute("aria-label", modules);
        jump.replaceChildren(...Array.from({ length: 5 }, (_, index) => {
            const number = index + 1;
            const anchor = link(`module${number}.html`, `${module} ${number}`);
            if (number === moduleNumber) anchor.setAttribute("aria-current", "page");
            return anchor;
        }));

        const pager = document.querySelector(".module-pager");
        pager.setAttribute("aria-label", modules);
        const backLink = moduleNumber > 1
            ? link(`module${moduleNumber - 1}.html`, `← ${previous}: ${module} ${moduleNumber - 1}`)
            : link("index.html#modules", `← ${all}`);
        const nextLink = moduleNumber < 5
            ? link(`module${moduleNumber + 1}.html`, `${next}: ${module} ${moduleNumber + 1} →`)
            : link("index.html#modules", `${all} →`);
        pager.replaceChildren(backLink, nextLink);
    }

    new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    render();
})();
