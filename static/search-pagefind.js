document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("search-container");
    const toggle = document.getElementById("search-toggle");
    const target = document.getElementById("pagefind-search");
    if (!container || !toggle || !target) return;

    let initialized = false;
    function initializeSearch() {
        if (initialized || typeof PagefindUI === "undefined") return;
        initialized = true;
        const observer = new MutationObserver(attachInput);
        function attachInput() {
            const input = target.querySelector("input");
            if (!input) return;
            input.id = "search-bar";
            input.setAttribute("autocomplete", "off");
            observer.disconnect();
            if (container.classList.contains("active")) input.focus();
        }
        observer.observe(target, {childList: true, subtree: true});
        new PagefindUI({
            element: "#pagefind-search",
            showSubResults: true,
            showImages: false,
            translations: {placeholder: target.dataset.placeholder || "Search"}
        });
        attachInput();
    }

    function setOpen(open, restoreFocus = false) {
        container.classList.toggle("active", open);
        container.inert = !open;
        toggle.setAttribute("aria-expanded", String(open));
        if (open) {
            initializeSearch();
            target.querySelector("input")?.focus();
        } else if (restoreFocus) {
            toggle.focus();
        }
    }

    toggle.addEventListener("click", () => setOpen(!container.classList.contains("active"), true));
    document.addEventListener("click", event => {
        if (!container.contains(event.target) && !toggle.contains(event.target)) setOpen(false);
    });
    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && container.classList.contains("active")) {
            event.preventDefault();
            setOpen(false, true);
        }
        const editing = event.target.closest?.("input, textarea, select, [contenteditable]:not([contenteditable='false'])");
        if (event.key === "/" && !editing && !event.ctrlKey && !event.metaKey && !event.altKey) {
            event.preventDefault();
            setOpen(true);
        }
    });
});
