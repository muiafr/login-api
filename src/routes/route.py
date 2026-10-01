from fastapi import APIRouter, HTTPException

from src.hashpass import hash_password
from src.schemas.schema import CreateUser, ReadUsers, UpdateUser
from src.data import data


router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.get("/", response_model=list[ReadUsers])
def get_users() -> list[ReadUsers]:
    return data


@router.get("/{user_id}", response_model=ReadUsers)
def get_user(user_id: int) -> ReadUsers:
    for user in data:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@router.post("/create", response_model=ReadUsers, status_code=201)
def create_user(user: CreateUser) -> ReadUsers:
    for existing_user in data:
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=409,
                detail="Email already in use"
            )

    new_user = {
        "id": len(data) + 1,
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "age": user.age,
    }

    data.append(new_user)

    return new_user

@router.delete("/{user_id}", response_model=ReadUsers)
def delete_user(user_id: int) -> ReadUsers:
    for user in data:
        if user["id"] == user_id:
            data.remove(user)
            return data
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/{user_id}", response_model=ReadUsers)
def update_user(user_id: int, change_user: UpdateUser):
    for user in data:
        if user["id"] == user_id:
            updates = change_user.model_dump(
                exclude_unset=True,
                exclude_none=True
            )

            for key, value in updates.items():
                user[key] = value

            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@router.put("/{user_id}", response_model=ReadUsers)
def update_user(user_id: int, change_user: UpdateUser):
    for user in data:
        if user["id"] == user_id:
            updates = change_user.model_dump(exclude_unset=True)
            for key, value in updates.items():
                user[key] = value

            return user
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
