"""
Auth schemas - LoginRequest, TokenPair, UserInfo.
"""
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)


class TokenPair(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    expires_in: int = Field(alias="expiresIn")

    model_config = {"populate_by_name": True}


class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    avatar: str | None = None
    roles: list[str]
    level: str
