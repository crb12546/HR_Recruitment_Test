#!/bin/bash
# Alembic安装和配置脚本

echo "开始安装和配置Alembic..."

# 安装Alembic依赖
pip install -r requirements-alembic.txt

# 运行Alembic修复脚本
python alembic_fix.py

# 测试迁移功能
python test_migration.py

echo "Alembic安装和配置完成"
