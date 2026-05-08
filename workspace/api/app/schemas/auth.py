"""
Auth schemas - LoginRequest, TokenPair, UserInfo.
"""
from pydantic import BaseModel, Field, SecretStr


class LoginRequest(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=100, description="用户名或邮箱")
    email: str | None = Field(None, max_length=200, description="邮箱地址")
    password: SecretStr = Field(..., min_length=1)
    
    def get_identifier(self) -> str:
        """Get login identifier (username or email)"""
        return self.username or self.email or ""


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
