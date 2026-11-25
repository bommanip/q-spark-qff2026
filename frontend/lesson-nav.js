(() => {
    const back = document.querySelector("[data-course-back]");
    const moduleNumber = Number(document.body.dataset.module);
    const names = {
        en: ["Learning Journey", "Quantum Arcade", "Modules", "Module", "Previous", "Next", "All modules"],
        kn: ["ಕಲಿಕೆಯ ಪಯಣ", "ಕ್ವಾಂಟಮ್ ಆರ್ಕೇಡ್", "ಘಟಕಗಳು", "ಘಟಕ", "ಹಿಂದಿನದು", "ಮುಂದಿನದು", "ಎಲ್ಲ ಘಟಕಗಳು"],
        te: ["అభ్యాస ప్రయాణం", "క్వాంటం ఆర్కేడ్", "మాడ్యూల్స్", "మాడ్యూల్", "మునుపటిది", "తదుపరిది", "అన్ని మాడ్యూల్స్"],
        hi: ["सीखने का सफ़र", "क्वांटम आर्केड", "मॉड्यूल", "मॉड्यूल", "पिछला", "अगला", "सभी मॉड्यूल"]
    };

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

    document.getElementById("languageSelect").addEventListener("change", render);
    render();
})();
