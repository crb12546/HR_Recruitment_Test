"""
Alembic迁移配置修复脚本
用于修复数据库迁移配置问题
"""
import os
import sys
from pathlib import Path
from alembic.config import Config
from alembic import command

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fix_alembic_config():
    """修复Alembic配置并创建初始迁移"""
    print("开始修复Alembic配置...")
    
    # 确保versions目录存在
    versions_dir = Path("alembic/versions")
    if not versions_dir.exists():
        print(f"创建versions目录: {versions_dir}")
        versions_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取alembic配置
    alembic_cfg = Config("alembic.ini")
    
    # 确保数据库URL配置正确
    from app.core.config import settings
    print(f"数据库URL: {settings.DATABASE_URL}")
    
    # 创建初始迁移
    try:
        print("创建初始迁移...")
        command.revision(alembic_cfg, message="初始化数据库模型", autogenerate=True)
        print("初始迁移创建成功")
    except Exception as e:
        print(f"创建初始迁移失败: {e}")
        return False
    
    print("Alembic配置修复完成")
    return True

if __name__ == "__main__":
    fix_alembic_config()
