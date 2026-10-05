import secrets

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.core.dependencies import Session_DEP
from src.core.security import hash_password, security
from src.database.models.auth import LoginModel
from src.database.models.user import UserModel
from src.schemas.auth import Login, Register

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/")
async def login(log: Login, session: Session_DEP, response: Response):
    result = await session.execute(
        select(UserModel).where(UserModel.username == log.username)
    )
    user = result.scalars().first()

    if user is None or not secrets.compare_digest(
        user.password,
        hash_password(log.password),
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    login_record = LoginModel(
        user_id=user.id,
        username=user.username,
        email=user.email,
        password="",
    )
    session.add(login_record)
    await session.commit()

    token = security.create_access_token(uid=str(user.id))
    security.set_access_cookies(token, response)

    return {"message": "Login successful"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    reg: Register,
    session: Session_DEP,
    response: Response,
):
    new_user = UserModel(
        username=reg.username,
        email=reg.email,
        age=18,
        password=hash_password(reg.password),
    )

    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    token = security.create_access_token(uid=str(new_user.id))
    security.set_access_cookies(token, response)

    return {
        "message": "Registration successful",
        "user_id": new_user.id,
    }
