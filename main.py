from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.database import engine, setup_db
from src.models.models import UserModel
from src.routes.route import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await setup_db()
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)