import pytest


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_health(client):

    response = await client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"


# ---------------------------------------------------------
# Ready
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_ready(client):

    response = await client.get("/ready")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ready"


# ---------------------------------------------------------
# Live
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_live(client):

    response = await client.get("/live")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "alive"


# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_metrics(client):

    response = await client.get("/metrics")

    assert response.status_code == 200


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_root(client):

    response = await client.get("/")

    assert response.status_code == 200


# ---------------------------------------------------------
# Docs Endpoint
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_docs(client):

    response = await client.get("/docs")

    assert response.status_code == 200


# ---------------------------------------------------------
# OpenAPI
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_openapi(client):

    response = await client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    assert "paths" in schema