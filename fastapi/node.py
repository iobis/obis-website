from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
import urllib
from lib import get_quality_statistics, get_statistics

router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")


@router.get("/{node_id}", response_class=HTMLResponse)
async def node_page(request: Request, node_id: str):

    api_url = f"https://api.obis.org/node/{node_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_json = response.json()
        node = response_json["results"][0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Node not found")

    statistics = get_statistics({
        "nodeid": node_id
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