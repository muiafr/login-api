from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class Register(BaseModel):
    username: str
    password: str
    email: str
