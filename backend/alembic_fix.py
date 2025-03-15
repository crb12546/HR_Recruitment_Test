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
    
    # 确保alembic目录存在
    alembic_dir = Path("alembic")
    if not alembic_dir.exists():
        print(f"创建alembic目录: {alembic_dir}")
        alembic_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    # 检查是否已有迁移版本
    try:
        print("检查当前迁移版本...")
        command.current(alembic_cfg)
        print("迁移版本检查成功")
    except Exception as e:
        print(f"迁移版本检查失败: {e}")
        
        # 初始化alembic环境
        try:
            print("初始化alembic环境...")
            # 如果alembic目录为空，则初始化
            if not os.path.exists("alembic/env.py"):
                command.init(alembic_cfg, "alembic")
                print("alembic环境初始化成功")
                
                # 修改env.py文件以支持自动生成迁移
                update_env_py()
        except Exception as e:
            print(f"初始化alembic环境失败: {e}")
            return False
    
    # 创建初始迁移
    try:
        print("创建初始迁移...")
        command.revision(alembic_cfg, message="初始化数据库模型", autogenerate=True)
        print("初始迁移创建成功")
    except Exception as e:
        print(f"创建初始迁移失败: {e}")
        return False
    
    # 应用迁移
    try:
        print("应用迁移...")
        command.upgrade(alembic_cfg, "head")
        print("迁移应用成功")
    except Exception as e:
        print(f"应用迁移失败: {e}")
        return False
    
    print("Alembic配置修复完成")
    return True

def update_env_py():
    """更新env.py文件以支持自动生成迁移"""
    env_py_path = "alembic/env.py"
    with open(env_py_path, "r") as f:
        content = f.read()
    
    # 添加导入项目配置和模型的代码
    import_code = """
# 导入项目配置和模型
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings
from app.db.base import Base
from app.models import *  # 导入所有模型以确保它们在创建表时被注册
"""
    
    # 添加设置数据库URL的代码
    db_url_code = """
# 设置数据库URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
"""
    
    # 修改target_metadata
    target_metadata_code = "target_metadata = Base.metadata"
    
    # 替换内容
    content = content.replace(
        "# add your model's MetaData object here",
        "# add your model's MetaData object here\n" + target_metadata_code
    )
    
    # 在导入部分后添加项目导入
    import_section_end = "from alembic import context"
    content = content.replace(
        import_section_end,
        import_section_end + import_code
    )
    
    # 在config对象后添加数据库URL设置
    config_section = "config = context.config"
    content = content.replace(
        config_section,
        config_section + db_url_code
    )
    
    # 写回文件
    with open(env_py_path, "w") as f:
        f.write(content)
    
    print(f"已更新 {env_py_path}")

if __name__ == "__main__":
    fix_alembic_config()
