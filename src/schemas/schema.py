from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateUser(BaseModel):
    username: str = Field(min_length=1, description="User's username")
    email: EmailStr = Field(description="User's email")
    password: str = Field(min_length=8, description="User's password")

    @field_validator("password")
    @classmethod
    def password_validator(cls, password: str):
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")

        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")

        return password

class ReadUsers(BaseModel):
    id: int = Field(description="User ID")
    username: str = Field(description="User's username")
    email: EmailStr = Field(description="User's email")

class UpdateUser(BaseModel):
    username: str = Field(description="User's username")
    email: EmailStr = Field(description="User's email")
    password: str = Field(description="User's password")
