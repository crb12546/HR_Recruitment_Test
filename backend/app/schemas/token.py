"""
令牌相关模式
"""
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """令牌模式"""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """令牌载荷模式"""
    sub: Optional[str] = None
    exp: Optional[int] = None
