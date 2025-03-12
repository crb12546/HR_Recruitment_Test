# 本地测试方案

## 概述

由于GitHub Actions付款问题，我们将采用本地测试方案来确保代码质量。本文档描述了如何在本地环境中运行测试，以及如何将测试结果集成到开发流程中。

## 后端测试

### 环境准备

1. 确保已安装Python 3.12及相关依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install pytest pytest-cov
   ```

### 运行测试

1. 运行所有测试：
   ```bash
   cd backend
   python -m pytest
   ```

2. 运行特定模块测试：
   ```bash
   python -m pytest tests/api/test_resumes_api.py
   ```

3. 生成测试覆盖率报告：
   ```bash
   python -m pytest --cov=app tests/
   ```

## 前端测试

### 环境准备

1. 确保已安装Node.js和npm：
   ```bash
   cd frontend
   npm install
   ```

### 运行测试

1. 运行所有测试：
   ```bash
   cd frontend
   npm test
   ```

2. 运行特定组件测试：
   ```bash
   npm test -- tests/components/JobList.spec.js
   ```

3. 生成测试覆盖率报告：
   ```bash
   npm test -- --coverage
   ```

## 测试结果管理

1. 测试结果应保存在项目根目录的`test_reports`文件夹中
2. 每次提交前应运行测试并确保通过
3. 测试覆盖率报告应定期审查，确保代码质量

## 集成到开发流程

1. 开发新功能前，先运行相关测试确认基线状态
2. 实现功能后，编写对应测试用例
3. 提交代码前，确保所有测试通过
4. 代码审查时，审查者应检查测试覆盖率和测试质量

## 测试最佳实践

1. 单元测试应该独立，不依赖外部服务
2. 使用mock对象模拟外部依赖
3. 测试应该快速执行，不应有长时间运行的测试
4. 测试应该可重复执行，不应有随机失败的情况
5. 测试应该有明确的断言，验证预期结果

## 常见问题解决

1. 测试数据库连接问题：使用SQLite内存数据库进行测试
2. 前端组件测试失败：检查Jest配置和组件依赖
3. 测试超时：优化测试执行时间，或增加超时设置
