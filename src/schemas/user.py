from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, computed_field



class CreateUser(BaseModel):
    username: str = Field(min_length=1,max_length=50,description="User's username")
    age: int = Field(ge=0,le=100,description="User's age")
    email: EmailStr = Field(description="User's email")
    password: str = Field(min_length=8,description="User's password")


    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18

    @field_validator("password")
    @classmethod
    def password_validator(cls, password: str):
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")

        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")

        return password


class ReadUsers(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str = Field(max_length=50,description="User's username")
    age: int
    email: EmailStr


    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18


class UpdateUser(BaseModel):
    username: str | None = Field(default=None,min_length=1,max_length=50)
    age: int | None = Field(default=None,ge=0,le=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None,min_length=8)

    @field_validator("password")
    @classmethod
    def password_validator(cls, password: str | None):
        if password is None:
            return None
        return CreateUser.password_validator(password)
