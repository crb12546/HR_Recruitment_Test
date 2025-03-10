# AI集成文档

## 概述

HR招聘系统使用GPT-4O模型提供智能分析功能，包括简历解析、人才画像生成、招聘需求匹配和招聘方案生成等。本文档描述了AI服务的集成方式和使用方法。

## 技术架构

AI服务采用服务工厂模式实现，支持在不同环境中使用不同的服务实现：

- 生产环境：使用真实的OpenAI GPT-4O API
- 开发/测试环境：使用模拟服务，无需API密钥

## 服务功能

AI服务提供以下核心功能：

1. **简历解析**：从简历文档中提取结构化信息
2. **人才画像生成**：基于简历内容生成候选人画像
3. **标签提取**：从简历和职位描述中提取关键技能标签
4. **简历与职位匹配**：评估候选人与职位的匹配度
5. **招聘方案生成**：根据职位需求和候选人匹配结果生成招聘方案

## 配置说明

### 环境变量

AI服务需要以下环境变量：

```
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 服务配置
# 设置为True使用模拟服务，适用于开发和测试环境
MOCK_SERVICES=True
```

### 模型配置

默认使用的模型为`gpt-4o`，可在`app/core/config.py`中修改：

```python
GPT_MODEL: str = "gpt-4o"
```

## 使用方法

### 获取AI服务实例

```python
from app.services.service_factory import get_ai_service

# 获取AI服务实例
ai_service = get_ai_service()
```

### 简历解析

```python
# 解析简历内容
parsed_content = ai_service.parse_resume(ocr_content)
```

### 人才画像生成

```python
# 生成人才画像
talent_portrait = ai_service.generate_talent_portrait(parsed_content)
```

### 标签提取

```python
# 从简历中提取标签
resume_tags = ai_service.generate_resume_tags(resume_content)

# 从职位描述中提取标签
job_tags = ai_service.extract_job_tags(job_description)
```

### 简历与职位匹配

```python
# 匹配简历与职位需求
match_result = ai_service.match_resume_to_job(resume_content, job_requirements)
```

### 招聘方案生成

```python
# 生成招聘方案
plan = ai_service.generate_recruitment_plan(job_requirement, matched_resumes)
```

## 错误处理

AI服务实现了完善的错误处理机制，包括：

1. 输入验证：检查输入参数是否有效
2. 异常捕获：捕获并记录API调用过程中的异常
3. 降级策略：在API调用失败时返回默认值或空结果
4. 日志记录：记录详细的错误信息，便于问题排查

## 测试

可以使用模拟服务进行测试，无需真实的API密钥：

```python
# 设置环境变量
os.environ["MOCK_SERVICES"] = "True"

# 获取AI服务实例（将返回模拟实现）
ai_service = get_ai_service()
```

## 性能优化

为提高性能和降低API调用成本，可以考虑以下优化措施：

1. 缓存常用结果
2. 批量处理请求
3. 调整模型参数（如temperature、max_tokens等）
4. 实现请求限流和重试机制
