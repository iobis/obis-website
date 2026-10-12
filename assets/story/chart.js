// Observable Plot chart component for stories.
//
//   chart("#my-chart", {
//       data: obisApi("/statistics/years", { scientificname: "Thunnus albacares" }),
//       plot: (data, { Plot, width }) => ({
//           marks: [Plot.lineY(data, { x: "year", y: "records" })]
//       })
//   });
//
// `data`  array, promise, function or URL (.json / .csv / API endpoint).
// `plot`  receives (data, { Plot, width }) and returns either Plot.plot() options
//         (width is filled in for you) or a ready DOM element (Plot.plot(...), d3, etc.).
// `height`  optional, forwarded to Plot when `plot` returns options.
// Returns { update(newData), redraw(), element }.
import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
import { loadData } from "./data.js";
import { resolveTarget } from "./dom.js";

export { Plot };

export async function chart(target, { data, plot, height, minHeight = 260 }) {
    const container = resolveTarget(target);
    if (!container) return;

    container.classList.add("story-chart");
    container.style.minHeight = `${height || minHeight}px`;
    container.innerHTML = `<div class="story-status">Loading…</div>`;

    let rows;
    let lastWidth = 0;

    function draw() {
        if (rows === undefined) return;
        const width = container.clientWidth;
        lastWidth = width;

        let output = plot(rows, { Plot, width });
        if (!(output instanceof Node)) {
            output = Plot.plot({ width, ...(height && { height }), ...output });
        }
        container.replaceChildren(output);
    }

    try {
        rows = await loadData(data);
        draw();
    } catch (error) {
        console.error(error);
        container.innerHTML = `<div class="story-status">This chart could not be loaded.</div>`;
        return;
    }

    // Redraw when the available width changes (window resize, orientation change)
    new ResizeObserver(() => {
        if (container.clientWidth !== lastWidth) draw();
    }).observe(container);

    return {
        element: container,
        redraw: draw,
        update(newData) {
            rows = newData;
            draw();
        }
    };
}
