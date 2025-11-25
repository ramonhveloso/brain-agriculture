from fastapi import status
from fastapi.testclient import TestClient

from app.api.v1.auth.auth_service import AuthService


def test_signup_success(client: TestClient, mocker):
    mocker.patch(
        "app.api.v1.auth.auth_service.AuthService.create_user",
        return_value={"id": 1, "email": "test@example.com", "name": "Test User", "username": "testuser"},
    )

    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass123",
        "name": "Test User",
    }

    response = client.post("/api/v1/auth/signup", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["email"] == "test@example.com"


def test_login_success(client: TestClient, mocker):
    mocker.patch(
        "app.api.v1.auth.auth_service.AuthService.authenticate_user",
        return_value={"id": 1, "email": "test@example.com"},
    )

    mocker.patch(
        "app.api.v1.auth.auth_service.AuthService.create_access_token",
        return_value={"access_token": "abc123", "token_type": "bearer"},
    )

    payload = {
        "username": "test@example.com",
        "password": "StrongPass123",
    }

    response = client.post("/api/v1/auth/login", data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == "abc123"


def test_signup_validation_error(client: TestClient):
    payload = {
        "username": "x",
        "email": "invalid-email",
        "password": "123",
        "name": "Test User",
    }

    response = client.post("/api/v1/auth/signup", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
