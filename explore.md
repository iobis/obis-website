---
layout: page
title: Explore
---

<script src="/assets/maplibre-gl.js"></script>
<link href="/assets/maplibre-gl.css" rel="stylesheet" />
<script src="https://cdn.plot.ly/plotly-3.0.1.min.js" charset="utf-8"></script>
<script src="/assets/script.js"></script>

<section class="section-superdense">
  <div class="container">
    <h2>Explore occurrences</h2>
    <div id="applied-filters" class="mb-3"></div>
    <div id="m"></div>

    <div class="row">
        <div id="occurrences"></div>
    </div>

    <div class="row align-items-center">
        <div class="col-12 col-md-6">
            <div id="timeplot"></div>
        </div>
        <div class="col-12 col-md-6">
            <div id="sunburst" style="height: 600px;"></div>
        </div>
    </div>

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

renderOccurrenceTable("occurrences", "/occurrence", params);
fetchTaxonomy(params).then(convertToSunburst).then((data) => {
    var layout = {
        margin: {l: 0, r: 0, b: 30, t: 30},
        sunburstcolorway: ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]
        // sunburstcolorway: ["#54bebe", "#76c8c8", "#98d1d1", "#badbdb", "#dedad2", "#e4bcad", "#df979e", "#d7658b", "#c80064"]
    };
    Plotly.newPlot("sunburst", data, layout);
});
renderTimeplot("timeplot", params);
</script>
