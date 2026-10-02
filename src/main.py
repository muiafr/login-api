from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.database import engine, setup_db
from src.database.models.user import UserModel
from src.api.users import router as user_router
from src.api.auth import router as login_router
from src.core.security import security

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await setup_db()
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)
security.handle_errors(app)
app.include_router(user_router)
app.include_router(login_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)