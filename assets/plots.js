import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6.17/+esm";

const compactFormat = new Intl.NumberFormat("en", {
    notation: "compact",
    maximumFractionDigits: 1,
}).format;

const TIER_COLORS = [
    "var(--tier-1)", "var(--tier-2)", "var(--tier-3)", "var(--tier-4)",
    "var(--tier-5)", "var(--tier-6)", "var(--tier-7)", "var(--tier-8)"
];

function resolveContainer(container) {
    return typeof container === "string" ? document.getElementById(container) : container;
}

// Zips parallel channel arrays ({x: [...], y: [...], fill: [...]}) into row
// objects, since Plot's marks expect a data array of objects with field names.
function toRows(channels) {
    const keys = Object.keys(channels);
    const length = channels[keys[0]].length;
    return Array.from({ length }, (_, i) => Object.fromEntries(keys.map((key) => [key, channels[key][i]])));
}

// Fills gaps in a sparse series (e.g. one row per year that actually
// changed) so every integer x in range has a row, carrying the last known y
// forward (0 before the first data point). For a cumulative count, a missing
// x means "unchanged", not "unknown" — plotting the sparse series as-is
// leaves a visual gap where there should be a flat run. Range defaults to
// [min(x), max(x)] in the data; pass `from`/`to` to force a shared range
// (e.g. across several series that should line up on the same axis).
export function fillCumulativeGaps({ x, y, from, to }) {
    const known = new Map(x.map((xi, i) => [xi, y[i]]));
    const start = from ?? Math.min(...x);
    const end = to ?? Math.max(...x);

    const filledX = [];
    const filledY = [];
    let last = 0;
    for (let xi = start; xi <= end; xi++) {
        if (known.has(xi)) last = known.get(xi);
        filledX.push(xi);
        filledY.push(last);
    }
    return { x: filledX, y: filledY };
}

function buildLegend(domain, colors) {
    const legend = document.createElement("div");
    legend.className = "plot-legend";
    domain.forEach((label, i) => {
        const item = document.createElement("span");
        item.className = "plot-legend-item";

        const swatch = document.createElement("span");
        swatch.className = "plot-legend-swatch";
        swatch.style.background = colors[i % colors.length];

        const text = document.createElement("span");
        text.textContent = label;

        item.append(swatch, text);
        legend.append(item);
    });
    return legend;
}

// Vertical bar chart for a quantitative x (e.g. year, month) against a count.
export function BarChart(container, { x, y, xLabel, yLabel, format = compactFormat, height = 320 }) {
    const el = resolveContainer(container);
    if (!el) return;
    const data = toRows({ x, y });

    const plot = Plot.plot({
        width: el.clientWidth,
        height,
        marginLeft: 56,
        style: { background: "transparent", fontFamily: "inherit" },
        x: { label: xLabel, tickFormat: "d" },
        y: { label: yLabel, grid: true, tickFormat: format },
        marks: [
            Plot.ruleY([0], { stroke: "var(--light-grey)" }),
            // explicit x1/x2 centers each bar on its own value, so a gap
            // between sparse x values still renders as a real gap
            Plot.rectY(data, {
                x1: (d) => d.x - 0.5,
                x2: (d) => d.x + 0.5,
                y: "y",
                fill: "var(--highlight)",
                rx: 3
            }),
            Plot.tip(data, Plot.pointerX({ x: "x", y: "y", format: { x: "d", y: format } }))
        ]
    });

    el.replaceChildren(plot);
    return plot;
}

