(() => {
    const root = document.documentElement;
    const defaultTheme = root.getAttribute("data-theme") || "system";
    const validThemes = ["light", "dark", "system"];
    let storedTheme;
    try { storedTheme = localStorage.getItem("theme"); } catch (_) { /* Storage can be disabled. */ }

    function applyTheme(theme, persist = false) {
        if (!validThemes.includes(theme)) theme = defaultTheme;
        if (theme === "system") root.removeAttribute("data-theme");
        else root.setAttribute("data-theme", theme);

        if (persist) {
            try { localStorage.setItem("theme", theme); } catch (_) { /* Keep the in-memory choice. */ }
        }
        const light = document.getElementById("giallo-light");
        const dark = document.getElementById("giallo-dark");
        if (light && dark) {
            light.media = theme === "system" ? "(prefers-color-scheme: light)" : theme === "light" ? "all" : "not all";
            dark.media = theme === "system" ? "(prefers-color-scheme: dark)" : theme === "dark" ? "all" : "not all";
        }
        const icon = document.querySelector("#theme-switcher summary .icon");
        icon?.classList.toggle("light", theme === "light");
        icon?.classList.toggle("dark", theme === "dark");
        for (const name of validThemes) {
            const button = document.getElementById(`theme-${name}`);
            button?.classList.toggle("active", name === theme);
            button?.setAttribute("aria-pressed", String(name === theme));
        }
    }

    for (const theme of validThemes) {
        document.getElementById(`theme-${theme}`)?.addEventListener("click", () => applyTheme(theme, true));
    }
    applyTheme(validThemes.includes(storedTheme) ? storedTheme : defaultTheme);
    window.switchTheme = theme => applyTheme(theme, true);
})();
