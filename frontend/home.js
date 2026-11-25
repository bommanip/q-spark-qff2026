(() => {
    const tabs = [...document.querySelectorAll(".home-tabs [role=tab]")];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute("aria-controls")));
    const audio = panels[0].querySelector("audio");
    const navLinks = [...document.querySelectorAll(".home-nav a")];
    let activeTab = 0;
    const labels = {
        en: { coin: "Quantum Coin Trail", journey: "Learning Journey", arcade: "Quantum Arcade" },
        kn: { coin: "ಕ್ವಾಂಟಮ್ ನಾಣ್ಯದ ಪಯಣ", journey: "ಕಲಿಕೆಯ ಪಯಣ", arcade: "ಕ್ವಾಂಟಮ್ ಆರ್ಕೇಡ್" },
        te: { coin: "క్వాంటం నాణెం ప్రయాణం", journey: "అభ్యాస ప్రయాణం", arcade: "క్వాంటం ఆర్కేడ్" },
        hi: { coin: "क्वांटम सिक्के का सफ़र", journey: "सीखने का सफ़र", arcade: "क्वांटम आर्केड" }
    };

    function renderLabels() {
        const words = labels[document.documentElement.lang] || labels.en;
        for (const tab of tabs) tab.textContent = words[tab.dataset.homeLabel];
    }

    function select(index) {
        activeTab = index;
        if (index !== 0) audio.pause();
        tabs.forEach((tab, i) => {
            const active = i === index;
            tab.setAttribute("aria-selected", String(active));
            tab.tabIndex = active ? 0 : -1;
            panels[i].hidden = !active;
        });
    }

    function highlightNavigation(hash) {
        for (const link of navLinks) {
            if (link.hash === (hash === "#coin" || !hash ? "#home" : hash)) {
                link.setAttribute("aria-current", "location");
            } else {
                link.removeAttribute("aria-current");
            }
        }
    }

    function selectHash(hash) {
        highlightNavigation(hash);
        const index = panels.findIndex(panel => hash === "#" + panel.id);
        if (index !== -1) select(index);
        return index;
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            select(index);
            const hash = "#" + panels[index].id;
            history.replaceState(null, "", hash);
            highlightNavigation(hash);
        });
        tab.addEventListener("keydown", event => {
            const next = {
                ArrowLeft: (activeTab + tabs.length - 1) % tabs.length,
                ArrowRight: (activeTab + 1) % tabs.length,
                Home: 0,
                End: tabs.length - 1
            }[event.key];
            if (next === undefined) return;
            event.preventDefault();
            tabs[next].click();
            tabs[next].focus();
        });
    });

    document.addEventListener("click", event => {
        const link = event.target.closest("a[href^='#']");
        if (link) selectHash(link.hash);
    });
    window.addEventListener("hashchange", () => selectHash(location.hash));
    new MutationObserver(renderLabels).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    renderLabels();
    const linkedTab = selectHash(location.hash);
    if (linkedTab > 0) document.getElementById("learn-tabs").scrollIntoView();
})();