// Horizontal 100%-style stacked bar(s) showing a composition, e.g. the share
// of records identified down to each taxonomic rank. `x` is the magnitude,
// `fill` the stack segment's category, and `y` which row it belongs to — pass
// a constant `y` (e.g. all "") for a single bar, or several distinct values
// to compare compositions across multiple rows in one chart.
export function StackedHorizontal(container, { x, y, fill, domain, xLabel, format = compactFormat, height, legend = true }) {
    const el = resolveContainer(container);
    if (!el) return;
    const order = domain ?? [...new Set(fill)];

    // Resolve each row's color ourselves rather than leaving it to Plot's
    // `color` scale: Plot only infers an ordinal color scale when a fill
    // channel has 2+ distinct values. With exactly one category present (a
    // real case here — a dataset can be 100% a single depth-coverage bucket)
    // it falls back to using the raw category string as a literal CSS color,
    // which is invalid and renders invisibly. Passing a precomputed color
    // string per row sidesteps that inference entirely.
    const colorOf = (category) => TIER_COLORS[order.indexOf(category) % TIER_COLORS.length];
    const data = toRows({ x, y, fill, color: fill.map(colorOf) });
    const rows = [...new Set(y)];
    const multiRow = rows.length > 1;
    const present = new Set(fill);

    const plot = Plot.plot({
        width: el.clientWidth,
        height: height ?? (multiRow ? rows.length * 36 + 30 : 90),
        marginLeft: multiRow ? 100 : 8,
        marginRight: 8,
        style: { background: "transparent", fontFamily: "inherit" },
        x: { label: xLabel, grid: true, tickFormat: format },
        y: { axis: multiRow ? "left" : null, label: null },
        marks: [
            Plot.barX(data, Plot.stackX({
                x: "x",
                y: "y",
                fill: "color",
                order,
                insetLeft: 1,
                insetRight: 1,
                rx: 2,
                tip: true,
                title: (d) => `${d.fill}: ${format(d.x)}`
            }))
        ]
    });

    const wrap = document.createElement("div");
    wrap.append(plot);
    // only show legend entries actually present in this chart's data, so it
    // doesn't list categories that have no visible segment in the bar
    const presentInOrder = order.filter((label) => present.has(label));
    if (legend) wrap.append(buildLegend(presentInOrder, presentInOrder.map(colorOf)));
    el.replaceChildren(wrap);
    return wrap;
}

// Small multiples: one step-area/line panel per group in `facet`, sharing
// scales so magnitudes stay comparable at a glance.
export function FacetedArea(container, { x, y, facet, xLabel, yLabel, format = compactFormat, panelWidth = 220, panelHeight = 140 }) {
    const el = resolveContainer(container);
    if (!el) return;
    const data = toRows({ x, y, facet });
    const groups = [...new Set(facet)];

    const xDomain = [Math.min(...x), Math.max(...x)];
    const yDomain = [0, Math.max(...y)];

    const grid = document.createElement("div");
    grid.className = "plot-facet-grid";

    for (const group of groups) {
        const panel = document.createElement("div");
        panel.className = "plot-facet-panel";

        const title = document.createElement("div");
        title.className = "plot-facet-title";
        title.textContent = group;

        const groupData = data.filter((d) => d.facet === group);

        const plot = Plot.plot({
            width: panelWidth,
            height: panelHeight,
            marginLeft: 40,
            style: { background: "transparent", fontFamily: "inherit", fontSize: "10px" },
            x: { domain: xDomain, ticks: 2, tickFormat: "d", label: xLabel },
            y: { domain: yDomain, ticks: 3, tickFormat: format, grid: true, label: yLabel },
            marks: [
                Plot.ruleY([0], { stroke: "var(--light-grey)" }),
                Plot.areaY(groupData, { x: "x", y: "y", curve: "step-after", fill: "var(--highlight)", fillOpacity: 0.15 }),
                Plot.lineY(groupData, { x: "x", y: "y", curve: "step-after", stroke: "var(--highlight)", strokeWidth: 2 }),
                Plot.tip(groupData, Plot.pointerX({ x: "x", y: "y", format: { x: "d", y: format } }))
            ]
        });

        panel.append(title, plot);
        grid.append(panel);
    }

    el.replaceChildren(grid);
    return grid;
}
