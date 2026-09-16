from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import asyncio
from lib import api_get, get_quality_statistics, get_statistics, process_contacts

router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")


@router.get("/{node_id}", response_class=HTMLResponse)
async def node_page(request: Request, node_id: str):

    api_url = f"https://api.obis.org/node/{node_id}"
    try:
        response_json = await api_get(api_url)
        node = response_json["results"][0]
        node["clean_contacts"] = process_contacts(node.get("contacts") or [])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Node not found")

    statistics, quality_statistics = await asyncio.gather(
        get_statistics({
            "nodeid": node_id,
            "dropped": "include",
            "absence": "include"
        }),
        get_quality_statistics({
            "nodeid": node_id,
            "dropped": "include",
            "absence": "include"
        }),
    )

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
