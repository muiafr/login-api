from fastapi import APIRouter, Depends, HTTPException
from authx import TokenPayload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.core.dependencies import Session_DEP
from src.core.security import hash_password, security
from src.database.models.user import UserModel
from src.schemas.user import CreateUser, ReadUsers


router = APIRouter(
    tags=["users"],
    prefix="/users",
)


@router.get("/", response_model=list[ReadUsers], dependencies=[Depends(security.access_token_required)])
async def get_users(session: Session_DEP):
    result = await session.execute(select(UserModel))
    return result.scalars().all()


@router.get("/{user_id}", response_model=ReadUsers, dependencies=[Depends(security.access_token_required)])
async def get_user(user_id: int, session: Session_DEP):
    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/create", response_model=ReadUsers, status_code=201)
async def create_user(user: CreateUser, session: Session_DEP):
    new_user = UserModel(
        username=user.username,
        email=user.email,
        age=user.age,
        password=hash_password(user.password),
    )

    session.add(new_user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")

    await session.refresh(new_user)
    return new_user


@router.delete("/delete/{user_id}", response_model=ReadUsers)
async def delete_user(
    user_id: int,
    session: Session_DEP,
    token: TokenPayload = Depends(security.access_token_required),
):
    if token.sub != str(user_id):
        raise HTTPException(status_code=403, detail="You can only delete your own account")

    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return user


@router.put("/update/{user_id}", response_model=ReadUsers)
async def update_user(
    user_id: int,
    user: CreateUser,
    session: Session_DEP,
    token: TokenPayload = Depends(security.access_token_required),
):
    if token.sub != str(user_id):
        raise HTTPException(status_code=403, detail="You can only update your own account")

    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.age = user.age
    db_user.password = hash_password(user.password)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")

    await session.refresh(db_user)
    return db_user
