---
layout: post
title: OBIS-GOOS Collaboration on EOVs - Establishing an operational global framework for seagrass monitoring and reporting
lang: en
author: OBIS
tags: 
- OBIS-GOOS collaboration
- Essential Ocean Variables
- Seagrass
purpose: news
feed: true
image: /images/seagrass_01.jpg
---
<img alt="Small fish school of Sarpa salpa above a seagrass meadow in Greece. Photo: Dimitris Poursanidis" src="/images/seagrass_01.jpg" style="width: 100%;">
<i>Small fish school of Sarpa salpa above a seagrass meadow in Greece. Photo: Dimitris Poursanidis</i>  
<br><br>
Seagrasses are crucial to coastal ecosystems. Meadows of these flowering, submerged plants provide habitat and serve as nurseries for numerous marine species, including endangered ones; capture and store carbon in their biomass and in the sediments below; provide substantial ecological benefits supporting the livelihood of coastal communities; filter pollutants and contribute to protecting coastlines from erosion. Despite these fundamental ecological functions, available scientific information on seagrasses remains fragmented and hard to compare, mainly due to a lack of standardization in data collection and reporting. In a [new paper](https://academic.oup.com/bioscience/advance-article-abstract/doi/10.1093/biosci/biaf199/8407550) published in BioScience, "*Measuring and Reporting on Seagrass as an Essential Ocean Variable for Science and Management*", the authors proposed the first comprehensive, community-endorsed specification framework for measuring and reporting [seagrass as a Biology and Ecosystems Essential Ocean Variable](https://goosocean.org/document/17513) (BioEco EOV) under the Global Ocean Observing System (GOOS).

Seagrass data is collected and reported using different methods and formats, varying from project to project and region to region. This lack of global coordination results in a patchwork of hard-to-compare observations, preventing most of the datasets from being submitted to global biodiversity information platforms such as OBIS. It also deprives scientists and decision-makers of the capacity to generate insights for research and evidence-based action. "Most of the studies done on seagrasses were on small scales, for very specific local purposes," explains **Emmett Duffy**, Chief Scientist emeritus at the Smithsonian MarineGEO program and the lead author of the paper. "Until about 20 years ago, seagrasses didn't have the high profile of coral reefs or mangroves." 

The 2015 Paris Agreement amplified the policy relevance of seagrass data. "Parties could now integrate seagrass habitats in their Nationally Determined Contributions, which created an incentive to map them," Duffy continues. "Later, when the Kunming-Montreal Global Biodiversity Framework was adopted, seagrass meadows fell within the scope of one of the headline indicators for Target 2 'Extent of natural ecosystems', again highlighting their recognized role in global biodiversity monitoring." For coastal nations, monitoring seagrass extent is becoming a key component of national biodiversity reporting under the Kunming-Montreal Global Biodiversity Framework.
<br><br>
<img alt="Close up of a Posidonia oceanica rhizome. Photo: Dimitris Poursanidis" src="/images/seagrass_02.jpg" style="width: 100%;">
<i>Close up of a Posidonia oceanica rhizome. Photo: Dimitris Poursanidis</i>  
<br><br>
### **Seagrasses as an Essential Ocean Variable**

The establishment of “Seagrass cover and composition” as a BioEco EOV, along with the resulting requirement to integrate these variables into OBIS, encouraged a need for a globally accepted observation method of seagrasses. [BioEco EOVs](https://goosocean.org/what-we-do/framework/essential-ocean-variables/) are a core set of measurements needed to observe the state of the ocean and monitor its changes through key variables, from microbes to mangroves. BioEco EOVs are defined and coordinated by GOOS and operationalized by OBIS, as their designated data repository. GOOS provides a common framework of EOVs that allows scientists worldwide to compare results and measure changes in the Ocean state. OBIS provides the data backbone that sustains and makes them standardized and FAIR (Findable, Accessible, Interoperable, and Reusable), allowing for cross-scale connection from local datasets to global indicators. To achieve full operationalization of the EOVs, collaboration with communities is essential, as **Ana Lara Lopez**, Lead Science Officer at the GOOS BioEco Panel, explains: "We continuously work with observing communities to ensure that the proposed approaches for marine biodiversity monitoring meet local and global needs. The seagrass community has fully embraced this approach.” 

### **A standardisation process that takes into account local contexts**

In their paper, Duffy et al., in consulation with the broader community, propose three core subvariables for the seagrass EOV: percentage cover (the seafloor proportion covered by seagrass at the quadrat scale), species composition (which species are present; what is their relative abundance), and areal extent (the total area of seagrass meadows at a given location at the landscape scale). The authors also propose a pragmatic, tiered approach for seagrass observations: high quality, medium quality, and minimum acceptable data. "Most biodiversity in the world occurs in developing countries, and, often, the places that need data the most have little scientific or institutional capacity," Duffy observes. "One of our guiding principles was to make the observation process as simple as possible, down to 'is there seagrass in that location or not?' If we manage to collect large amounts of this basic yet robust data, it's a win for seagrasses and science." Such an approach would also leverage local knowledge: Duffy points to citizen science apps like the Seagrass Spotter, developed by Project Seagrass in the UK, as an example of how even minimum-level observations, such as species presence recorded by someone snorkeling, can contribute to the global picture.

The proposed guidelines for monitoring and reporting seagrasses have three major benefits:   
They allow for remaining flexible and taking into account local ecological contexts and the biological variations of the 72 currently recognized seagrass species; they link fine-scale in-field measurements with remote-sensing observations; they can be made fully compatible with Darwin Core standards. This last point is crucial to ensure total interoperability of the data at local and global scales, from fine-scale measurements in the field to satellite-based observations. One question remains open: what to do with seagrass observation legacy data? "In principle, as long as you know what species was found in this place on this date, it can be published to OBIS," Duffy says. Although he is realistic about the effort involved: "This is going to need case-specific approaches, and will require funding, and certainly a lot of time and dedication from the community."
<br><br>
<img alt="Seafloor view of a seaieass meadow in Greece. Photo: Dimitris Poursanidis" src="/images/seagrass_03.jpg" style="width: 100%;">
<i>Seafloor view of a seaieass meadow in Greece. Photo: Dimitris Poursanidis</i>  
<br><br>
### **Data integration through Darwin Core**

Translation of seagrass observations into an OBIS-ready format is achieved through three interlinked tables formatted in Darwin Core, as explained in the paper: an Event table, an Occurrence table and a table for Extended Measurements or Facts. 

The **Event table** provides the sampling context: each row is a sampling event and includes the decimal latitude/longitude, date, and a unique eventID field. The Event table also carries metadata such as the sampling protocol used, the depth of the observation, the type of habitat, the dataset name, and the type of data-sharing license.  
→ *You can read more about the OBIS generic dataset structure in [this part](https://manual.obis.org/formatting.html#dataset-structure) of the OBIS Manual.*   
*→ You can read more about the Event table in [this part](https://manual.obis.org/format_event.html) of the OBIS Manual.* 

The **Occurrence table** informs on the species observed during an event, and each row represents a species occurrence with its scientific name validated against the World Register of Marine Species (WoRMS), using a Life Science Identifier (LSID). The table records whether the species was present or absent, how the observation was made, and who recorded it.   
*→ You can read more about the Occurrence table in [this part](https://manual.obis.org/format_occurrence.html) of the OBIS Manual.* 

Finally, the **Extended Measurement or Fact (EMoF) table** harbours the quantitative seagrass EOV data. This table integrates biological variables (percentage cover, shoot density, shoot length, and canopy height) with physical and biochemical variables (water temperature, salinity, for example). Each measurement in the EMoF table links to both an eventID and an occurrenceID to provide the most comprehensive context possible for each observation. All the measurement types and units match the controlled vocabularies established by the Natural Environment Research Council ([NERC](https://vocab.nerc.ac.uk/)). eventID and occurrenceID fields act as the shared links that interconnect the three tables.   
*→ You can read more about the EMoF table in [this part](https://manual.obis.org/format_emof.html) of the OBIS Manual*  
*→ Read more about identifiers in [this part](https://manual.obis.org/identifiers.html) of the OBIS Manual*

The tables are submitted for publication to OBIS as a package via an Integrated Publishing Toolkit (IPT), ensuring in the process that all metadata is included, describing the datasets as a whole, using the Ecological Metadata Language (EML) standard.   
*→ You can read more about IPTs in [this part](https://manual.obis.org/ipt.html) of the OBIS Manual.*   
 

### **Data ownership and quality control**

To ensure data ownership, traceability, and contributors' recognition, OBIS can assign a DOI to the dataset. Because the datasets are published via IPT, they undergo OBIS's systematic quality assessment and quality control process, ensuring that potential mistakes, abnormalities, or inconsistencies in the data are flagged before publication and corrected. “A key goal of the EOVs is to make ocean data public and shareable with as little friction as possible,” says Duffy. “Collaborating with the OBIS Secretariat ensured that seagrass data would flow smoothly and accurately into OBIS, making it available to everyone.”

The impact of publishing standardized seagrass data could be massive. From an OBIS perspective, this would bring on the platform a stream of FAIR, traceable, quality-controlled seagrass data from field observations that could be mobilized for ground-truthing remote sensing products and improving models. This new data would also contribute to strengthening evidence-based national assessments and would better support evidence-based decision-making, especially at the regional level. For communities of seagrass researchers and local monitoring initiatives, publishing standardized data to OBIS allows for increased visibility and recognition, as well as a guarantee of data ownership even through downstream transformations. For Duffy, there is no doubt that these guidelines can boost available global information on seagrass and increase collaboration between communities involved: "Let's work together to make our seagrass data accessible and useful to all," he concludes. 

*Do you want to learn more about publishing data to OBIS? Our [publishing tutorial series](https://youtube.com/playlist?list=PLlgUwSvpCFS4TS7ZN0fhByj_3EBZ5lXbF&si=92QcNlwg6pfoteiM) on YouTube walks you through the process step by step\!*  
