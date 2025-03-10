"""
用户相关的Pydantic模型
"""
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="全名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    is_superuser: Optional[bool] = Field(False, description="是否超级用户")

class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., description="密码")

class UserUpdate(BaseModel):
    """更新用户模型"""
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    full_name: Optional[str] = Field(None, description="全名")
    password: Optional[str] = Field(None, description="密码")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_superuser: Optional[bool] = Field(None, description="是否超级用户")

class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class User(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """令牌载荷模型"""
    sub: Optional[int] = None
