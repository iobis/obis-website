# Run from fastapi/:
#   pip install -r ../requirements-dev.txt fastapi uvicorn jinja2 httpx starlette itsdangerous
#   ln -sfn ../_site static   # or let conftest write a minimal shell
#   PYTHONPATH=. pytest -q

import asyncio
import sys
import time
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport

# Ensure fastapi/ is on the path when pytest collects from tests/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import dataset as dataset_mod
import lib
import taxon as taxon_mod


pytestmark = pytest.mark.asyncio

DATASET_ID = "test-dataset-id"
DATASET_TITLE = "Test Dataset Title"


def _make_app():
    """Minimal app with SSR routes only (avoids auth/doi deps)."""
    app = FastAPI()
    app.include_router(dataset_mod.router, prefix="/dataset")
    app.include_router(taxon_mod.router, prefix="/taxon")
    return app


@pytest.fixture
async def client():
    transport = ASGITransport(app=_make_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def _dataset_fixture():
    return {
        "id": DATASET_ID,
        "title": DATASET_TITLE,
        "abstract": "An abstract",
        "nodes": [],
        "statistics": {"Occurrence": 100},
        "contacts": [],
    }


async def test_hang_regression_slow_dataset_does_not_block_taxon(client, monkeypatch):
    """A slow SSR fetch must not block concurrent requests on the event loop."""

    async def slow_metadata(dataset_id: str):
        await asyncio.sleep(2)
        return _dataset_fixture()

    async def fast_stats(filters):
        return {"taxa": 1, "species": 1}

    async def fast_qc(filters):
        return {"fields": {}, "flags": {}}

    async def fast_vars(filters):
        return []

    async def fast_taxon_api(url: str, **kwargs):
        return {
            "results": [
                {
                    "scientificName": "Acropora cervicornis",
                    "taxonRank": "Species",
                    "taxonomicStatus": "accepted",
                    "taxonID": 123,
                }
            ]
        }

    monkeypatch.setattr(dataset_mod, "get_metadata", slow_metadata)
    monkeypatch.setattr(dataset_mod, "get_statistics", fast_stats)
    monkeypatch.setattr(dataset_mod, "get_quality_statistics", fast_qc)
    monkeypatch.setattr(dataset_mod, "get_dataset_variables", fast_vars)
    monkeypatch.setattr(taxon_mod, "api_get", fast_taxon_api)

    async def timed_taxon():
        start = time.perf_counter()
        await asyncio.sleep(0.05)
        resp = await client.get("/taxon/123")
        elapsed = time.perf_counter() - start
        return resp, elapsed

    dataset_task = asyncio.create_task(client.get(f"/dataset/{DATASET_ID}"))
    taxon_task = asyncio.create_task(timed_taxon())

    dataset_resp, (taxon_resp, taxon_elapsed) = await asyncio.gather(
        dataset_task, taxon_task
    )

    assert dataset_resp.status_code == 200
    assert taxon_resp.status_code == 200
    assert "Acropora cervicornis" in taxon_resp.text
    assert taxon_elapsed < 0.5, f"taxon took {taxon_elapsed:.3f}s; event loop likely blocked"


async def test_timeout_fail_fast(client, monkeypatch):
    """Dataset SSR returns within a short timeout budget instead of hanging."""

    async def timing_out_api(url: str, **kwargs):
        await asyncio.sleep(0.25)
        raise httpx.TimeoutException("upstream timeout")

    monkeypatch.setattr(dataset_mod, "api_get", timing_out_api)

    start = time.perf_counter()
    resp = await client.get(f"/dataset/{DATASET_ID}")
    elapsed = time.perf_counter() - start

    assert resp.status_code == 200
    assert "Dataset not found" in resp.text or DATASET_ID in resp.text
    assert elapsed < 1.0, f"took {elapsed:.3f}s; expected fail-fast within ~1s"


async def test_graceful_degrade_when_secondary_calls_fail(client, monkeypatch):
    """Metadata still renders when stats / QC / variables fail."""

    async def ok_metadata(dataset_id: str):
        return _dataset_fixture()

    async def fail_stats(filters):
        return None

    async def fail_qc(filters):
        return None

    async def fail_vars(filters):
        return None

    monkeypatch.setattr(dataset_mod, "get_metadata", ok_metadata)
    monkeypatch.setattr(dataset_mod, "get_statistics", fail_stats)
    monkeypatch.setattr(dataset_mod, "get_quality_statistics", fail_qc)
    monkeypatch.setattr(dataset_mod, "get_dataset_variables", fail_vars)

    resp = await client.get(f"/dataset/{DATASET_ID}")
    assert resp.status_code == 200
    assert DATASET_TITLE in resp.text


async def test_happy_path_mocked(client, monkeypatch):
    """Full mocked dataset page returns metadata and statistics."""

    async def ok_metadata(dataset_id: str):
        return _dataset_fixture()

    async def ok_stats(filters):
        return {"taxa": 42, "species": 7, "yearrange": [2000, 2020]}

    async def ok_qc(filters):
        return {"fields": {}, "flags": {}}

    async def ok_vars(filters):
        return [{"key": "temperature|http://example.org/temp"}]

    monkeypatch.setattr(dataset_mod, "get_metadata", ok_metadata)
    monkeypatch.setattr(dataset_mod, "get_statistics", ok_stats)
    monkeypatch.setattr(dataset_mod, "get_quality_statistics", ok_qc)
    monkeypatch.setattr(dataset_mod, "get_dataset_variables", ok_vars)

    resp = await client.get(f"/dataset/{DATASET_ID}")
    assert resp.status_code == 200
    assert DATASET_TITLE in resp.text
    assert "42" in resp.text


async def test_api_get_raises_on_timeout(monkeypatch):
    """api_get surfaces TimeoutException from a failing transport."""

    monkeypatch.setattr(lib, "API_TIMEOUT", httpx.Timeout(0.2))

    def timeout_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    transport = httpx.MockTransport(timeout_handler)
    original_client = httpx.AsyncClient

    class PatchedAsyncClient(original_client):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            kwargs["timeout"] = lib.API_TIMEOUT
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", PatchedAsyncClient)

    start = time.perf_counter()
    with pytest.raises(httpx.TimeoutException):
        await lib.api_get("https://api.obis.org/statistics?datasetid=x")
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0
