"""
认证API端点
"""
from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_current_active_user, get_current_superuser, authenticate_user
from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    获取OAuth2兼容的令牌，用于用户登录
    """
    # 认证用户
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserSchema)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    注册新用户
    """
    # 检查用户名是否已存在
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    # 创建新用户（默认为普通用户，非超级用户）
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/me", response_model=UserSchema)
def read_current_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    更新当前用户信息
    """
    # 如果更新邮箱，检查邮箱是否已存在
    if user_in.email and user_in.email != current_user.email:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
    
    # 更新用户信息
    if user_in.password:
        current_user.hashed_password = get_password_hash(user_in.password)
    if user_in.full_name:
        current_user.full_name = user_in.full_name
    if user_in.email:
        current_user.email = user_in.email
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

# 以下接口仅超级用户可访问

@router.get("/users", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    获取所有用户列表（仅超级用户可访问）
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/users", response_model=UserSchema)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    创建新用户（仅超级用户可访问）
    """
    # 检查用户名是否已存在
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )
    
    # 创建新用户
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    获取指定用户信息（仅超级用户可访问）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    更新指定用户信息（仅超级用户可访问）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 如果更新邮箱，检查邮箱是否已存在
    if user_in.email and user_in.email != user.email:
        user_with_email = db.query(User).filter(User.email == user_in.email).first()
        if user_with_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
    
    # 更新用户信息
    if user_in.password:
        user.hashed_password = get_password_hash(user_in.password)
    if user_in.full_name:
        user.full_name = user_in.full_name
    if user_in.email:
        user.email = user_in.email
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    if user_in.is_superuser is not None:
        user.is_superuser = user_in.is_superuser
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    删除指定用户（仅超级用户可访问）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不允许删除自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除当前登录用户"
        )
    
    db.delete(user)
    db.commit()
    
    return user
