import pytest
from httpx import AsyncClient
from fastapi import status

class TestHealthEndpoint:
    """BDD-style tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """
        Given: A running FastAPI application
        When: Making a GET request to /health
        Then: Should return 200 and healthy status
        """
        response = await async_client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_health_check_with_db(self, async_client: AsyncClient):
        """
        Given: A running FastAPI application with database connection
        When: Making a GET request to /health/db
        Then: Should return 200 and database connection status
        """
        response = await async_client.get("/api/v1/health/db")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
