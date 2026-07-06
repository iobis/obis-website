---
layout: post
title: "Standardized and FAIR: unleashing nearly 75 years of fish larvae and egg records"
lang: en
author: OBIS
tags: 
- CalCOFI
- OBIS USA
- BioEco EOVs
purpose: news
feed: true
image: /images/bb9527600n_2.jpg
imageAlt: "Scientists and ship crew recover CalBOBL (Bongo) net. Photo: NOAA Fisheries / James Wilkinson"
imageCaption: "Scientists and ship crew recover CalBOBL (Bongo) net.<br>Photo: NOAA Fisheries / James Wilkinson"
---
Turning decades of historical marine life records into standardized and FAIR data is a massive, but crucial challenge. Long-term data series on marine biodiversity are unique scientific assets that can help us understand how the ocean is changing. Making the *CalCOFI Fish Larvae & Egg Tows* dataset available through OBIS was made possible with a joint effort between the California Cooperative Oceanic Fisheries Investigations (CalCOFI), the Global Ocean Observing System (GOOS), and OBIS. The result is a Darwin Core-formatted dataset spanning 1951 to 2023, covering an area located mainly across the California Current, and containing 463,655 occurrence records, 610,816 measurements and facts, and observations of 539 species, accessible [here](https://obis.org/dataset/0e223f55-c826-4513-ae9a-b04cbf2e189c).
<br><br>

### The challenge of making long-term marine biodiversity data accessible

Long-term ecological datasets on the scale of the *CalCOFI Fish Larvae & Egg Tows* are scientifically invaluable because they provide the historical baselines needed to understand how marine ecosystems respond to environmental change. But such datasets remain rare. Although fisheries institutions worldwide hold some of the richest long-term marine life data ever collected, much of this information can be difficult to discover and access due to limited publishing capacity, lack of standardization, institutional dependence, or reluctance to share material that could be commercially sensitive. Before its integration into OBIS, the CalCOFI fish larvae and egg data was openly accessible, but needed to be further standardized to be findable, interoperable, and reusable by all. 

“We discussed with the GOOS team on using CalCOFI’s marine biodiversity datasets as a blueprint for integrating long-term observing data within the Essential Ocean Variables framework,” explains **Erin Satterthwaite**, CalCOFI Coordinator, Scripps Institution of Oceanography, University of California San Diego. “We chose that specific larval fish dataset because it is one of the longest-running in the program.” With its decades of richly detailed records, the *CalCOFI Fish Larvae & Egg Tows* dataset was a natural fit for supporting the Fish Abundance and Distribution of the BioEco Essential Ocean Variables (BioEco EOVs). 

<br><br>
<img alt="A researcher sorting a sample collected from the Continuous Underway Fish Egg Sampler (CUFES). CUFES samples are collected during transits between CalCOFI stations to see which fish species are spawning throughout the CalCOFI survey pattern. Photo: NOAA Fisheries / Angela Klemmedson" src="/images/bb0585544v_2.jpg" style="width: 100%;">
<p style="text-align: center;"><i>A researcher sorting a sample collected from the Continuous Underway Fish Egg Sampler (CUFES). CUFES samples are collected during transits between CalCOFI stations to see which fish species are spawning throughout the CalCOFI survey pattern.<br>Photo: NOAA Fisheries / Angela Klemmedson</i></p>  
<br><br>

The first phase involved a collaboration with the Ocean Data and Information System (ODIS) to make the CalCOFI datasets findable online. “After that, we wanted to step up and have our data directly integrated into OBIS, to make it fully and globally FAIR,” says Erin Satterthwaite. Standardising, quality-checking, and transforming a long-term historical dataset containing more than 400,000 occurrences into FAIR and trusted data is not a small task, especially when the goal is to create a reproducible publication workflow. “One of the huge challenges to solve remains to standardize formats, naming conventions, and structure across data spanning from the pre-digital to digital era, explains Erin Satterthwaite.    

“That standardization process began with sorting the data and organizing it, with much of this groundwork done by **Ed Weber**, data manager at NOAA,” explains **Ben Best**, marine data scientist at Ocean Metrics LLC (formerly EcoQuants LLC). “From that point on, we could focus on restructuring the data to streamline the standardization process.” Originally, the dataset had a hierarchical sampling structure nested across several levels: cruise, site (spatial coordinates), tow (time), net, and, finally, individual species observations. To make the data more usable, the team restructured it into two main event levels in Darwin Core: Cruise-level Events, to capture the overall sampling context; and Net Sample Events, representing the individual sampling actions at specific locations and times. The team then used the ExtendedMeasurementOrFact (eMoF) extension of Darwin Core to attach additional measurements and contextual information, and built a standardized vocabulary to describe the observed fish egg and larva stages. At that stage, the dataset was ready to be published into OBIS. 

<br><br>
<img alt="Overview of the data structure reorganization." src="/images/calcofi_schema.png" style="width: 100%;">
<p style="text-align: center;"><i>Overview of the data structure reorganization.</i></p>  
<br><br>

Beyond the dataset itself, the publication process of *CalCOFI Fish Larvae & Egg Tows* offers a reproducible path for turning biodiversity data held institutionally into globally accessible information. “From the start, we wanted this publication process to OBIS to be a template that could be applied to other use cases,” says Erin Satterthwaite. “We wanted to provide a clear pathway for how long-term datasets can contribute to EOVs and the Global Ocean Observing System. It was amazing to see what can happen when you get the right people working together: I am really grateful for the GOOS, OBIS, ODIS teams, and all the ones who helped us navigate that process.” The teams involved were tightly focused on a common objective: ensuring that these long-term observations could eventually be published for global use. “We really wanted to support the CalCOFI team to unleash the full potential of their data,” says **Elizabeth Lawrence,** OBIS Training Officer. “We brought into this project our know-how and experience in structuring Core tables and organizing nested Events.” The workflow, fully available through [CalCOFI.io](http://calcofi.io), is designed to be transparent, transposable, and reproducible, offering a ready-to-use path for other institutions looking to publish long-term biodiversity observations through OBIS. 
<br><br>

### More data to come

CalCOFI holds numerous long-term datasets on marine life from microbes to megafauna, such as seabirds, marine mammals, plankton, and eDNA data, which document biodiversity patterns and change in the [California Current marine ecosystem](https://www.fisheries.noaa.gov/west-coast/ecosystems/california-current-regional-ecosystem). Many of these datasets could progressively be integrated into OBIS through a similar pipeline. There is also potential to link CalCOFI’s physical and biogeochemical data streams with its biological observations, creating an integrated long-term dataset that connects multiple components of the California Current ecosystem. “Getting CalCOFI datasets standardized and more broadly shared is a bellwether for how science is changing, explains **Steve Formel**, OBIS Data Officer. “AI tools and global models are only as good as the data they rely on. This is exactly what platforms like OBIS and standards like Darwin Core were built for."

“No single institution can build the integrated global picture we need,” explains **Ana Lara-Lopez**, Lead Science Officer for the GOOS Biology and Ecosystems Expert Panel. “But combining observations, long-term records, and a shared commitment to open, standardized FAIR data allows us to move closer to a system that is greater than the sum of its parts. This is exactly the vision the EOV framework was built for.” The successful integration of the *CalCOFI Fish Larvae & Egg Tows* dataset into OBIS illustrates the value of the global marine biodiversity data chain in two important ways. First, it highlights the role of global data platforms in integrating and making large local datasets accessible to all. Second, it shows how sustained collaboration can transform locally-stored observations into standardized global information that supports research, modeling, global biodiversity frameworks, national assessment and reports, marine management, and ocean conservation. This achievement by CalCOFI, GOOS, and OBIS demonstrates how collaboration enables complex, but essential, marine life data to become available to all. ◼️

