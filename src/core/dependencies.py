from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_session

Session_DEP = Annotated[AsyncSession, Depends(get_session)]
