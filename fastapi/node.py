from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
import urllib
import json
import os
from lib import get_quality_statistics, get_statistics, process_contacts

router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

# temporary local source for node metrics, will be replaced by an API call
METRICS_DIR = os.path.join(os.path.dirname(__file__), "..", "_DATA_TEMP")


def get_metrics(node_id: str):
    path = os.path.join(METRICS_DIR, f"{node_id}_metrics.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return None


@router.get("/{node_id}/metrics", response_class=JSONResponse)
async def node_metrics(node_id: str):
    metrics = get_metrics(node_id)
    if metrics is None:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics


@router.get("/{node_id}", response_class=HTMLResponse)
async def node_page(request: Request, node_id: str):

    api_url = f"https://api.obis.org/node/{node_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_json = response.json()
        node = response_json["results"][0]
        node["clean_contacts"] = process_contacts(node.get("contacts") or [])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Node not found")

    statistics = get_statistics({
        "nodeid": node_id,
        "dropped": "include",
        "absence": "include"
    })

    quality_statistics = get_quality_statistics({
        "nodeid": node_id,
        "dropped": "include",
        "absence": "include"
    })

    block = templates.get_template("node.html").render(
        node=node,
        statistics=statistics,
        quality_statistics=quality_statistics
    )

    return shell_templates.TemplateResponse(
        request=request,
        name="portal/index.html",
        context={
            "title": node["name"],
            "content": block
        }
    )