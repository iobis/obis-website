---
layout: post
title: "OBIS publishes its first eDNA dataset based on Event Core"
lang: en
author: OBIS
tags: 
- eDNA
- Event Core
- BioEco EOVs
purpose: news
feed: true
image: /images/Common_moon_jelly_Janine H.jpeg
---
<img alt="A common moon jelly (Aurelia aurita), one of the species from the "Invertebrate eDNA Gotland Summer 2021 " dataset." src="/images/Common_moon_jelly_Janine H.jpeg" style="width: 100%;">
<p style="text-align: center;"><i>A common moon jelly (Aurelia aurita), one of the species from the "Invertebrate eDNA Gotland Summer 2021 " dataset. Photo: Janine H. / iNaturalist</i></p>  
<br><br>

DNA-derived marine biodiversity datasets can contain a huge amount of information that can become hard to access if not properly structured. OBIS reached an important technical milestone by publishing its [very first environmental DNA (eDNA)-based dataset](https://obis.org/dataset/8c638ec0-7567-4397-be52-f305eadf4b24) using the Event Core structure, paving the way for how complex biodiversity observations can be integrated into global platforms operating under the Darwin Core format.
<br><br>

### A small dataset built to test a new structure

Collected during a biodiversity survey around the Swedish island of Gotland, the dataset "Invertebrate eDNA Gotland Summer 2021" (Nordlund L M, Lüskow F, Lawrence E (2026). Invertebrate eDNA Gotland Summer 2021\. Version 2.1. OBIS Secretariat. Samplingevent dataset. [https://doi.org/10.25607/bgjoog](https://doi.org/10.25607/bgjoog)) demonstrates how eDNA, occurrence records, sampling events, and environmental measurements can all be neatly integrated using Event core in Darwin Core format, without causing information inflation. “The dataset is modest in size, containing 116 occurrence records,” explains **Florian Lüskow**, postdoctoral research fellow at Uppsala University, one of the authors, who was conducting this work within the EU-funded project BioEcoOcean. “That relatively small size for a DNA-derived occurrence dataset made it an ideal candidate to experiment with the Event core structure. The dataset was originally collected as part of a researcher-led biodiversity survey, showcasing that advanced biodiversity data standards are becoming accessible to individual researchers and smaller monitoring initiatives.” 

<br><br>

> In addition to linking environmental measurements to Event Core, the dataset has also been aligned with Essential Ocean Variables (EOVs) through its metadata.

### From Occurrence core to Event core

Traditionally, biodiversity datasets published through OBIS have been structured around species occurrences, using the Occurrence core approach. In these datasets, environmental measurements, such as temperature or salinity, need to be duplicated for every occurrence record, potentially leading to data inflation if the dataset contains a large number of species occurrences. Shifting from Occurrence core to Event core allows for environmental measurements to be linked directly to the sampling event itself, removing duplication and making datasets easier to manage and interpret. “If we really want to make environmental monitoring data Findable, Accessible, Interoperable, and Reusable,” says Florian Lüskow, “we need to have data publication pipelines that work for large, national programmes and smaller, project-based initiatives.”

<br><br>
<img alt="Comparison between the Occurrence core and the Event core approach to managing extendedMeasurementOrFact data." src="/images/edna_event_core_illu_01.jpg" style="width: 100%;">
<p style="text-align: center;"><i>Comparison between the Occurrence core and the Event core approach to managing extendedMeasurementOrFact data.</i></p>  
<br><br>

### A reusable pipeline for eDNA data

The publication of the "Invertebrate eDNA Gotland Summer 2021" dataset also reflects ongoing work across the biodiversity informatics community to innovate data management approaches through more flexible structures within, for example, Darwin Core Data Packages. Recent developments in the OBIS data pipeline now allow complex relationships between sampling events, DNA observations, occurrences, and measurement data to be processed and integrated more efficiently. “In addition to linking environmental measurements to Event Core, the dataset has also been aligned with Essential Ocean Variables (EOVs) through its metadata,” explains **Elizabeth Lawrence**, OBIS Training Officer, who provided technical support in the integration of the dataset into OBIS. “This helps improve discoverability and interoperability with broader ocean observing efforts. This EOV alignment was done retroactively: EOV specification sheets were still being updated at the time the sampling was done. We demonstrated that datasets originally not collected specifically to match EOVs requirements could still be retrofitted and contribute to the framework.” 

<br><br>
<img alt="Flowchart showing the data pipeline from field collection through DNA-derived occurrences, sampling events, and environmental measurements, to Event Core formatting, OBIS integration, EOV alignment, and publication to OBIS." src="/images/edna_event_core_illu_02.jpg" style="width: 100%;">
<p style="text-align: center;"><i>Sample-to-screen flowchart showing the entire data integration process of the "Invertebrate eDNA Gotland Summer 2021" dataset into OBIS, including EOV alignment</i></p>  
<br><br>

### Local survey, global standard

"It is exciting to see a dataset collected around Gotland, Sweden, contribute to advances in global biodiversity data standards,” says **Lina Mtwana Nordlund,** Uppsala University & GOOS Biology and Ecosystem EOV panel member and project coordinator of BioEcoOcean. “For me, this publication illustrates an important principle: local observations can have global value when they are shared in interoperable formats. If we want marine biodiversity to be visible in global assessments, Essential Ocean Variables, global ocean indicators, and Digital Twins of the Ocean, we need to invest in collecting data, but also in publishing and connecting that data to the wider digital ocean ecosystem.”

Environmental DNA-derived data, like other innovative formats, capture incredibly complex information that requires creative standardization and formatting approaches to prevent data inflation while preserving FAIRness and actionability. ◼️
