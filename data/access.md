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
| R package | Programmatic download of smaller subsets and checklists using R<br><span class="alert alert-warning d-inline-block py-1 px-2 mt-1 mb-0"><strong>For large downloads:</strong> use the OBIS dataset on AWS Open Data. Do not parallelize downloads.</span> | Data frame | <https://github.com/iobis/robis> |
| API | Programmatic access to smaller subsets, checklists, and statistics<br><span class="alert alert-warning d-inline-block py-1 px-2 mt-1 mb-0"><strong>For large downloads:</strong> use the OBIS dataset on AWS Open Data. Do not parallelize downloads.</span> | JSON | <https://api.obis.org> |
| AWS Open Data | Analysis of large subsets | GeoParquet | <https://github.com/iobis/obis-open-data> |
| OBIS helpdesk | Contact the OBIS helpdesk if you are experiencing issues downloading or working with data | Any | <mailto:helpdesk@obis.org> |

All data exported from OBIS contains fields submitted by the data provider as well as fields added by OBIS during data ingestion. An overview of the data fields can be found below.

## Data fields

OBIS data exports include all Darwin Core fields provided by the data provider as either Event or Occurrence records, with the exception of the fields below which have been transformed or added by the OBIS quality control pipeline.

{:.table .table-sm .table-striped}
| field | remarks |
| --- | --- |
| id | Globally unique identifier assigned by OBIS. |
| dataset_id | Internal dataset identifier assigned by OBIS. |
| decimalLongitude | Parsed and validated by OBIS. |
| decimalLatitude | Parsed and validated by OBIS. |
| date_start | Unix timestamp based on eventDate (start). |
| date_mid | Unix timestamp based on eventDate (middle). |
| date_end | Unix timestamp based on eventDate (end). |
| date_year | Year based on eventDate. |
| scientificName | Valid scientific name based on the scientificNameID or derived by matching the provided scientificName with WoRMS |
| originalScientificName | The scientificName as provided. |
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
| AphiaID | AphiaID for the valid name based on the scientificNameID or derived by matching the provided scientificName with WoRMS. |
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


