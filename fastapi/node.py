from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import asyncio
from lib import api_get, get_quality_statistics, get_statistics, process_contacts

router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

# Temporary: hide OceanExpert "group leaders" from node contact lists.
# Keep them on the OBIS Secretariat node page.
SECRETARIAT_NODE_ID = "310922b4-9d0c-4de1-92d7-9b442d34765b"
HIDDEN_NODE_CONTACT_OE_IDS = {11770, 72350}  # Ward Appeltans, Laurent Chmiel


def filter_node_contacts(contacts, node_id: str):
    if node_id == SECRETARIAT_NODE_ID:
        return contacts

    filtered = []
    for contact in contacts:
        oe_id = contact.get("oceanexpert_id")
        try:
            oe_id = int(oe_id) if oe_id is not None else None
        except (TypeError, ValueError):
            oe_id = None
        if oe_id not in HIDDEN_NODE_CONTACT_OE_IDS:
            filtered.append(contact)
    return filtered


@router.get("/{node_id}", response_class=HTMLResponse)
async def node_page(request: Request, node_id: str):

    api_url = f"https://api.obis.org/node/{node_id}"
    try:
        response_json = await api_get(api_url)
        node = response_json["results"][0]
        node["contacts"] = filter_node_contacts(node.get("contacts") or [], node_id)
        node["clean_contacts"] = process_contacts(node["contacts"])
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
