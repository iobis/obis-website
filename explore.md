---
layout: page
title: Search
---

<link href="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v3.12.0/mapbox-gl.js"></script>
<script src="/assets/script.js"></script>

<section class="section-superdense">
  <div class="container">
    <h2>Explore</h2>
    <div id="applied-filters" class="mb-3"></div>
    <div id="m"></div>
    <div id="occurrences"></div>
  </div>
</section>

<script>
function getUrlParams() {
    const params = {};
    for (const [key, value] of new URLSearchParams(window.location.search)) {
        params[key] = value;
    }
    return params;
}
const params = getUrlParams();
const filterDiv = document.getElementById("applied-filters");

if (Object.keys(params).length > 0) {
    filterDiv.innerHTML = "Filters: " + Object.entries(params).map(([k, v]) => `<span style="display:inline-block;background:#eee;border-radius:12px;padding:2px 10px;margin:2px 4px 2px 0;font-size:90%">${k}: ${v}</span>`).join(" ");
} else {
    filterDiv.innerHTML = "<span style='color:#888'>No filters applied</span>";
}
renderMap("m", params);

renderOccurrenceTable("occurrences", "/occurrence", params)
</script>
