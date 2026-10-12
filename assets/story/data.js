// Small data-loading helpers shared by the story components.
import { csvParse, autoType } from "https://cdn.jsdelivr.net/npm/d3-dsv@3/+esm";

// Resolves `source` to data. Accepts an array (returned as is), a promise,
// a function returning either, or a URL to a .json / .csv file or API endpoint.
export async function loadData(source) {
    if (typeof source === "function") source = source();
    source = await source;
    if (typeof source !== "string") return source;

    const response = await fetch(source);
    if (!response.ok) throw new Error(`HTTP error ${response.status} for ${source}`);
    if (/\.csv(\?|$)/i.test(source)) return csvParse(await response.text(), autoType);
    return response.json();
}

// Builds an OBIS API URL, e.g. obisApi("/statistics/years", { scientificname: "Thunnus albacares" })
export function obisApi(endpoint, params = {}) {
    return `https://api.obis.org${endpoint}?${new URLSearchParams(params)}`;
}
