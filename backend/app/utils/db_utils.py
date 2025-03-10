"""
数据库工具模块
提供数据库操作相关的工具函数
"""
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# 获取日志记录器
logger = logging.getLogger(__name__)

def safe_commit(db: Session, error_msg: str = "数据库提交失败") -> bool:
    """
    安全提交数据库事务
    
    Args:
        db: 数据库会话
        error_msg: 错误消息
        
    Returns:
        bool: 提交是否成功
    """
    try:
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"{error_msg}: {str(e)}")
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"{error_msg}: {str(e)}")
        return False
