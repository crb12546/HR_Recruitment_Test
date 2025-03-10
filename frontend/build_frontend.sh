#!/bin/bash

# 前端构建脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}开始构建前端...${NC}"

# 检查Node.js版本
echo -e "${YELLOW}检查Node.js版本...${NC}"
node_version=$(node --version)
echo "当前Node.js版本: $node_version"

# 检查npm版本
echo -e "${YELLOW}检查npm版本...${NC}"
npm_version=$(npm --version)
echo "当前npm版本: $npm_version"

# 安装依赖
echo -e "${YELLOW}安装依赖...${NC}"
npm install --legacy-peer-deps

# 构建前端
echo -e "${YELLOW}构建前端...${NC}"
if [ -f "package.json" ]; then
  if grep -q "build" package.json; then
    npm run build
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}前端构建成功${NC}"
    else
      echo -e "${RED}前端构建失败${NC}"
      exit 1
    fi
  else
    echo "package.json中没有build脚本，使用简化构建..."
    mkdir -p dist
    cp -r public/* dist/
    echo -e "${GREEN}简化构建完成${NC}"
  fi
else
  echo -e "${RED}package.json不存在，无法构建${NC}"
  exit 1
fi

# 检查构建结果
echo -e "${YELLOW}检查构建结果...${NC}"
if [ -d "dist" ]; then
  echo -e "${GREEN}构建目录存在${NC}"
  ls -la dist
else
  echo -e "${RED}构建目录不存在，构建失败${NC}"
  exit 1
fi

echo -e "${GREEN}前端构建完成${NC}"
