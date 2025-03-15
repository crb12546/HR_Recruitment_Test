"""
测试配置
"""
import os
import pytest
from typing import Dict, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db.base import Base
from app.main import app
from app.db.session import get_db
from app.core.security import create_access_token, get_password_hash
from app.models.user import User

# 设置测试环境变量
os.environ["ENV"] = "test"
os.environ["MOCK_SERVICES"] = "True"

# 测试用户数据
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword",
    "full_name": "测试用户"
}

test_superuser = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "adminpassword",
    "full_name": "管理员",
    "is_superuser": True
}

# 创建测试数据库引擎
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    提供测试数据库会话
    """
    # 创建测试数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # 清理测试数据库表
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """
    提供测试客户端
    """
    # 覆盖依赖
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # 创建测试客户端
    with TestClient(app) as c:
        yield c
    
    # 清理依赖覆盖
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def user_token_headers(client: TestClient, db) -> Dict[str, str]:
    """
    创建普通用户认证头
    """
    # 清理已有用户
    db.query(User).filter(User.username == test_user["username"]).delete()
    db.commit()
    
    # 创建用户
    user = User(
        username=test_user["username"],
        email=test_user["email"],
        hashed_password=get_password_hash(test_user["password"]),
        full_name=test_user["full_name"],
        is_active=True,
        is_superuser=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 创建访问令牌
    access_token = create_access_token(
        subject=str(user.id)
    )
    
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient, db) -> Dict[str, str]:
    """
    创建超级用户认证头
    """
    # 清理已有用户
    db.query(User).filter(User.username == test_superuser["username"]).delete()
    db.commit()
    
    # 创建超级用户
    user = User(
        username=test_superuser["username"],
        email=test_superuser["email"],
        hashed_password=get_password_hash(test_superuser["password"]),
        full_name=test_superuser["full_name"],
        is_active=True,
        is_superuser=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 创建访问令牌
    access_token = create_access_token(
        subject=str(user.id)
    )
    
    return {"Authorization": f"Bearer {access_token}"}
