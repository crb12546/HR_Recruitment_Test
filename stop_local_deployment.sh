#!/bin/bash

# 停止本地部署脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}停止HR招聘系统本地部署...${NC}"

# 停止ngrok进程
echo "停止ngrok进程..."
pkill -f "ngrok http"

# 停止前端服务
echo "停止前端服务..."
pkill -f "python -m http.server 8081"

# 停止后端服务
echo "停止后端服务..."
pkill -f "python simple_fastapi.py"

echo -e "${GREEN}所有服务已停止${NC}"
