# HR招聘系统本地部署文档

## 概述

本文档提供HR招聘系统的本地部署指南，包括环境要求、安装步骤、配置说明和常见问题排查。通过本文档，可以在本地环境中部署系统并通过ngrok映射到公网IP，供外部用户访问。

## 环境要求

- Python 3.9
- MySQL 8.0
- ngrok (已安装)
- 网络连接 (用于ngrok映射)

## 部署步骤

### 1. 安装MySQL数据库

```bash
# 安装MySQL
sudo apt-get update
sudo apt-get install -y mysql-server

# 启动MySQL服务
sudo systemctl start mysql
sudo systemctl enable mysql

# 创建数据库和用户
sudo mysql -e "CREATE DATABASE IF NOT EXISTS database_name;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'username'@'localhost' IDENTIFIED BY 'password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### 2. 配置后端环境

```bash
cd backend

# 创建Python 3.9虚拟环境
python3.9 -m venv venv_py39
source venv_py39/bin/activate

# 安装依赖
pip install -r requirements.txt

# 修改.env文件中的数据库连接
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/database_name
```

### 3. 启动本地部署

```bash
# 在项目根目录下
chmod +x start_local_deployment.sh
./start_local_deployment.sh
```

启动脚本会：
- 检查MySQL服务状态
- 启动后端服务 (端口8001)
- 启动前端服务 (端口8081)
- 使用ngrok映射前端和后端服务到公网IP
- 显示访问地址

### 4. 停止本地部署

```bash
# 在项目根目录下
chmod +x stop_local_deployment.sh
./stop_local_deployment.sh
```

## 访问系统

启动脚本会显示两个URL：
- 前端访问地址：用于访问系统界面
- 后端访问地址：用于API调用

将前端访问地址分享给需要访问系统的用户即可。

## 常见问题排查

### 1. MySQL连接问题

**问题**：无法连接到MySQL数据库。

**解决方案**：
- 检查MySQL服务是否运行：`systemctl status mysql`
- 检查数据库用户和权限：`mysql -u username -ppassword -e "SHOW GRANTS;"`
- 检查数据库连接字符串是否正确

### 2. ngrok映射问题

**问题**：ngrok映射失败或无法访问。

**解决方案**：
- 检查ngrok日志：`cat /tmp/ngrok_frontend.log`
- 确保ngrok已正确安装：`ngrok --version`
- 重启ngrok服务：先停止再启动

### 3. 前后端连接问题

**问题**：前端无法连接到后端API。

**解决方案**：
- 检查后端服务是否正常运行：`curl http://localhost:8001/api/health`
- 检查前端配置文件中的API URL是否正确
- 检查浏览器控制台是否有CORS错误
