from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from lib import api_get

router = APIRouter()

templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

@router.get("/{taxon_id}", response_class=HTMLResponse)
async def taxon(request: Request, taxon_id: int):
    try:
        data = await api_get(f"https://api.obis.org/taxon/{taxon_id}")
        
        if not data.get("results"):
            raise HTTPException(status_code=404, detail="Taxon not found")
            
        taxon = data["results"][0]
        
        taxon_block = templates.get_template("taxon.html").render(
            taxon=taxon
        )

        return shell_templates.TemplateResponse(
            request=request,
            name="portal/index.html",
            context={
                "title": taxon["scientificName"],
                "content": taxon_block
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Taxon not found")
