---
identifier: access
lang: en
layout: page
shorttitle: Data access
title: Data access
---

# Data access

OBIS harvests occurrence records from thousands of datasets and makes them available as a single integrated dataset. This page gives an overview of the the different ways the integrated OBIS dataset can be accessed. There is also a section on data access [in the OBIS manual](https://manual.obis.org/access).

The recommended way to access OBIS data depends on the size of your subset and the way you intend to work with the data. For example, for a quick visual exploration of the data we recommend using the OBIS mapper or the search function, but for programmatic analysis of large subsets of data, the GeoParquet version of the dataset hosted on AWS is highly recommended. Note that downloading large datasets through the mapper or the R package is very slow and causes unnecessary load on the OBIS systems.

{:.table .table-nowrap-first}
| Method | Suitable for | Data format | Link |
|---|---|---|
| Mapper | Visual selection and download of smaller subsets | TSV | <https://mapper.obis.org> |
| Search | Visual exploration of datasets and taxa | - | <https://obis.org/search> |
| R package | Programmatic download of smaller subsets and checklists using R | Data frame | <https://github.org/iobis/robis> |
| API | Programmatic access to smaller subsets, checklists, and statistics | JSON | <https://api.obis.org> |
| AWS Open Data | Analysis of large subsets | GeoParquet | <https://github.com/iobis/obis-open-data> |
| Full exports | Analysis of large subsets, presence occurrences only <span class="badge bg-warning text-dark">Deprecated</span> | GeoParquet, CSV | See below |
| OBIS helpdesk | Contact the OBIS helpdesk if you are experiencing issues downloading or working with data | Any | <mailto:helpdesk@obis.org> |

All data exported from OBIS contains fields submitted by the data provider as well as fields added by OBIS during data ingestion. An overview of the data fields can be found below.

## Full exports

<span class="badge bg-warning text-dark">Deprecated</span>

We provide periodic exports of the entire set of quality controlled presence records as GeoParquet and TSV. This is the easiest way to download data for large scale analyses. Absence records and records of insufficient quality (for example, missing coordinates or ambiguous taxonomy) are not included.

#### GeoParquet

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

#### TSV

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

## Data fields

OBIS data exports include all Darwin Core fields provided by the data provider as either Event or Occurrence records, with the exception of the fields below which have been transformed or added by the OBIS quality control pipeline.

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


