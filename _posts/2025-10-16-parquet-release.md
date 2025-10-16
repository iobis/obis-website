---
layout: post
title: New OBIS Parquet data release to improve global access and in-cloud analysis capacity
lang: en
author: OBIS
excerpt: This release contributes to providing a more equitable access to OBIS data and marine biodiversity information around the world.
tags: 
- actionable data
- Parquet
- full OBIS occurrence dataset
- DuckDB
- tutorial
purpose: news
feed: true
image: /images/thumbnails/parquet-thumb.png
---

<img alt="" src="/images/nenad-novakovic-mHX5e1gFQVo-unsplash.jpg" style="width: 100%;">
<i>Image: Nenad Novaković / Unsplash</i>  
<br><br>

OBIS has released new data products in **Parquet format**, including the [**speciesgrids**](https://github.com/iobis/speciesgrids), and the full OBIS occurrence dataset, which is now widely accessible through the [**AWS Open Data Program**](https://aws.amazon.com/opendata/). This release marks a significant step forward in how OBIS data can be accessed and analyzed.  
The speciesgrids are global maps that summarize species distributions, integrating marine data from OBIS and GBIF—two of the world’s major global biodiversity platforms—across a high-resolution global spatial grid. These maps make it easier to visualize and analyze large-scale patterns in species distributions.

The full OBIS occurrence dataset provides the most comprehensive view of marine biodiversity available through OBIS and now includes sequence records as well as the full set of variables from the Extended Measurement or Fact (eMoF) extension, such as sampling effort, environmental variables, and biological traits.

With this release, the OBIS occurrence dataset has been restructured to better meet users’ evolving needs. It is now published as a collection of [**GeoParquet**](https://geoparquet.org/) files, designed for efficient storage and cloud-based analysis. Combined with the technical infrastructure provided by the AWS Open Data Program, this new format enables users to perform large-scale spatial analyses directly in the cloud without the need to download massive datasets locally.

This shift is a significant step toward making OBIS data truly actionable for a broader range of users, especially those with limited or unstable internet connectivity. This release contributes to providing a more equitable access to OBIS data and marine biodiversity information around the world.

To support users in adopting these new formats, OBIS has published a three-part tutorial series on how to use DuckDB (a fast, in-process analytical database) with the Parquet datasets:

* [**Part 1: Introduction**](https://resources.obis.org/tutorials/duckdb-part1/) **/** Users learn how to connect to the OBIS Parquet datasets and run their first SQL queries using DuckDB—without downloading gigabytes of data.

* [**Part 2: Spatial Extension**](https://resources.obis.org/tutorials/duckdb-part2/) **/** Users discover how to enable and use DuckDB’s spatial extension to perform spatial queries directly on GeoParquet files, including filtering by geographic areas and intersecting polygons.

* [**Part 3: duckplyr Package**](https://resources.obis.org/tutorials/duckdb-part3/) **/** Users explore how to use the duckplyr R package to work with OBIS data using tidyverse syntax while benefiting from DuckDB’s high-performance backend.

While you're here, did you know that OBIS offers a wide range of **guides, tools, and training materials** to help you work with marine biodiversity data? In the [OBIS Resources Hub](https://resources.obis.org/), you can explore manuals, data publishing guides, video tutorials, and much more. These resources are designed to support both newcomers to OBIS and experienced data users.  

