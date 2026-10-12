// MapLibre map component for stories, using the same base map and OBIS occurrence
// grid as the maps on the rest of the website. Requires the global `maplibregl`
// (loaded by the story layout).
//
//   const m = await storyMap("#my-map", {
//       filter: { scientificname: "Thunnus albacares" },   // OBIS occurrence filters
//       center: [0, 20], zoom: 1,
//   });
//   m.flyTo({ center: [-30, 10], zoom: 3 });
//   m.setFilter({ scientificname: "Thunnus obesus" });
//
// Options
//   filter        OBIS occurrence API filters. Omit (or pass null) for no occurrence layer.
//   center, zoom, bearing, pitch   initial camera
//   height        CSS height, default "500px"
//   numbers       show record counts on the grid cells (default false)
//   legend        show the records legend (default true when there is a filter)
//   interactive   "click" (default: scroll/drag enabled after first click), true, or false
//   points        GeoJSON FeatureCollection (or URL) drawn as circles, e.g. stations
//   pointStyle    paint overrides for the circle layer
//   popup         (feature) => html string, shown when a point is clicked
//   layers        extra raw MapLibre { source: {id, ...spec}, layer: {...} } pairs
//   onLoad        (map) => void, runs once the map is ready
// Returns { map, ready, flyTo, fitBounds, setFilter, setPoints }.
import { resolveTarget } from "./dom.js";

const TILE_URL = "https://api.obis.org/occurrence/tile/{x}/{y}/{z}.mvt";
const OCCURRENCE_SOURCE = "story-occurrence";
const POINTS_SOURCE = "story-points";

const baseStyle = {
    version: 8,
    glyphs: "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",
    sources: {
        land_polygons: {
            type: "vector",
            tiles: ["https://tiles.obis.org/land_tiles/{z}/{x}/{y}.pbf"],
            minzoom: 0,
            maxzoom: 14
        },
        gebco_filtered: {
            type: "vector",
            tiles: ["https://tiles.obis.org/gebco_filtered_tiles/{z}/{x}/{y}.pbf"],
            minzoom: 0,
            maxzoom: 14
        }
    },
    layers: [
        { id: "background", type: "background", paint: { "background-color": "#dbdbdc" } },
        {
            id: "land_polygons",
            type: "fill",
            source: "land_polygons",
            "source-layer": "land",
            paint: { "fill-color": "#fcfcfd", "fill-opacity": 1.0 }
        },
        {
            id: "contours",
            type: "line",
            source: "gebco_filtered",
            "source-layer": "gebco_filtered",
            paint: { "line-color": "#044062", "line-width": 0.2, "line-opacity": 0.33 }
        }
    ]
};

const legendSteps = [
    ["#2c7bb6", "1"],
    ["#abd9e9", "10"],
    ["#ffffbf", "100"],
    ["#fdae61", "1,000"],
    ["#d7191c", "&gt;10,000"]
];

const tileUrl = (filter) => `${TILE_URL}?${new URLSearchParams(filter)}`;

