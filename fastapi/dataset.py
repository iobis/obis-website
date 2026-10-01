from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
import json
import os
import re
import markdown
from datetime import datetime
from lib import get_statistics, get_quality_statistics, render_jsonld, get_dataset_variables, process_contacts

# temporary local source for dataset insights, will be replaced by an API call
INSIGHTS_DIR = os.path.join(os.path.dirname(__file__), "..", "_DATA_TEMP")

# same IUCN Red List palette as renderRedListBadge() in assets/script.js — keep in sync
REDLIST_COLORS = {
    "Extinct": ("#000000", "#fff"),
    "Extinct in the Wild": ("#880000", "#fff"),
    "Critically Endangered": ("#d1001c", "#fff"),
    "Endangered": ("#e67e22", "#fff"),
    "Vulnerable": ("#f7b731", "#222"),
    "Near Threatened": ("#3fa535", "#fff"),
    "Least Concern": ("#1e90a2", "#fff"),
    "Data Deficient": ("#aaaaaa", "#fff"),
    "Not Evaluated": ("#cccccc", "#222"),
}

# longest phrase first, so "Critically Endangered" matches before "Endangered" alone
_REDLIST_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(term) for term in sorted(REDLIST_COLORS, key=len, reverse=True)) + r")\b"
)


def highlight_redlist_terms(html: str):
    def replace(match):
        term = match.group(1)
        background, color = REDLIST_COLORS[term]
        return f'<span class="badge" style="background-color: {background}; color: {color}; font-weight: 600;">{term}</span>'
    return _REDLIST_PATTERN.sub(replace, html)


router = APIRouter()
templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

def datetimeformat(value, format="%B %d, %Y at %H:%M"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value.strftime(format)

templates.filters["datetimeformat"] = datetimeformat


def get_metadata(dataset_id: str):
    api_url = f"https://api.obis.org/dataset/{dataset_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_json = response.json()
        dataset = response_json["results"][0]
        if "contacts" in dataset:
            dataset["clean_contacts"] = process_contacts(dataset["contacts"])
    except Exception as e:
        print(e)
        return None
    return dataset


def render_inline_markdown(text: str):
    html = markdown.markdown(text)
    if html.startswith("<p>") and html.endswith("</p>"):
        html = html[len("<p>"):-len("</p>")]
    return html


# every highlight renders as a stat tile (big number + caption). One that
# opens with a count ("16 species ...") uses that as the number and the rest
# of the sentence as the caption. One that doesn't (e.g. "The most frequently
# recorded taxon is... with 6,883 records.") uses the first number found in
# the rendered, tag-stripped text instead (searching raw markdown would catch
# digits inside link URLs, e.g. a taxon ID or dataset UUID), and keeps the
# full sentence as the caption so the grammar around that number stays intact.
_LEADING_NUMBER_PATTERN = re.compile(r"^([\d,]+)\s+(.*)$")
_ANY_NUMBER_PATTERN = re.compile(r"[\d][\d,]*")
_TAG_PATTERN = re.compile(r"<[^>]+>")


def split_highlight(text: str):
    match = _LEADING_NUMBER_PATTERN.match(text)
    if match:
        return match.group(1), match.group(2)
    visible_text = _TAG_PATTERN.sub("", render_inline_markdown(text))
    any_number = _ANY_NUMBER_PATTERN.search(visible_text)
    return (any_number.group(0) if any_number else None), text


def get_insights(dataset_id: str):
    path = os.path.join(INSIGHTS_DIR, f"{dataset_id}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            insights = json.load(f)
        insights["description_html"] = highlight_redlist_terms(markdown.markdown(insights["description"]))
        for highlight in insights.get("highlights", []):
            number, caption_text = split_highlight(highlight["text"])
            highlight["number"] = number
            highlight["caption_html"] = highlight_redlist_terms(render_inline_markdown(caption_text))
    except Exception as e:
        print(e)
        return None
    return insights


def get_metrics(dataset_id: str):
    path = os.path.join(INSIGHTS_DIR, f"{dataset_id}_metrics.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return None


def get_blacklist(dataset_id: str):
    api_url = f"https://api.obis.org/dataset/blacklist/{dataset_id}"
    try:
        print(api_url)
        response = requests.get(api_url)
        response.raise_for_status()
        results = response.json()["results"]
        if len(results) > 0:
            return results[0]
        else:
            return None
    except Exception as e:
        print(e)
        return None


@router.get("/{dataset_id}/metrics", response_class=JSONResponse)
async def dataset_metrics(dataset_id: str):
    metrics = get_metrics(dataset_id)
    if metrics is None:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics


@router.get("/{dataset_id}/report", response_class=HTMLResponse)
async def dataset_report(dataset_id: str):

    dataset = get_metadata(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    statistics = get_statistics({
        "datasetid": dataset_id
    })

    quality_statistics = get_quality_statistics({
        "datasetid": dataset_id,
        "dropped": "include",
        "absence": "include"
    })

    insights = get_insights(dataset_id)

    html = templates.get_template("dataset_report.html").render(
        dataset=dataset,
        statistics=statistics,
        quality_statistics=quality_statistics,
        insights=insights,
        generated_at=datetime.utcnow()
    )

    return HTMLResponse(html)


@router.get("/{dataset_id}", response_class=HTMLResponse)
async def dataset_page(request: Request, dataset_id: str):

    # dataset metadata

    dataset = get_metadata(dataset_id)

    if dataset is None:

        blacklist = get_blacklist(dataset_id)

        dataset_block = templates.get_template("dataset_404.html").render(
            dataset_id=dataset_id,
            blacklist=blacklist
        )

        return shell_templates.TemplateResponse(
            request=request,
            name="portal/index.html",
            context={
                "title": "Dataset not found",
                "content": dataset_block
            }
        )

    # statistics

    statistics = get_statistics({
        "datasetid": dataset_id
    })

    # quality statistics

    quality_statistics = get_quality_statistics({
        "datasetid": dataset_id,
        "dropped": "include",
        "absence": "include"
    })

    # variables

    variables = get_dataset_variables({
        "datasetid": dataset_id,
        "dropped": "include",
        "absence": "include",
        "event": "include"
    })

    # jsonld

    jsonld = render_jsonld(dataset, statistics=statistics, variables=variables)

    # insights

    insights = get_insights(dataset_id)

    # render

    dataset_block = templates.get_template("dataset.html").render(
        dataset=dataset,
        statistics=statistics,
        quality_statistics=quality_statistics,
        jsonld=jsonld,
        insights=insights
    )

    return shell_templates.TemplateResponse(
        request=request,
        name="portal/index.html",
        context={
            "title": dataset["title"],
            "content": dataset_block
        }
    )