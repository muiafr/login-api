from typing import Annotated

from fastapi import Depends, HTTPException
from authx import TokenPayload
from src.core.security import security
from src.database.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_session

Session_DEP = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    session: Session_DEP,
    token: TokenPayload = Depends(security.access_token_required),
) -> UserModel:
    if not token.sub.isdecimal():
        raise HTTPException(status_code=401, detail="Invalid user token")
    user = await session.get(UserModel, int(token.sub))
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user
