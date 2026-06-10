// Giallo code block processing: line-number grid restructure, copy button, and table wrapping
document.addEventListener("DOMContentLoaded", function () {
	// --- Process all Giallo code blocks ---
	document.querySelectorAll("pre.giallo").forEach(block => {
		// Wrap in .pre-container for scrolling and visual chrome
		const container = document.createElement("div");
		container.className = "pre-container";
		block.parentNode.insertBefore(container, block);
		container.appendChild(block);

		// Restructure into a grid layout.
		// With line numbers: gutter column + code column side by side.
		// Without line numbers: code column only (same DOM structure for consistency).
		// This ensures that:
		//   1. Highlighted lines (.z-hl) only colour the code area, not the gutter
		//   2. The highlight background covers the full scrollable width
		//   3. Visual behaviour is consistent regardless of line numbers
		const code = block.querySelector("code");
		const lines = code ? code.querySelectorAll(".giallo-l") : [];
		const hasLineNumbers = code && code.querySelector(".giallo-ln");

		if (lines.length > 0) {
			const lineNumsCol = document.createElement("div");
			lineNumsCol.className = "giallo-gutter";
			if (hasLineNumbers) {
				lineNumsCol.setAttribute("aria-hidden", "true");
			}

			const codeCol = document.createElement("div");
			codeCol.className = "giallo-code";

			lines.forEach(line => {
				// Gutter cell
				const gutterSpan = document.createElement("span");
				gutterSpan.className = "giallo-gutter-ln";
				const ln = line.querySelector(".giallo-ln");
				if (ln) {
					gutterSpan.textContent = ln.textContent;
				}

				// Code cell
				const codeSpan = document.createElement("span");
				codeSpan.classList.add("giallo-code-l");
				if (line.classList.contains("z-hl")) {
					codeSpan.classList.add("z-hl");
				}

				line.childNodes.forEach(child => {
					if (!(child.classList && child.classList.contains("giallo-ln"))) {
						codeSpan.appendChild(child.cloneNode(true));
					}
				});

				lineNumsCol.appendChild(gutterSpan);
				codeCol.appendChild(codeSpan);
			});

			const grid = document.createElement("div");
			grid.className = "giallo-grid";
			if (!hasLineNumbers) {
				grid.classList.add("giallo-grid--no-gutter");
			}
			grid.appendChild(lineNumsCol);
			grid.appendChild(codeCol);

			code.textContent = "";
			code.appendChild(grid);
		}

		// Copy button (only if clipboard API and label text exist)
		if (!navigator.clipboard) return;
		const copyLabel = document.getElementById("copy-code-text");
		if (!copyLabel) return;

		const title = document.createElement("span");
		const codeEl = block.querySelector("code");
		const name =
			codeEl?.getAttribute("data-name") ||
			block.getAttribute("data-name") ||
			codeEl?.getAttribute("data-lang") ||
			block.getAttribute("data-language");
		title.innerHTML = name || "";

		const icon = document.createElement("i");
		icon.classList.add("icon");

		const button = document.createElement("button");
		button.setAttribute("title", copyLabel.textContent);
		button.appendChild(icon);

		const header = document.createElement("div");
		header.classList.add("header");
		if (title.innerHTML) {
			header.appendChild(title);
		}
		header.appendChild(button);

		container.insertBefore(header, block);

		button.addEventListener("click", async () => {
			const codeEl = block.querySelector("code");
			await navigator.clipboard.writeText(codeEl.innerText);

			header.classList.add("active");
			button.setAttribute("disabled", true);

			header.addEventListener("animationend", () => {
				header.classList.remove("active");
				button.removeAttribute("disabled");
			}, { once: true });
		});
	});

	// --- Wrap tables for responsive horizontal scrolling ---
	document.querySelectorAll("article table").forEach(table => {
		const wrapper = document.createElement("div");
		wrapper.className = "table-container";
		table.parentNode.insertBefore(wrapper, table);
		wrapper.appendChild(table);
	});
});