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
        
        print("\n数据库迁移测试成功")
        return True
    except Exception as e:
        print(f"数据库迁移测试失败: {e}")
        return False

if __name__ == "__main__":
    test_migration()
