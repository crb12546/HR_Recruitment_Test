"""
数据库创建脚本
用于初始化数据库和表结构
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.config import settings
from app.db.base import Base

def init_db():
    """初始化数据库"""
    engine = create_engine(settings.DATABASE_URL)
    
    # 对于SQLite，直接创建表
    if settings.DATABASE_URL.startswith('sqlite'):
        # 确保目录存在
        db_path = settings.DATABASE_URL.replace('sqlite:///', '')
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print(f"SQLite数据库 {db_path} 和所有表已创建")
    else:
        # 对于其他数据库，如MySQL
        # 如果数据库不存在，则创建
        if not database_exists(engine.url):
            create_database(engine.url)
            print(f"数据库 {engine.url.database} 已创建")
        else:
            print(f"数据库 {engine.url.database} 已存在")
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("所有表已创建")

if __name__ == "__main__":
    init_db()
