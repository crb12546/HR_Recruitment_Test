"""
数据库迁移测试脚本
用于测试Alembic迁移配置是否正确
"""
import os
import sys
from pathlib import Path
from alembic.config import Config
from alembic import command

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_migration():
    """测试数据库迁移功能"""
    print("开始测试数据库迁移...")
    
    # 获取alembic配置
    alembic_cfg = Config("alembic.ini")
    
    try:
        # 检查当前迁移版本
        print("检查当前迁移版本...")
        command.current(alembic_cfg)
        
        # 应用迁移
        print("\n应用迁移...")
        command.upgrade(alembic_cfg, "head")
        
        # 检查迁移历史
        print("\n检查迁移历史...")
        command.history(alembic_cfg)
        
        # 测试回滚
        print("\n测试回滚...")
        command.downgrade(alembic_cfg, "-1")
        
        # 重新应用迁移
        print("\n重新应用迁移...")
        command.upgrade(alembic_cfg, "head")
        
        # 验证数据库表结构
        print("\n验证数据库表结构...")
        verify_database_tables()
        
        print("\n数据库迁移测试成功")
        return True
    except Exception as e:
        print(f"数据库迁移测试失败: {e}")
        return False

def verify_database_tables():
    """验证数据库表结构是否与模型定义一致"""
    from sqlalchemy import inspect
    from app.db.session import engine
    from app.models import Base
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    # 检查所有模型对应的表是否存在
    model_tables = [model.__tablename__ for model in Base.__subclasses__()]
    missing_tables = [table for table in model_tables if table not in tables]
    
    if missing_tables:
        print(f"警告：以下表未创建: {missing_tables}")
        return False
    
    print(f"所有表已创建: {tables}")
    return True

if __name__ == "__main__":
    test_migration()
