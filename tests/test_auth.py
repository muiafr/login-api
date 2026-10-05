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


def test_register_and_login_work_for_a_new_user():
    register_response = client.post(
        "/login/register",
        json={
            "username": "dana",
            "email": "dana@example.com",
            "password": "StrongPass4",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/login/",
        json={"username": "dana", "password": "StrongPass4"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["message"] == "Login successful"
    assert login_response.cookies.get("access_token")
