(() => {
    const root = document.documentElement;
    const key = "qspark-theme";
    try {
        if (localStorage.getItem(key) === "light") root.dataset.theme = "light";
    } catch {
        // The toggle still works for this page when storage is unavailable.
    }

    document.addEventListener("DOMContentLoaded", () => {
        const picker = document.getElementById("languageSelect");
        const button = document.querySelector(".theme-toggle");
        const labels = {
            en: ["Light mode", "Dark mode"],
            kn: ["ಬೆಳಕಿನ ಮೋಡ್", "ಕತ್ತಲೆಯ ಮೋಡ್"],
            te: ["లైట్ మోడ్", "డార్క్ మోడ్"],
            hi: ["लाइट मोड", "डार्क मोड"]
        };

        function render() {
            const light = root.dataset.theme === "light";
            const words = labels[picker.value] || labels.en;
            button.textContent = words[Number(light)];
        }

        button.addEventListener("click", () => {
            const light = root.dataset.theme !== "light";
            if (light) root.dataset.theme = "light";
            else delete root.dataset.theme;
            try {
                localStorage.setItem(key, light ? "light" : "dark");
            } catch {
                // The current page keeps the selected theme.
            }
            render();
        });
        picker.addEventListener("change", render);
        render();
    });
})();
