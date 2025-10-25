from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
import os
from lib import get_statistics


router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

@router.get("/{occurrence_id}", response_class=HTMLResponse)
async def occurrence(request: Request, occurrence_id: str):
    url = f"https://api.obis.org/occurrence/{occurrence_id}?mof=true&dna=true&dropped=include"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get("results"):
            raise HTTPException(status_code=404, detail=f"Occurrence {url} not found")
        occurrence = data["results"][0]

        occurrence_block = templates.get_template("occurrence.html").render(
            occurrence=occurrence
        )

        return shell_templates.TemplateResponse(
            request=request,
            name="portal/index.html",
            context={
                "title": occurrence["id"],
                "content": occurrence_block
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail=f"Occurrence {url} not found") 