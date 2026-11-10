from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
from datetime import datetime
from lib import get_metrics, get_statistics


router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")


def datetimeformat(value, format="%B %d, %Y at %H:%M"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value.strftime(format)


templates.filters["datetimeformat"] = datetimeformat


def get_area(area_id: int):
    api_url = f"https://api.obis.org/area/{area_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            return None
        return data["results"][0]
    except Exception as e:
        print(e)
        return None


@router.get("/{area_id}/metrics", response_class=JSONResponse)
async def area_metrics(area_id: int):
    metrics = get_metrics({"areaid": area_id})
    if metrics is None:
        raise HTTPException(status_code=404, detail="Metrics not found")
    return metrics


@router.get("/{area_id}/report", response_class=HTMLResponse)
async def area_report(area_id: int):

    area = get_area(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Area not found")

    statistics = get_statistics({
        "areaid": area_id,
        "dropped": "include",
        "absence": "include"
    })

    html = templates.get_template("area_report.html").render(
        area=area,
        statistics=statistics,
        generated_at=datetime.utcnow()
    )

    return HTMLResponse(html)


@router.get("/{area_id}", response_class=HTMLResponse)
async def area(request: Request, area_id: int):

    area = get_area(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Area not found")

    statistics = get_statistics({
        "areaid": area_id
    })

    area_block = templates.get_template("area.html").render(
        area=area,
        statistics=statistics
    )

    return shell_templates.TemplateResponse(
        request=request,
        name="portal/index.html",
        context={
            "title": area["name"],
            "content": area_block
        }
    )
