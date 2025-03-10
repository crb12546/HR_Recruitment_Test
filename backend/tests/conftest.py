"""
测试配置
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.db.base import Base
from app.main import app
from app.db.session import get_db

# 设置测试环境变量
os.environ["ENV"] = "test"
os.environ["MOCK_SERVICES"] = "True"

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
