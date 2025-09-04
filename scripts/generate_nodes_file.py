import json
from typing import Any, Dict, List
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


BASE_URL = "https://oceanexpert.org/api/v1/group/{group_id}.json"
ROOT_GROUP_ID = 386
OBIS_NODES_URL = "https://api.obis.org/node"


def create_session() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        # allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": "obisnew-nodes-fetcher/1.0 (+https://obis.org)",
        "Accept": "application/json",
    })
    return session


def fetch_group(session: requests.Session, group_id: int) -> Dict[str, Any]:
    url = BASE_URL.format(group_id=group_id)
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_members(group_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    members = group_json.get("members") or {}
    return list(members.values())


def build_subgroups_with_members(session: requests.Session, root_group_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    subgroups = root_group_json.get("subGroups") or []
    results: List[Dict[str, Any]] = []
    for sg in subgroups:
        sg_id = sg.get("idGroup")
        if sg_id is None:
            continue
        sg_details = fetch_group(session, int(sg_id))
        results.append({
            "idGroup": sg_details.get("idGroup", sg_id),
            "groupname": sg_details.get("groupname", sg.get("groupname")),
            "members": extract_members(sg_details),
        })
    return results


def fetch_obis_nodes(session: requests.Session) -> Dict[str, Dict[str, Any]]:
    """Return a mapping from node name to node object from OBIS API."""
    response = session.get(OBIS_NODES_URL, timeout=30)
    response.raise_for_status()
    data = response.json() or {}
    results = data.get("results") or []
    mapping: Dict[str, Dict[str, Any]] = {}
    for node in results:
        name = node.get("name")
        if name:
            mapping[str(name)] = node
    return mapping


def enrich_with_obis_metadata(groups: List[Dict[str, Any]], name_to_node: Dict[str, Dict[str, Any]]) -> None:
    for g in groups:
        name = g.get("groupname")
        node = name_to_node.get(name or "")
        if not node:
            continue
        urls = node.get("url") or []
        g["lat"] = node.get("lat")
        g["lon"] = node.get("lon")
        g["description"] = node.get("description")
        g["url"] = urls[0] if isinstance(urls, list) and urls else urls


def prioritize_subgroup(groups: List[Dict[str, Any]], target_id: int = 432) -> None:
    idx = next((i for i, g in enumerate(groups) if str(g.get("idGroup")) == str(target_id)), None)
    if idx is not None and idx != 0:
        groups.insert(0, groups.pop(idx))


def main() -> None:
    session = create_session()
    root = fetch_group(session, ROOT_GROUP_ID)
    obis_nodes = fetch_obis_nodes(session)
    data = build_subgroups_with_members(session, root)
    prioritize_subgroup(data, 432)
    enrich_with_obis_metadata(data, obis_nodes)

    output = json.dumps(data, ensure_ascii=False, indent=2)
    with open(os.path.join("_data", "nodes.json"), "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()


