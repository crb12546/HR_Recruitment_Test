#!/bin/bash

# 本地部署启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}启动HR招聘系统本地部署...${NC}"

# 检查MySQL服务
echo -e "${YELLOW}检查MySQL服务...${NC}"
if ! systemctl is-active --quiet mysql; then
    echo -e "${RED}MySQL服务未运行，正在启动...${NC}"
    sudo systemctl start mysql
fi
echo "MySQL服务正常运行"

# 配置数据库连接
echo -e "${YELLOW}配置数据库连接...${NC}"
echo "请在启动前设置以下环境变量:"
echo "export DB_USER=数据库用户名"
echo "export DB_PASSWORD=数据库密码"
echo "export DB_NAME=数据库名称"

# 检查Python虚拟环境
echo -e "${YELLOW}检查Python虚拟环境...${NC}"
if [ ! -d "backend/venv" ]; then
    echo "创建Python虚拟环境..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn sqlalchemy pymysql
    cd ..
else
    echo "Python虚拟环境已存在"
fi

# 启动后端服务
echo -e "${YELLOW}启动后端服务...${NC}"
cd backend
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
python simple_fastapi.py &
backend_pid=$!
echo "后端服务已启动，PID: $backend_pid"
cd ..

# 等待后端服务启动
echo "等待后端服务启动..."
sleep 3

# 测试后端服务
echo -e "${YELLOW}测试后端服务...${NC}"
curl -s http://localhost:8001/api/health || echo "后端服务未响应，请检查日志"
echo ""

# 启动前端服务
echo -e "${YELLOW}启动前端服务...${NC}"
cd frontend/public
python -m http.server 8081 &
frontend_pid=$!
echo "前端服务已启动，PID: $frontend_pid"
cd ../..

echo -e "${GREEN}本地服务已启动${NC}"
echo "后端服务: http://localhost:8001"
echo "前端服务: http://localhost:8081"
echo ""

# 创建前端配置文件，用于连接后端
cat > frontend/public/config.js << EOLJS
// 前端配置文件
window.API_URL = "http://localhost:8001";
EOLJS

echo "已创建前端配置文件，连接到后端URL: http://localhost:8001"
echo ""
echo -e "${YELLOW}如需外部访问，请使用以下命令：${NC}"
echo "1. 映射前端服务: ngrok http 8081"
echo "2. 映射后端服务: ngrok http 8001"
echo ""
echo -e "${YELLOW}按Ctrl+C停止服务${NC}"

# 等待用户中断
wait
