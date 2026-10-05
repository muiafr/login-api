import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Override environment BEFORE importing the application; never use a real database.
_test_directory = tempfile.TemporaryDirectory(prefix="fastapistudy-tests-")
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///" + str(Path(_test_directory.name) / "test.db")
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-at-least-32-characters"

from src.main import app
from src.database.database import engine, Base


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        async def reset():
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.drop_all)
                await connection.run_sync(Base.metadata.create_all)
        test_client.portal.call(reset)
        yield test_client
