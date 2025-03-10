#!/bin/bash

# 前端测试脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始前端测试...${NC}"

# 检查Node.js版本
echo -e "${YELLOW}检查Node.js版本...${NC}"
node_version=$(node --version)
echo "当前Node.js版本: $node_version"

# 检查npm版本
echo -e "${YELLOW}检查npm版本...${NC}"
npm_version=$(npm --version)
echo "当前npm版本: $npm_version"

# 检查前端依赖
echo -e "${YELLOW}检查前端依赖...${NC}"
if [ -d "node_modules" ]; then
  echo "node_modules目录已存在"
else
  echo "node_modules目录不存在，安装依赖..."
  npm install --legacy-peer-deps
fi

# 检查前端服务器
echo -e "${YELLOW}检查前端服务器...${NC}"
if pgrep -f "http.server 8081" > /dev/null; then
  echo "前端服务器已运行"
else
  echo "前端服务器未运行，启动服务器..."
  cd public
  python -m http.server 8081 &
  cd ..
  echo "前端服务器已启动"
fi

# 等待服务器启动
echo "等待前端服务器启动..."
sleep 2

# 测试前端页面
echo -e "${YELLOW}测试前端页面...${NC}"
curl -s http://localhost:8081 > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}前端页面访问成功${NC}"
else
  echo -e "${RED}前端页面访问失败${NC}"
  exit 1
fi

# 测试前端与后端连接
echo -e "${YELLOW}测试前端与后端连接...${NC}"
# 检查后端服务器
if pgrep -f "simple_fastapi.py" > /dev/null; then
  echo "后端服务器已运行"
else
  echo "后端服务器未运行，启动服务器..."
  cd ../backend
  source venv_py39/bin/activate
  export PYTHONPATH=$PYTHONPATH:$(pwd)
  python simple_fastapi.py &
  cd ../frontend
  echo "后端服务器已启动"
  sleep 2
fi

# 测试后端API
echo -e "${YELLOW}测试后端API...${NC}"
curl -s http://localhost:8001/api/health > /dev/null
if [ $? -eq 0 ]; then
  echo -e "${GREEN}后端API访问成功${NC}"
else
  echo -e "${RED}后端API访问失败${NC}"
  exit 1
fi

echo -e "${GREEN}前端测试完成${NC}"
