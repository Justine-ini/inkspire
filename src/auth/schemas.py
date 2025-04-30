from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str 
    email: EmailStr
    password: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool 
    created_at: datetime
    updated_at: datetime
    password: str = Field(exclude=True)



class UserCreateModel(BaseModel):
    first_name: Optional[str] = Field(default="NA")
    last_name: Optional[str] = Field(default="NA")
    username: str = Field(min_length=3)
    email: str = Field(max_length=40)
    password: str = Field(min_length=5)


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class UserUpdateModel(UserCreateModel):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None