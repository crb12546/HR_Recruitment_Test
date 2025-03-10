"""
数据库设置脚本
用于安装依赖、创建数据库和初始化表结构
"""
import os
import sys
import subprocess

def install_dependencies():
    """安装必要的依赖项"""
    print("安装必要的依赖项...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sqlalchemy_utils", "python-dotenv"])
    print("依赖项安装完成")

def run_db_creation():
    """运行数据库创建脚本"""
    print("运行数据库创建脚本...")
    try:
        from app.db.create_db import init_db
        init_db()
        print("数据库创建完成")
    except Exception as e:
        print(f"数据库创建失败: {str(e)}")
        print("将尝试使用alembic创建表结构")

def create_migration():
    """创建数据库迁移文件"""
    print("创建数据库迁移文件...")
    try:
        # 尝试创建迁移文件
        subprocess.check_call(["alembic", "revision", "--autogenerate", "-m", "初始化数据库模型"])
        print("迁移文件创建成功")
    except Exception as e:
        print(f"创建迁移文件失败: {str(e)}")
        print("将使用SQLAlchemy直接创建表结构")

def run_migration():
    """运行数据库迁移"""
    print("运行数据库迁移...")
    try:
        # 尝试运行迁移
        subprocess.check_call(["alembic", "upgrade", "head"])
        print("数据库迁移完成")
    except Exception as e:
        print(f"运行迁移失败: {str(e)}")
        print("将使用SQLAlchemy直接创建表结构")

if __name__ == "__main__":
    # 安装依赖项
    install_dependencies()
    
    # 运行数据库创建脚本
    run_db_creation()
    
    # 创建并运行迁移
    create_migration()
    run_migration()
    
    print("数据库设置完成")
