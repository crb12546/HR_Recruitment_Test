#!/bin/bash

# 启动开发环境脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}启动HR招聘系统开发环境...${NC}"

# 检查Python版本
echo -e "${YELLOW}检查Python版本...${NC}"
python_version=$(python --version)
echo "当前Python版本: $python_version"

# 检查Node.js版本
echo -e "${YELLOW}检查Node.js版本...${NC}"
node_version=$(node --version)
echo "当前Node.js版本: $node_version"

# 启动后端服务
echo -e "${YELLOW}启动后端服务...${NC}"
cd backend
source venv_py39/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)
python simple_fastapi.py &
backend_pid=$!
echo "后端服务已启动，PID: $backend_pid"

# 等待后端服务启动
echo "等待后端服务启动..."
sleep 3

# 测试后端服务
echo -e "${YELLOW}测试后端服务...${NC}"
curl -s http://localhost:8001/api/health
echo ""

# 启动前端服务
echo -e "${YELLOW}启动前端服务...${NC}"
cd ../frontend
cd public
python -m http.server 8081 &
frontend_pid=$!
echo "前端服务已启动，PID: $frontend_pid"

echo -e "${GREEN}开发环境已启动${NC}"
echo "后端服务: http://localhost:8001"
echo "前端服务: http://localhost:8081"
echo ""
echo -e "${YELLOW}按Ctrl+C停止服务${NC}"

# 等待用户中断
wait
