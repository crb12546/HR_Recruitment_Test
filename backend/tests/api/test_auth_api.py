"""
认证API测试
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

# 测试数据
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

def create_test_user(db: Session) -> User:
    """创建测试用户"""
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
    return user

def create_test_superuser(db: Session) -> User:
    """创建测试超级用户"""
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
    return user

class TestAuth:
    """认证API测试类"""
    
    def test_login(self, client: TestClient, db: Session):
        """测试登录功能"""
        # 创建测试用户
        create_test_user(db)
        
        # 登录请求
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data=login_data
        )
        
        # 验证响应
        assert response.status_code == 200
        token = response.json()
        assert "access_token" in token
        assert token["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client: TestClient, db: Session):
        """测试错误密码登录"""
        # 创建测试用户
        create_test_user(db)
        
        # 登录请求（错误密码）
        login_data = {
            "username": test_user["username"],
            "password": "wrongpassword"
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/login",
            data=login_data
        )
        
        # 验证响应
        assert response.status_code == 401
        assert "detail" in response.json()
    
    def test_register(self, client: TestClient, db: Session):
        """测试注册功能"""
        # 注册请求
        new_user = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword",
            "full_name": "新用户"
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=new_user
        )
        
        # 验证响应
        assert response.status_code == 200
        created_user = response.json()
        assert created_user["username"] == new_user["username"]
        assert created_user["email"] == new_user["email"]
        assert created_user["full_name"] == new_user["full_name"]
        assert "id" in created_user
        
        # 验证数据库
        db_user = db.query(User).filter(User.username == new_user["username"]).first()
        assert db_user is not None
        assert db_user.email == new_user["email"]
    
    def test_register_existing_username(self, client: TestClient, db: Session):
        """测试注册已存在用户名"""
        # 创建测试用户
        create_test_user(db)
        
        # 注册请求（已存在用户名）
        new_user = {
            "username": test_user["username"],  # 已存在的用户名
            "email": "another@example.com",
            "password": "anotherpassword",
            "full_name": "另一个用户"
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/register",
            json=new_user
        )
        
        # 验证响应
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_get_current_user(self, client: TestClient, db: Session, user_token_headers):
        """测试获取当前用户信息"""
        response = client.get(
            f"{settings.API_V1_STR}/auth/me",
            headers=user_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == test_user["username"]
        assert user_data["email"] == test_user["email"]
        assert user_data["full_name"] == test_user["full_name"]
    
    def test_update_current_user(self, client: TestClient, db: Session, user_token_headers):
        """测试更新当前用户信息"""
        # 更新请求
        update_data = {
            "email": "updated@example.com",
            "full_name": "更新后的用户"
        }
        response = client.put(
            f"{settings.API_V1_STR}/auth/me",
            json=update_data,
            headers=user_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["email"] == update_data["email"]
        assert updated_user["full_name"] == update_data["full_name"]
        
        # 验证数据库
        db_user = db.query(User).filter(User.username == test_user["username"]).first()
        assert db_user.email == update_data["email"]
        assert db_user.full_name == update_data["full_name"]
    
    def test_get_users_normal_user(self, client: TestClient, db: Session, user_token_headers):
        """测试普通用户获取用户列表（应该失败）"""
        response = client.get(
            f"{settings.API_V1_STR}/auth/users",
            headers=user_token_headers
        )
        
        # 验证响应（应该是403禁止访问）
        assert response.status_code == 403
    
    def test_get_users_superuser(self, client: TestClient, db: Session, superuser_token_headers):
        """测试超级用户获取用户列表"""
        response = client.get(
            f"{settings.API_V1_STR}/auth/users",
            headers=superuser_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 1  # 至少有超级用户
    
    def test_create_user_superuser(self, client: TestClient, db: Session, superuser_token_headers):
        """测试超级用户创建用户"""
        # 创建用户请求
        new_user = {
            "username": "createduser",
            "email": "created@example.com",
            "password": "createdpassword",
            "full_name": "被创建的用户",
            "is_active": True,
            "is_superuser": False
        }
        response = client.post(
            f"{settings.API_V1_STR}/auth/users",
            json=new_user,
            headers=superuser_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        created_user = response.json()
        assert created_user["username"] == new_user["username"]
        assert created_user["email"] == new_user["email"]
        
        # 验证数据库
        db_user = db.query(User).filter(User.username == new_user["username"]).first()
        assert db_user is not None
    
    def test_delete_user_superuser(self, client: TestClient, db: Session, superuser_token_headers):
        """测试超级用户删除用户"""
        # 创建要删除的用户
        user_to_delete = User(
            username="userdelete",
            email="delete@example.com",
            hashed_password=get_password_hash("deletepassword"),
            full_name="要删除的用户",
            is_active=True,
            is_superuser=False
        )
        db.add(user_to_delete)
        db.commit()
        db.refresh(user_to_delete)
        
        # 删除用户请求
        response = client.delete(
            f"{settings.API_V1_STR}/auth/users/{user_to_delete.id}",
            headers=superuser_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        
        # 验证数据库
        db_user = db.query(User).filter(User.id == user_to_delete.id).first()
        assert db_user is None
