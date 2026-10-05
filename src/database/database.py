import datetime
from typing import Annotated

from sqlalchemy import String, func, inspect, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from src.core.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


IntPK = Annotated[int, mapped_column(primary_key=True)]
CreatedAtType = Annotated[datetime.datetime, mapped_column(server_default=func.current_timestamp())]
UpdatedAtType = Annotated[datetime.datetime, mapped_column(server_default=func.current_timestamp(), onupdate=func.current_timestamp())]
NameType = Annotated[str, mapped_column(String(50))]
PasswordType = Annotated[str, mapped_column(String(256))]
EmailType = Annotated[str, mapped_column(String(254))]


class Base(DeclarativeBase):
    pass


async def setup_db():
    from src.database.models.user import UserModel
    from src.database.models.auth import LoginModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        columns = await conn.run_sync(
            lambda connection: inspect(connection).get_columns("login")
        )
        if "email" not in {column["name"] for column in columns}:
            await conn.execute(text(
                "ALTER TABLE login ADD COLUMN email VARCHAR(256) NOT NULL DEFAULT ''"
            ))

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)