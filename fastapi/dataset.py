from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from lib import get_statistics, get_quality_statistics, render_jsonld, get_dataset_variables, process_contacts


router = APIRouter()
templates = Environment(loader=FileSystemLoader("templates"))
shell_templates = Jinja2Templates(directory="static")

def datetimeformat(value, format="%B %d, %Y at %H:%M"):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value.strftime(format)

templates.filters["datetimeformat"] = datetimeformat


def extract_doi(citation_id):
    if not citation_id:
        return None
    match = re.search(r'10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+', citation_id)
    return match.group(0) if match else None


EML_TAG_RE = re.compile(r'\{.*\}')


def eml_local_tag(element):
    return EML_TAG_RE.sub('', element.tag)


def get_eml(dataset_url):
    # Most OBIS datasets are hosted on an IPT instance, whose resource
    # pages and EML documents follow this URL convention. Datasets hosted
    # elsewhere (e.g. hosted-datasets.gbif.org archives) won't match, and
    # we fall back to None - the publisher/funding sections just don't show.
    if not dataset_url or "resource?r=" not in dataset_url:
        return None
    eml_url = dataset_url.replace("resource?r=", "eml.do?r=")
    try:
        response = requests.get(eml_url)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except Exception as e:
        print(e)
        return None


def get_gbif_dataset_key(eml_root):
    # GBIF's own registry key for the dataset is conventionally the first
    # alternateIdentifier in the EML (ahead of the DOI and IPT resource URL).
    if eml_root is None:
        return None
    for element in eml_root.iter():
        if eml_local_tag(element) == "alternateIdentifier":
            value = (element.text or "").strip()
            if re.fullmatch(r'[0-9a-fA-F-]{36}', value):
                return value
    return None


def get_funding(eml_root):
    if eml_root is None:
        return None
    for element in eml_root.iter():
        if eml_local_tag(element) == "funding":
            text = "".join(element.itertext()).strip()
            if text:
                return text
    return None


def get_publishing_organization(gbif_dataset_key):
    # The "publishing organization" is a property of the IPT installation's
    # registration with GBIF, not part of the resource's own EML - it isn't
    # exposed by the OBIS API or the EML document, only via GBIF's registry.
    if not gbif_dataset_key:
        return None
    try:
        response = requests.get(f"https://api.gbif.org/v1/dataset/{gbif_dataset_key}", timeout=10) 
        response.raise_for_status()
        publishing_org_key = response.json().get("publishingOrganizationKey")
        if not publishing_org_key:
            return None

        org_response = requests.get(f"https://api.gbif.org/v1/organization/{publishing_org_key}", timeout=10)
        org_response.raise_for_status()
        org = org_response.json()
        homepage = org.get("homepage")
        return {
            "name": org.get("title"),
            "url": homepage[0] if homepage else f"https://www.gbif.org/publisher/{publishing_org_key}"
        }
    except Exception as e:
        print(e)
        return None


def get_metadata(dataset_id: str):
    api_url = f"https://api.obis.org/dataset/{dataset_id}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        response_json = response.json()
        dataset = response_json["results"][0]
        dataset["doi"] = extract_doi(dataset.get("citation_id"))
        if "contacts" in dataset:
            dataset["clean_contacts"] = process_contacts(dataset["contacts"])

        eml_root = get_eml(dataset.get("url"))
        dataset["funding"] = get_funding(eml_root)
        dataset["publishing_organization"] = get_publishing_organization(get_gbif_dataset_key(eml_root))
    except Exception as e:
        print(e)
        return None
    return dataset


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