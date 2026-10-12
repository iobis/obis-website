// Declarative story components, as custom HTML elements usable straight from Markdown.
// Loaded automatically by _layouts/story.html: no per-article script needed.
//
//   <obis-recs-by-year taxonid="127027"></obis-recs-by-year>
//   <obis-map taxonid="127027" center="0,10" zoom="1"></obis-map>
//   <obis-chart src="/data/foo.csv" mark="line" x="year" y="value" stroke="site"></obis-chart>
//
//   <obis-scrolly taxonid="127027" center="-35,5" zoom="2">
//     <obis-step center="75,5" zoom="3" markdown="1">Text, **Markdown** works.</obis-step>
//     <obis-step taxonid="127028" center="-140,5" zoom="2" markdown="1">Another species.</obis-step>
//   </obis-scrolly>
//
// OBIS filter attributes (any element): taxonid, scientificname, areaid, datasetid, nodeid,
// startdate, enddate, geometry, or `filter="key=value&key2=value2"` for any other API parameter.
// Always close the tag (</obis-map>); self-closing tags are not valid for custom elements.
import { chart } from "./chart.js";
import { storyMap } from "./map.js";
import { scroll } from "./scroll.js";
import { loadData, obisApi } from "./data.js";

const FILTER_ATTRIBUTES = ["taxonid", "scientificname", "areaid", "datasetid", "nodeid", "startdate", "enddate", "geometry"];

function filterOf(el, fallback = null) {
    const filter = {};
    for (const name of FILTER_ATTRIBUTES) {
        if (el.hasAttribute(name)) filter[name] = el.getAttribute(name);
    }
    if (el.hasAttribute("filter")) {
        for (const [key, value] of new URLSearchParams(el.getAttribute("filter"))) filter[key] = value;
    }
    return Object.keys(filter).length ? filter : fallback;
}

const num = (el, name, fallback) => (el.hasAttribute(name) ? Number(el.getAttribute(name)) : fallback);
const lonLat = (value, fallback) => (value ? value.split(",").map(Number) : fallback);

// Defines the element and guards against connectedCallback running twice.
function define(name, render) {
    customElements.define(name, class extends HTMLElement {
        connectedCallback() {
            if (this._rendered) return;
            this._rendered = true;
            render(this);
        }
    });
}

define("obis-recs-by-year", (el) => {
    const filter = filterOf(el) ?? {};
    const since = num(el, "startyear", 1950);
    const color = el.getAttribute("color") || "#2c7bb6";
    chart(el, {
        data: obisApi("/statistics/years", filter),
        height: num(el, "height", 320),
        plot: (data, { Plot }) => ({
            x: { label: "Year", tickFormat: "d" },
            y: { label: "Records", grid: true },
            marks: [
                Plot.rectY(data.filter(d => d.year >= since), { x: "year", y: "records", interval: 1, fill: color }),
                Plot.ruleY([0]),
                Plot.tip(data.filter(d => d.year >= since), Plot.pointerX({ x: "year", y: "records" }))
            ]
        })
    });
});

define("obis-chart", (el) => {
    const mark = { line: "lineY", bar: "barY", area: "areaY", dot: "dot", rect: "rectY" }[el.getAttribute("mark") || "line"];
    const x = el.getAttribute("x");
    const y = el.getAttribute("y");
    const series = el.getAttribute("stroke") || el.getAttribute("fill");
    const path = el.getAttribute("path");
    chart(el, {
        data: async () => {
            const data = await loadData(el.getAttribute("src"));
            return path ? path.split(".").reduce((d, key) => d?.[key], data) : data;
        },
        height: num(el, "height", 320),
        plot: (data, { Plot }) => ({
            x: { label: el.getAttribute("xlabel") ?? x },
            y: { label: el.getAttribute("ylabel") ?? y, grid: true },
            color: series ? { legend: true } : undefined,
            marks: [
                Plot[mark](data, {
                    x, y,
                    ...(mark === "barY" || mark === "rectY" ? { fill: series || "#2c7bb6" } : { stroke: series || "#2c7bb6" })
                }),
                Plot.tip(data, Plot.pointerX({ x, y }))
            ]
        })
    });
});

define("obis-map", (el) => {
    storyMap(el, {
        filter: filterOf(el),
        center: lonLat(el.getAttribute("center"), [0, 25]),
        zoom: num(el, "zoom", 1),
        height: el.getAttribute("height") || "500px",
        numbers: el.hasAttribute("numbers")
    });
});

define("obis-scrolly", async (el) => {
    const steps = [...el.querySelectorAll("obis-step")];
    const baseFilter = filterOf(el);
    const baseCenter = lonLat(el.getAttribute("center"), [0, 25]);
    const baseZoom = num(el, "zoom", 2);

    el.classList.add("story-scrolly", "story-wide");
    const sticky = document.createElement("div");
    sticky.className = "story-sticky";
    const mapTarget = document.createElement("div");
    sticky.append(mapTarget);
    const stepsBox = document.createElement("div");
    stepsBox.className = "story-steps";
    for (const step of steps) {
        step.classList.add("story-step");
        const card = document.createElement("div");
        card.className = "story-step-card";
        card.append(...step.childNodes);
        step.append(card);
        stepsBox.append(step);
    }
    el.replaceChildren(sticky, stepsBox);

    const map = await storyMap(mapTarget, {
        filter: baseFilter, center: baseCenter, zoom: baseZoom, interactive: false, height: "100vh"
    });

    let current = JSON.stringify(baseFilter);
    scroll(steps, (step) => {
        const filter = filterOf(step, baseFilter);
        if (filter && JSON.stringify(filter) !== current) {
            current = JSON.stringify(filter);
            map.setFilter(filter);
        }
        map.flyTo({
            center: lonLat(step.getAttribute("center"), baseCenter),
            zoom: num(step, "zoom", baseZoom),
            duration: 2000
        });
    });
});
