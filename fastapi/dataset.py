from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import asyncio
from datetime import datetime
from lib import (
    api_get,
    get_statistics,
    get_quality_statistics,
    render_jsonld,
    get_dataset_variables,
    process_contacts,
)


router = APIRouter()
templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

def datetimeformat(value, format="%B %d, %Y at %H:%M"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value.strftime(format)

templates.filters["datetimeformat"] = datetimeformat


async def get_metadata(dataset_id: str):
    api_url = f"https://api.obis.org/dataset/{dataset_id}"
    try:
        response_json = await api_get(api_url)
        dataset = response_json["results"][0]
        if "contacts" in dataset:
            dataset["clean_contacts"] = process_contacts(dataset["contacts"])
    except Exception as e:
        print(e)
        return None
    return dataset


async def get_blacklist(dataset_id: str):
    api_url = f"https://api.obis.org/dataset/blacklist/{dataset_id}"
    try:
        print(api_url)
        results = (await api_get(api_url))["results"]
        if len(results) > 0:
            return results[0]
        else:
            return None
    except Exception as e:
        print(e)
        return None


@router.get("/{dataset_id}", response_class=HTMLResponse)
async def dataset_page(request: Request, dataset_id: str):

    # dataset metadata

    dataset = await get_metadata(dataset_id)

    if dataset is None:

        blacklist = await get_blacklist(dataset_id)

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

    # statistics, quality statistics, variables (parallel)

    statistics, quality_statistics, variables = await asyncio.gather(
        get_statistics({
            "datasetid": dataset_id
        }),
        get_quality_statistics({
            "datasetid": dataset_id,
            "dropped": "include",
            "absence": "include"
        }),
        get_dataset_variables({
            "datasetid": dataset_id,
            "dropped": "include",
            "absence": "include",
            "event": "include"
        }),
    )

    # jsonld

    jsonld = render_jsonld(dataset, statistics=statistics, variables=variables)

    # render

    dataset_block = templates.get_template("dataset.html").render(
        dataset=dataset,
        statistics=statistics,
        quality_statistics=quality_statistics,
        jsonld=jsonld
    )

    return shell_templates.TemplateResponse(
        request=request,
        name="portal/index.html",
        context={
            "title": dataset["title"],
            "content": dataset_block
        }
    )
