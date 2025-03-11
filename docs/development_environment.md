# HR招聘系统开发环境搭建文档

## 概述

本文档提供HR招聘系统的开发环境搭建指南，包括环境要求、安装步骤、配置说明和常见问题排查。通过本文档，开发团队成员可以快速配置开发环境并开始项目开发工作。

HR招聘系统采用前后端分离架构：
- 后端：FastAPI (Python 3.9)
- 前端：Vue.js 3.x
- 数据库：开发环境使用SQLite，生产环境使用MySQL
- AI服务：集成GPT-4O API

## 环境要求

### 后端环境要求
- Python 3.9
- 虚拟环境工具 (venv)
- FastAPI 0.115.11
- SQLAlchemy 2.0.7
- Pydantic 2.10.6
- 其他依赖见 `backend/requirements.txt`

### 前端环境要求
- Node.js 14+
- npm 6+
- Vue.js 3.2.47
- Element Plus 2.9.6
- 其他依赖见 `frontend/package.json`

### 开发工具建议
- Visual Studio Code 或 PyCharm (后端开发)
- Visual Studio Code 或 WebStorm (前端开发)
- Postman 或 Insomnia (API测试)

## 环境搭建步骤

### 1. 克隆代码库
```bash
git clone https://github.com/crb12546/HR_Recruitment_Test.git
cd HR_Recruitment_Test
```

### 2. 后端环境搭建
```bash
cd backend

# 创建Python 3.9虚拟环境
python3.9 -m venv venv_py39
source venv_py39/bin/activate  # Linux/Mac
# 或 venv_py39\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env  # 如果.env文件不存在，复制一份
# 编辑.env文件，设置必要的环境变量
```

#### 环境变量配置
编辑`.env`文件，设置以下环境变量：
```
# 环境
ENV=development

# 数据库配置
DATABASE_URL=sqlite:///./hr_recruitment.db

# 安全配置
SECRET_KEY=hr_recruitment_secret_key_for_development

# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 服务配置
MOCK_SERVICES=True
```

### 3. 前端环境搭建
```bash
cd frontend

# 安装依赖
npm install --legacy-peer-deps

# 如果遇到依赖冲突，可以尝试以下命令
npm install --force
```

## 启动开发环境

### 方法一：使用一键启动脚本
项目根目录提供了一键启动脚本，可以同时启动前端和后端服务：
```bash
# 在项目根目录下
./start_dev_environment.sh
```

脚本会自动：
- 检查Python和Node.js版本
- 启动后端服务（端口8001）
- 启动前端服务（端口8081）
- 显示服务访问地址

### 方法二：分别启动服务

#### 启动后端服务
```bash
cd backend
source venv_py39/bin/activate  # Linux/Mac
# 或 venv_py39\Scripts\activate  # Windows

# 设置Python路径
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Linux/Mac
# 或 set PYTHONPATH=%PYTHONPATH%;%cd%  # Windows

# 启动服务
python simple_fastapi.py
# 或使用脚本
./start_backend.sh
```

后端服务将在 http://localhost:8001 上运行。

#### 启动前端服务
```bash
cd frontend

# 开发模式启动
npm run serve
# 或使用简化服务器
./start_frontend.sh
# 或 python -m http.server 8081 --directory ./public
```

前端服务将在 http://localhost:8080 或 http://localhost:8081 上运行（取决于启动方式）。

## Docker开发环境

项目支持使用Docker进行开发和测试，特别适合团队成员使用不同操作系统的情况。

### 使用Docker Compose启动开发环境
```bash
# 在项目根目录下
docker-compose up -d
```

这将启动：
- 后端服务 (http://localhost:8001)
- 前端服务 (http://localhost:8080)
- MySQL数据库 (端口3306)

### 查看容器日志
```bash
# 查看所有容器日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## 常见问题排查

### 1. Python版本兼容性问题
**问题**：使用Python 3.12时出现FastAPI或Pydantic导入错误。
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

**解决方案**：
- 使用Python 3.9创建虚拟环境
- 或更新FastAPI和Pydantic到兼容版本：
  ```bash
  pip install fastapi==0.115.11 pydantic==2.10.6
  ```

### 2. 前端依赖冲突
**问题**：安装前端依赖时出现版本冲突错误。

**解决方案**：
```bash
npm install --legacy-peer-deps
# 或
npm install --force
```

### 3. 数据库连接问题
**问题**：后端启动时出现数据库连接错误。

**解决方案**：
- 检查`.env`文件中的`DATABASE_URL`配置
- 确保SQLite数据库文件路径正确
- 如果使用MySQL，确保数据库服务已启动

### 4. 端口占用问题
**问题**：启动服务时提示端口已被占用。

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8001  # 查找占用8001端口的进程
lsof -i :8081  # 查找占用8081端口的进程

# 终止进程
kill -9 <进程ID>
```

## 开发工作流

### 代码提交流程
1. 创建功能分支
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 开发功能并提交更改
   ```bash
   git add <修改的文件>
   git commit -m "描述你的更改"
   ```

3. 推送到远程仓库
   ```bash
   git push origin feature/your-feature-name
   ```

4. 创建Pull Request
   - 在GitHub上创建PR，请求合并到main分支
   - 等待代码审核和CI/CD检查
   - 根据反馈进行修改
   - 合并PR

### 测试
- 后端单元测试：
  ```bash
  cd backend
  python -m pytest tests/
  ```

- 前端测试：
  ```bash
  cd frontend
  npm run test
  ```

## 文档历史

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| 1.0 | 2025-03-11 | 初始版本 | Devin |
