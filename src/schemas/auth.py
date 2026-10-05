from pydantic import BaseModel, Field
from src.schemas.user import CreateUser


class Login(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=8)




class Register(CreateUser):
    pass
