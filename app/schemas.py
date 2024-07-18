from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    country_name: str
    password: str


class User(BaseModel):
    id: int
    country_name: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    country_name: Optional[str] = None
