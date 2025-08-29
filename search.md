---
layout: page
title: Search
---

<div class="section-light">
    <h1 class="mb-4">Search</h1>
    <form class="row g-2 align-items-end mb-4" onsubmit="event.preventDefault(); performSearch();">
        <div class="col-md-2">
            <label for="entity" class="form-label">Search for</label>
            <select id="entity" class="form-select">
                <option value="dataset" selected>Dataset</option>
                <option value="taxon">Scientific name</option>
                <option value="common">Common name</option>
                <option value="area">Area</option>
                <option value="country">Publisher country</option>
            </select>
        </div>
        <div class="col-md-4">
            <label for="query" class="form-label">Search term</label>
            <input type="text" id="query" class="form-control" placeholder="Enter search term" value="">
        </div>
        <div class="col-md-2 d-grid">
            <button type="submit" class="btn">Search</button>
        </div>
    </form>
    <div id="dataset-search-help" class="mt-3">
        Dataset search syntax:
        <code>+</code> signifies AND operation,
        <code>|</code> signifies OR operation,
        <code>-</code> negates a single token,
        <code>"</code> wraps a number of tokens to signify a phrase for searching,
        <code>*</code> at the end of a term signifies a prefix query,
        <code>(</code> and <code>)</code> signify precedence.
    </div>
    <div id="results" class="mt-5"></div>
</div>

<script src="/assets/script.js"></script>
<script>
let currentSkip = 0;
const pageSize = 10;

const entityConfig = {
    dataset: {
        endpoint: 'dataset/search2',
        renderItem: renderDatasetItem
    },
    taxon: {
        endpoint: 'taxon/search',
        renderItem: renderTaxonItem
    },
    common: {
        endpoint: 'taxon/search/common',
        renderItem: renderTaxonItem
    },
    area: {
        endpoint: 'area/search',
        renderItem: renderAreaItem
    },
    country: {
        endpoint: 'country/search',
        renderItem: renderCountryItem
    }
};

async function performSearch(skip = 0) {
    currentSkip = skip;
    const entity = document.getElementById("entity").value;
    const query = document.getElementById("query").value.trim();
    
    if (!query) {
        const resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        return;
    }

    const encodedQuery = encodeURIComponent(query);
    const config = entityConfig[entity];
    if (!config) {
        console.error(`No configuration found for entity: ${entity}`);
        return;
    }

    const url = `https://api.obis.org/${config.endpoint}?q=${encodedQuery}&size=${pageSize}&skip=${skip}`;

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Searching...</p>";

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data && data.results && data.results.length > 0) {
            renderTable("results", data.results, data.total, skip, pageSize, config.renderItem, performSearch);
        } else {
            resultsDiv.innerHTML = "<p>No results found.</p>";
        }
    } catch (error) {
        resultsDiv.innerHTML = "<p>Error fetching results.</p>";
        console.error(error);
    }
}

function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function updateURL() {
    const entity = document.getElementById("entity").value;
    const query = document.getElementById("query").value.trim();
    const params = new URLSearchParams();
    if (entity && entity !== "dataset") {
        params.set("entity", entity);
    }
    if (query) {
        params.set("q", query);
    }
    const newURL = params.toString() ? `/search?${params.toString()}` : "/search";
    window.history.replaceState({}, "", newURL);
}

document.addEventListener('DOMContentLoaded', function() {
    const entityParam = getURLParameter('entity');
    const queryParam = getURLParameter('q');
    if (entityParam) {
        const entitySelect = document.getElementById('entity');
        entitySelect.value = entityParam;
    }
    if (queryParam) {
        const queryInput = document.getElementById('query');
        queryInput.value = queryParam;
    }
    if (queryParam) {
        performSearch();
    }

    var entitySelect = document.getElementById('entity');
    var helpBox = document.getElementById('dataset-search-help');
    if (entitySelect && helpBox) {
        function updateHelpBox() {
            if (entitySelect.value === 'dataset') {
                helpBox.style.display = '';
            } else {
                helpBox.style.display = 'none';
            }
        }
        entitySelect.addEventListener('change', updateHelpBox);
        updateHelpBox(); // Initial call
    }

    document.getElementById("entity").addEventListener("change", updateURL);
    document.getElementById("query").addEventListener("input", updateURL);
});

</script>

## Accessing OBIS data