export async function storyMap(target, options = {}) {
    const container = resolveTarget(target);
    if (!container) return;

    const {
        filter = null,
        center = [0, 25],
        zoom = 1,
        bearing = 0,
        pitch = 0,
        height = "500px",
        numbers = false,
        legend = !!filter,
        interactive = "click",
        points = null,
        pointStyle = {},
        popup = null,
        layers = [],
        onLoad = null
    } = options;

    const id = "story_map_" + Math.random().toString(36).slice(2, 11);
    container.classList.add("story-map");
    container.innerHTML = `
        <div class="map-container" style="height: ${height}; width: 100%; position: relative;">
            <div id="${id}" style="height: 100%; width: 100%"></div>
            ${legend ? `<div class="map-legend"><p>Records</p>${legendSteps
                .map(([color, label]) => `<div><span style="background:${color};margin-right:6px;"></span>${label}</div>`)
                .join("")}</div>` : ""}
            ${interactive === "click" ? `<div class="map-click-message">Click the map to<br/>start interacting</div>` : ""}
        </div>
    `;

    const map = new maplibregl.Map({
        container: id,
        style: baseStyle,
        center, zoom, bearing, pitch,
        projection: "mercator",
        attributionControl: false,
        scrollZoom: interactive === true,
        dragPan: interactive === true,
        interactive: interactive !== false
    });

    if (interactive === "click") {
        map.once("click", () => {
            map.scrollZoom.enable();
            map.dragPan.enable();
            container.querySelector(".map-click-message")?.remove();
        });
    }

    const ready = new Promise((resolve) => map.on("load", resolve));
    await ready;

    function addOccurrences(currentFilter) {
        map.addSource(OCCURRENCE_SOURCE, { type: "vector", tiles: [tileUrl(currentFilter)], scheme: "xyz" });
        map.addLayer({
            id: `${OCCURRENCE_SOURCE}-fill`,
            type: "fill",
            source: OCCURRENCE_SOURCE,
            "source-layer": "grid",
            paint: {
                "fill-color": [
                    "interpolate", ["linear"], ["get", "doc_count"],
                    0, "#2c7bb6", 10, "#abd9e9", 100, "#ffffbf", 1000, "#fdae61", 10000, "#d7191c"
                ],
                "fill-opacity": 0.8
            }
        });
        if (numbers) {
            map.addLayer({
                id: `${OCCURRENCE_SOURCE}-numbers`,
                type: "symbol",
                source: OCCURRENCE_SOURCE,
                "source-layer": "grid",
                layout: { "text-field": ["to-string", ["get", "doc_count"]], "text-size": 10, "text-anchor": "center" },
                paint: { "text-color": "#000000", "text-halo-color": "#ffffff", "text-halo-width": 1 }
            });
        }
    }

    async function setPoints(data) {
        if (typeof data === "string") data = await (await fetch(data)).json();
        const source = map.getSource(POINTS_SOURCE);
        if (source) return source.setData(data);

        map.addSource(POINTS_SOURCE, { type: "geojson", data });
        map.addLayer({
            id: `${POINTS_SOURCE}-circles`,
            type: "circle",
            source: POINTS_SOURCE,
            paint: {
                "circle-radius": 6,
                "circle-color": "#e8590c",
                "circle-stroke-color": "#ffffff",
                "circle-stroke-width": 1.5,
                ...pointStyle
            }
        });

        if (popup) {
            const layer = `${POINTS_SOURCE}-circles`;
            map.on("click", layer, (e) => {
                const feature = e.features[0];
                new maplibregl.Popup({ closeButton: false })
                    .setLngLat(feature.geometry.coordinates.slice())
                    .setHTML(popup(feature))
                    .addTo(map);
            });
            map.on("mouseenter", layer, () => (map.getCanvas().style.cursor = "pointer"));
            map.on("mouseleave", layer, () => (map.getCanvas().style.cursor = ""));
        }
    }

    if (filter) addOccurrences(filter);
    if (points) await setPoints(points);
    for (const { source, layer } of layers) {
        const { id: sourceId, ...spec } = source;
        if (!map.getSource(sourceId)) map.addSource(sourceId, spec);
        map.addLayer({ source: sourceId, ...layer });
    }

    map.addControl(new maplibregl.ScaleControl({ maxWidth: 100, unit: "metric" }), "bottom-left");
    map.addControl(new maplibregl.FullscreenControl(), "bottom-left");

    if (onLoad) onLoad(map);

    return {
        map,
        ready,
        flyTo: (opts) => map.flyTo({ essential: true, ...opts }),
        fitBounds: (bounds, opts) => map.fitBounds(bounds, { padding: 40, ...opts }),
        setPoints,
        // Swap the OBIS occurrence filter without recreating the map.
        setFilter(newFilter) {
            const source = map.getSource(OCCURRENCE_SOURCE);
            if (source) source.setTiles([tileUrl(newFilter)]);
            else addOccurrences(newFilter);
        }
    };
}
