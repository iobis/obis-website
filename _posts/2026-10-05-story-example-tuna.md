---
layout: story
title: "Tracking tunas through OBIS data"
subtitle: "An example of a dynamic story"
lang: en
author: OBIS
tags:
- Story
purpose: news
feed: true
intro: "Charts and maps in this article are drawn live from the OBIS API. This page doubles as a template for building dynamic news stories."
---

Writing a story works like any other news article: plain Markdown. Wherever you want something dynamic, add a component tag such as `<obis-map>`. No script is needed.

## A chart

The chart below shows how many yellowfin tuna (*Thunnus albacares*) records have been published to OBIS each year.

<obis-recs-by-year taxonid="127027"></obis-recs-by-year>
<p class="story-caption">Records per year, fetched live from the OBIS API.</p>

Charts are built with [Observable Plot](https://observablehq.com/plot/). Components accept OBIS filters such as `taxonid`, `scientificname`, `areaid` or `datasetid`.

## A map

The map shows where those records were collected, using the same occurrence grid as the rest of the website.

<obis-map taxonid="127027" center="0,10" zoom="1"></obis-map>

## A scrolling story

Maps can also be driven by the text. Scroll down: the camera moves, and the occurrence layer changes, as each step comes into view.

<obis-scrolly taxonid="127027" center="-35,5" zoom="2">
  <obis-step center="-35,5" zoom="2" markdown="1">
**Yellowfin tuna** are found across tropical and subtropical oceans, with dense reporting in the Atlantic.
  </obis-step>
  <obis-step center="75,5" zoom="3" markdown="1">
In the **Indian Ocean**, a major fishery supports many coastal communities.
  </obis-step>
  <obis-step taxonid="127028" center="-140,5" zoom="2" markdown="1">
Switching species: **bigeye tuna** (*Thunnus obesus*) across the Pacific.
  </obis-step>
</obis-scrolly>

## Any other data

`<obis-chart>` plots any JSON or CSV file or API endpoint, here the yearly records of bigeye tuna:

<obis-chart class="story-wide" src="https://api.obis.org/statistics/years?taxonid=127028" mark="bar" x="year" y="records" xlabel="Year" ylabel="Records"></obis-chart>

For anything the built-in components can't do, add `story_script: /assets/story/your-script.js` to the front matter and use `chart()` / `storyMap()` from `/assets/story/story.js`.
