# HR招聘系统部署文档

## 部署环境要求

### 后端环境
- Python 3.9
- FastAPI 0.95.0
- SQLAlchemy 2.0.7
- 数据库：MySQL（生产环境）/ SQLite（开发环境）
- 其他依赖见 `backend/requirements.txt`

### 前端环境
- Node.js 14+
- Vue.js 3.2+
- Element Plus 2.2+
- 其他依赖见 `frontend/package.json`

## 开发环境部署

### 1. 克隆代码库
```bash
git clone https://github.com/crb12546/HR_Recruitment_Test.git
cd HR_Recruitment_Test
```

### 2. 后端部署
```bash
cd backend

# 创建Python 3.9虚拟环境
python3.9 -m venv venv_py39
source venv_py39/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置必要的环境变量

# 初始化数据库
python setup_db.py

# 启动后端服务
./start_backend.sh
```

### 3. 前端部署
```bash
cd frontend

# 安装依赖
npm install --legacy-peer-deps

# 启动前端服务
./start_frontend.sh
```

### 4. 使用开发环境启动脚本
```bash
# 在项目根目录下
./start_dev_environment.sh
```

## 生产环境部署

### 1. 后端部署

#### 使用Docker部署
```bash
cd backend

# 构建Docker镜像
docker build -t hr-recruitment-backend .

# 运行Docker容器
docker run -d -p 8001:8001 --name hr-backend \
  --env-file .env.prod \
  hr-recruitment-backend
```

#### 使用Fly.io部署
```bash
cd backend

# 安装Fly CLI
curl -L https://fly.io/install.sh | sh

# 登录Fly.io
fly auth login

# 部署应用
fly launch --name hr-recruitment-backend
fly secrets set $(cat .env.prod)
fly deploy
```

### 2. 前端部署

#### 构建前端
```bash
cd frontend

# 安装依赖
npm install --legacy-peer-deps

# 构建生产版本
npm run build
```

#### 使用Netlify部署
```bash
# 安装Netlify CLI
npm install -g netlify-cli

# 登录Netlify
netlify login

# 部署应用
netlify deploy --prod --dir=dist
```

## 环境变量配置

### 后端环境变量
- `ENV`: 环境类型（development/production）
- `DATABASE_URL`: 数据库连接URL
- `SECRET_KEY`: 应用密钥
- `OPENAI_API_KEY`: OpenAI API密钥
- `MOCK_SERVICES`: 是否使用模拟服务（True/False）

### 前端环境变量
- `VUE_APP_API_URL`: 后端API地址
- `VUE_APP_ENV`: 环境类型（development/production）

## 数据库迁移

```bash
cd backend

# 创建迁移
alembic revision --autogenerate -m "迁移描述"

# 应用迁移
alembic upgrade head
```

## 监控与日志

### 后端日志
- 日志文件位于 `backend/logs/`
- 生产环境使用 `fly logs` 查看日志

### 前端监控
- 使用浏览器开发者工具（F12）查看控制台日志
- 生产环境可集成Sentry进行错误监控

## 常见问题排查

1. **数据库连接问题**
   - 检查数据库连接URL是否正确
   - 确认数据库服务是否运行
   - 检查数据库用户权限

2. **API调用失败**
   - 检查CORS配置
   - 验证API路径是否正确
   - 检查认证令牌是否有效

3. **OpenAI API调用问题**
   - 验证API密钥是否有效
   - 检查API调用限制
   - 考虑使用模拟服务进行测试

4. **前端构建问题**
   - 清除node_modules并重新安装
   - 使用 `--legacy-peer-deps` 解决依赖冲突
   - 检查Node.js版本兼容性
