(() => {
    const links = [...document.querySelectorAll(".home-nav a")];
    const coinLink = links.find(link => link.hash === "#coin");
    const coinTitle = document.getElementById("coin-lesson-title");
    const audio = document.querySelector("#coin audio");

    function highlightNavigation() {
        const hash = location.hash || "#home";
        for (const link of links) {
            if (link.hash === hash) link.setAttribute("aria-current", "location");
            else link.removeAttribute("aria-current");
        }
    }

    function syncCoinLabel() {
        coinLink.textContent = coinTitle.textContent;
    }

    links.forEach(link => link.addEventListener("click", () => {
        if (link !== coinLink) audio.pause();
    }));
    window.addEventListener("hashchange", highlightNavigation);
    new MutationObserver(syncCoinLabel).observe(coinTitle, { childList: true });
    highlightNavigation();
    syncCoinLabel();
})();
