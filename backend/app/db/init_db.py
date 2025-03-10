"""
数据库初始化模块
"""
import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

# 获取日志记录器
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    初始化数据库
    
    Args:
        db: 数据库会话
    """
    # 创建超级管理员用户
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="系统管理员",
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        logger.info("创建超级管理员用户成功")
