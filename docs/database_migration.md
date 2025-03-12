# 数据库迁移指南

## 概述

本文档提供HR招聘系统的数据库迁移指南，包括迁移配置、创建迁移脚本、应用迁移和回滚操作等内容。系统使用Alembic作为数据库迁移工具，支持自动生成迁移脚本和版本控制。

## 环境要求

- Python 3.9+
- Alembic 1.12.0+
- SQLAlchemy 2.0.23+

## 安装和配置

### 自动安装和配置

项目提供了自动安装和配置脚本，可以一键完成Alembic的安装和配置：

```bash
cd backend
bash setup_alembic.sh
```

### 手动安装和配置

1. 安装依赖

```bash
pip install -r requirements-alembic.txt
```

2. 修复Alembic配置

```bash
python alembic_fix.py
```

3. 测试迁移功能

```bash
python test_migration.py
```

## 迁移操作指南

### 创建新的迁移

当数据模型发生变化时，需要创建新的迁移脚本：

```bash
cd backend
alembic revision --autogenerate -m "迁移说明"
```

### 应用迁移

将数据库更新到最新版本：

```bash
alembic upgrade head
```

### 回滚迁移

回滚到上一个版本：

```bash
alembic downgrade -1
```

回滚到特定版本：

```bash
alembic downgrade <版本号>
```

### 查看迁移历史

```bash
alembic history
```

### 查看当前版本

```bash
alembic current
```

## 常见问题排查

### 1. 迁移脚本生成失败

**问题**：运行`alembic revision --autogenerate`时出错。

**解决方案**：
- 确保所有模型已正确导入
- 检查env.py文件中的target_metadata设置
- 确保数据库URL配置正确

### 2. 迁移应用失败

**问题**：运行`alembic upgrade head`时出错。

**解决方案**：
- 检查数据库连接是否正常
- 查看迁移脚本是否有语法错误
- 确保数据库用户有足够权限

### 3. Python 3.12兼容性问题

**问题**：在Python 3.12环境下出现兼容性错误。

**解决方案**：
- 使用requirements-alembic.txt中指定的版本
- 如果仍有问题，考虑降级到Python 3.9

## 文档历史

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| 1.0 | 2025-03-12 | 初始版本 | Devin |
