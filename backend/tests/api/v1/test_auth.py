"""
BDD-style tests for authentication endpoints.
"""
import pytest
from fastapi import status


def test_health_check(client):
    """
    Given: A running FastAPI application
    When: Making a GET request to the root endpoint
    Then: It should return a 200 status code and health check info
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert data["service"] == "GeoVoyager"


def test_get_current_user_no_token(client):
    """
    Given: A protected endpoint
    When: Making a request without an authentication token
    Then: It should return a 403 Forbidden response
    """
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authenticated"


def test_get_current_user_valid_token(client, valid_token):
    """
    Given: A protected endpoint
    When: Making a request with a valid authentication token
    Then: It should return the user profile
    """
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == "test-user-id"
    assert data["email"] == "test@example.com"
    assert data["role"] == "authenticated"


def test_get_current_user_invalid_token(client, invalid_token):
    """
    Given: A protected endpoint
    When: Making a request with an invalid token (missing required claims)
    Then: It should return a 401 Unauthorized response
    """
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid role in token"


def test_get_current_user_expired_token(client, expired_token):
    """
    Given: A protected endpoint
    When: Making a request with an expired token
    Then: It should return a 401 Unauthorized response
    """
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid authentication token" in response.json()["detail"]


def test_get_current_user_malformed_token(client):
    """
    Given: A protected endpoint
    When: Making a request with a malformed token
    Then: It should return a 401 Unauthorized response
    """
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer not-a-valid-token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid authentication token" in response.json()["detail"]
