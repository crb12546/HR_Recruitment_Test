# GitHub Actions配置说明

## 必要的密钥配置

在GitHub仓库设置中，需要添加以下密钥：

1. `FLY_API_TOKEN`: Fly.io API令牌，用于部署应用
2. `DATABASE_URL`: 生产环境数据库URL
3. `SECRET_KEY`: 应用密钥
4. `OPENAI_API_KEY`: OpenAI API密钥

## 配置步骤

1. 在GitHub仓库页面，点击"Settings"
2. 在左侧菜单中选择"Secrets and variables" -> "Actions"
3. 点击"New repository secret"按钮
4. 添加上述密钥

## 获取Fly.io API令牌

1. 安装Fly.io CLI: `curl -L https://fly.io/install.sh | sh`
2. 登录Fly.io: `fly auth login`
3. 获取令牌: `fly auth token`
4. 将获取的令牌添加到GitHub密钥中
