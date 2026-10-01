import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
    host=os.environ["DATABASE_HOST"],
    port=int(os.environ["DATABASE_PORT"]),
    database=os.environ["DATABASE_NAME"],
)
