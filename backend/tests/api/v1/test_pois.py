import pytest
from fastapi import status
from httpx import AsyncClient
from tests.conftest import TestingSessionLocal
from app.models.poi import POI
import asyncio

class TestPOIEndpoints:
    """BDD-style tests for POI endpoints."""

    @pytest.mark.asyncio
    async def test_create_poi(self, async_client: AsyncClient, auth_headers: dict):
        """
        Given: An authenticated admin user
        When: Creating a new POI with valid data
        Then: Should return 201 and the created POI
        """
        poi_data = {
            "title": "Eiffel Tower",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "description": "Famous landmark in Paris",
            "audio_url": "https://storage.example.com/audio/eiffel.mp3"
        }

        response = await async_client.post(
            "/api/v1/pois",
            json=poi_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == poi_data["title"]
        assert data["latitude"] == poi_data["latitude"]
        assert data["longitude"] == poi_data["longitude"]

    @pytest.mark.asyncio
    async def test_create_poi_invalid_coordinates(self, async_client: AsyncClient, auth_headers: dict):
        """
        Given: An authenticated admin user
        When: Creating a POI with invalid coordinates
        Then: Should return 422 validation error
        """
        poi_data = {
            "title": "Invalid POI",
            "latitude": 91.0,  # Invalid latitude
            "longitude": 2.2945,
            "description": "Test POI"
        }

        response = await async_client.post(
            "/api/v1/pois",
            json=poi_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_update_poi(self, async_client: AsyncClient, auth_headers: dict):
        """
        Given: An existing POI and authenticated admin user
        When: Updating the POI with new data
        Then: Should return 200 and updated POI
        """
        # First create a POI
        poi_data = {
            "title": "Original Title",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "description": "Original description"
        }
        create_response = await async_client.post(
            "/api/v1/pois",
            json=poi_data,
            headers=auth_headers
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        poi_id = create_response.json()["id"]

        # Update the POI
        update_data = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        response = await async_client.put(
            f"/api/v1/pois/{poi_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        updated_data = response.json()
        assert updated_data["title"] == update_data["title"]
        assert updated_data["description"] == update_data["description"]

    @pytest.mark.asyncio
    async def test_delete_poi(self, async_client: AsyncClient, auth_headers: dict):
        """
        Given: An existing POI and authenticated admin user
        When: Deleting the POI
        Then: Should return 204 and POI should be deleted
        """
        # First create a POI
        poi_data = {
            "title": "To Be Deleted",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "description": "This POI will be deleted"
        }
        create_response = await async_client.post(
            "/api/v1/pois",
            json=poi_data,
            headers=auth_headers
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        poi_id = create_response.json()["id"]

        # Delete the POI
        response = await async_client.delete(
            f"/api/v1/pois/{poi_id}",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify POI is deleted
        get_response = await async_client.get(
            f"/api/v1/pois/{poi_id}",
            headers=auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