OBIS harvests occurrence records from thousands of datasets and makes them available as a single integrated dataset. Read more about the ways you can access OBIS data [in the OBIS manual](https://manual.obis.org/access).

## Full exports

We provide periodic exports of the entire set of quality controlled presence records as GeoParquet and TSV. This is the easiest way to download data for large scale analyses. **Absence records and records of insufficient quality (for example, missing coordinates or ambiguous taxonomy) are not included. Use the API or the robis R package to access these data as well, or contact <a href="mailto:helpdesk@obis.org">helpdesk@obis.org</a>.** Each export includes a list of data licenses for the underlying datasets.

### GeoParquet

<button class="btn btn-primary" onclick="dl(this, 'https://obis-open-data.s3.amazonaws.com/snapshots/obis_20250318_parquet.zip')">Download</button>

This export contains two folders with parquet files, one for the Occurrence records and one for the (Extended)MeasurementOrFact records. Here's an example showing how the occurrence data can be queried using R and DuckDB:

```txt
library(DBI)

con <- dbConnect(duckdb::duckdb())
result <- dbGetQuery(con, "
    select * from read_parquet('occurrence/*.parquet')
    where genus == 'Abra'
")
dbDisconnect(con, shutdown = TRUE)
```

Here's an example of a spatial query:

```txt
con <- dbConnect(duckdb::duckdb())
result <- dbGetQuery(con, "
    install spatial;
    load spatial;
    select * from read_parquet('occurrence/*.parquet')
    where ST_Intersects(geometry, ST_GeomFromText('POLYGON ((2.831383 51.212045, 2.896957 51.212045, 2.896957 51.240211, 2.831383 51.240211, 2.831383 51.212045))'))
")
dbDisconnect(con, shutdown = TRUE)
```

### TSV

<button class="btn btn-primary" onclick="dl(this, 'https://obis-open-data.s3.amazonaws.com/snapshots/obis_20250318_tsv.zip')">Download</button>

In addition to GeoParquet, we also have a TSV export available. Note that these files are a lot larger and slower to work with compared to parquet. Here's an example in R that reads the occurrence TSV file in chunks and extracts the records of interest:

```txt
library(dplyr)
library(readr)

callback <- function(df, index) {
  df %>% filter(genus == "Abra")  
}

read_delim_chunked("occurrence.tsv", DataFrameCallback$new(callback), delim = "\t", progress = TRUE, col_types = cols(.default = "c"))
```

{% raw  %}
<script>
function dl(button, s3path) {
    button.disabled = true;
    $.get("https://api.obis.org/metrics/logusage?agent=full_export");
    window.open(s3path, "_blank");
};
</script>
{% endraw %}

### Fields

Each export contains occurrence table which includes all Darwin Core fields provided by the data providers as either Event or Occurrence records, with the exception of the fields below which have been transformed or added by the OBIS quality control pipeline.

{:.table .table-sm .table-striped}
| field | remarks |
| --- | --- |
| id | Globally unique identifier assigned by OBIS. |
| dataset_id | Internal dataset identifier assigned by OBIS. |
| decimalLongitude | Parsed and validated by OBIS. |
| decimalLatitude | Parsed and validated by OBIS. |
| date_start | Unix timestamp based on `eventDate` (start). |
| date_mid | Unix timestamp based on `eventDate` (middle). |
| date_end | Unix timestamp based on `eventDate` (end). |
| date_year | Year based on `eventDate`. |
| scientificName | Valid scientific name based on the `scientificNameID` or derived by matching the provided `scientificName` with WoRMS |
| originalScientificName | The `scientificName` as provided. |
| minimumDepthInMeters | Parsed and validated by OBIS. |
| maximumDepthInMeters | Parsed and validated by OBIS. |
| coordinateUncertaintyInMeters | Parsed and validated by OBIS. |
| flags | Quality flags added by OBIS. The quality flags are documented [here](https://github.com/iobis/obis-qc). |
| dropped | Record dropped by OBIS quality control? |
| absence | Absence record? |
| shoredistance | Distance from shore in meters added by OBIS quality control, based on OpenStreetMap. Negative value indicates that the observation was inland by -1 times that distance |
| bathymetry | Bathymetry added by OBIS. Bathymetry values based on EMODnet Bathymetry and GEBCO, see https://github.com/iobis/xylookup (Data references) |
| sst | Sea surface temperature added by OBIS. sst values based on Bio-Oracle, see https://github.com/iobis/xylookup (Data references) |
| sss | Sea surface salinity added by OBIS. sss values based on Bio-Oracle, see https://github.com/iobis/xylookup (Data references)|
| marine | Marine environment flag based on WoRMS. |
| brackish | Brackish environment flag based on WoRMS. |
| freshwater | Freshwater environment flag based on WoRMS. |
| terrestrial | Terrestrial environment flag based on WoRMS. |
| taxonRank | Based on WoRMS. |
| AphiaID | AphiaID for the valid name based on the `scientificNameID` or derived by matching the provided `scientificName` with WoRMS. |
| redlist_category | IUCN Red List category. |
| superdomain | Based on WoRMS. |
| domain | Based on WoRMS. |
| kingdom | Based on WoRMS. |
| subkingdom | Based on WoRMS. |
| infrakingdom | Based on WoRMS. |
| phylum | Based on WoRMS. |
| phylum (division) | Based on WoRMS. |
| subphylum (subdivision) | Based on WoRMS. |
| subphylum | Based on WoRMS. |
| infraphylum | Based on WoRMS. |
| parvphylum | Based on WoRMS. |
| gigaclass| Based on WoRMS. |
| megaclass | Based on WoRMS. |
| superclass | Based on WoRMS. |
| class | Based on WoRMS. |
| subclass | Based on WoRMS. |
| infraclass | Based on WoRMS. |
| subterclass | Based on WoRMS. |
| superorder | Based on WoRMS. |
| order | Based on WoRMS. |
| suborder | Based on WoRMS. |
| infraorder | Based on WoRMS. |
| parvorder | Based on WoRMS. |
| superfamily | Based on WoRMS. |
| family | Based on WoRMS. |
| subfamily | Based on WoRMS. |
| supertribe | Based on WoRMS. |
| tribe | Based on WoRMS. |
| subtribe | Based on WoRMS. |
| genus | Based on WoRMS. |
| subgenus | Based on WoRMS. |
| section | Based on WoRMS. |
| subsection | Based on WoRMS. |
| series | Based on WoRMS. |
| species | Based on WoRMS. |
| subspecies | Based on WoRMS. |
| natio | Based on WoRMS. |
| variety | Based on WoRMS. |
| subvariety | Based on WoRMS. |
| forma | Based on WoRMS. |
| subforma | Based on WoRMS. |


