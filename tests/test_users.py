import asyncio
import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_fastapistudy.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

from src.database.database import drop_db, setup_db
from src.main import app


@pytest.fixture(autouse=True)
def reset_db():
    asyncio.run(drop_db())
    asyncio.run(setup_db())
    yield
    asyncio.run(drop_db())
    asyncio.run(setup_db())


client = TestClient(app)


def test_register_user_creates_account_and_sets_cookie():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "StrongPass1",
    }

    response = client.post("/login/register", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Registration successful"
    assert response.cookies.get("access_token")


def test_login_accepts_registered_user():
    client.post(
        "/login/register",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "StrongPass2",
        },
    )

    response = client.post(
        "/login/",
        json={"username": "bob", "password": "StrongPass2"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert response.cookies.get("access_token")


def test_user_list_requires_authentication():
    client.post(
        "/login/register",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "StrongPass3",
        },
    )

    response = client.get("/users/")

    assert response.status_code == 200
    assert any(user["username"] == "charlie" for user in response.json())
