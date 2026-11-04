from pathlib import Path

import pytest

FASTAPI_DIR = Path(__file__).resolve().parent.parent
STATIC_PORTAL = FASTAPI_DIR / "static" / "portal" / "index.html"

MINIMAL_SHELL = """<!DOCTYPE html>
<html>
<head><title>{{ title }} | OBIS</title></head>
<body>{{ content | safe }}</body>
</html>
"""


@pytest.fixture(scope="session", autouse=True)
def ensure_static_shell():
    """Write a minimal portal shell so SSR tests do not need a Jekyll build."""
    STATIC_PORTAL.parent.mkdir(parents=True, exist_ok=True)
    if not STATIC_PORTAL.is_file():
        STATIC_PORTAL.write_text(MINIMAL_SHELL)
    yield
