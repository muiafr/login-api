from pydantic import BaseModel, EmailStr, Field, field_validator


class Login(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8)


class Register(Login):
    email: EmailStr = Field(description="User email")

    @field_validator("password")
    @classmethod
    def password_validator(cls, password: str) -> str:
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        return password
