# 招聘需求模块实现文档

## 1. 概述

招聘需求模块（B2系列任务）是HR招聘系统的核心功能之一，用于管理企业的招聘岗位需求。该模块支持招聘需求的创建、编辑、查询和删除，并提供文档智能解析功能，大幅提高HR人员的工作效率。

## 2. 功能特性

### 2.1 需求上传功能（B2-1）

- **文档上传**：支持上传Word、PDF等格式的招聘需求文档
- **智能解析**：使用GPT-4O API自动提取文档中的职位信息
- **预览编辑**：解析结果支持人工预览和编辑后再保存

### 2.2 需求解析集成（B2-2）

- **GPT-4O集成**：使用OpenAI的GPT-4O模型进行文档内容解析
- **结构化提取**：从非结构化文档中提取职位名称、部门、职责、要求等信息
- **标签生成**：自动为职位生成技能标签，便于后续匹配

### 2.3 需求管理界面（B2-3）

- **列表视图**：展示所有招聘需求，支持筛选和排序
- **详情视图**：查看招聘需求的详细信息
- **批量操作**：支持批量删除、导出等操作

### 2.4 需求编辑功能（B2-4）

- **表单编辑**：提供结构化表单编辑招聘需求
- **实时保存**：编辑过程中自动保存草稿
- **历史版本**：记录编辑历史，支持版本回溯

## 3. 技术实现

### 3.1 后端实现

#### 3.1.1 数据模型

```python
class JobRequirement(Base):
    """招聘需求模型"""
    __tablename__ = "job_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False, comment="职位名称")
    department = Column(String(50), comment="部门")
    responsibilities = Column(Text, comment="职责描述")
    requirements = Column(Text, comment="职位要求")
    salary_range = Column(String(50), comment="薪资范围")
    location = Column(String(50), comment="工作地点")
    tags = Column(ARRAY(String), comment="职位标签")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 3.1.2 API端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/jobs | 获取招聘需求列表 |
| GET | /api/v1/jobs/{id} | 获取招聘需求详情 |
| POST | /api/v1/jobs | 创建招聘需求 |
| PUT | /api/v1/jobs/{id} | 更新招聘需求 |
| DELETE | /api/v1/jobs/{id} | 删除招聘需求 |
| POST | /api/v1/jobs/parse | 解析招聘需求文档（不保存） |
| POST | /api/v1/jobs/upload | 上传并解析招聘需求文档 |

#### 3.1.3 文档解析实现

```python
def parse_job_requirement(self, document_content: str) -> Dict[str, Any]:
    """解析招聘需求文档"""
    # 构建提示词
    prompt = f"""
    请解析以下招聘需求文档，提取关键信息，并以JSON格式返回。
    需要提取的字段包括：
    - position_name: 职位名称
    - department: 部门
    - responsibilities: 工作职责（详细描述）
    - requirements: 任职要求（详细描述）
    - salary_range: 薪资范围
    - location: 工作地点
    
    招聘需求文档内容：
    {document_content}
    """
    
    # 调用GPT-4O API
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": "你是一位专业的HR招聘助手，擅长解析招聘需求文档。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000,
        response_format={"type": "json_object"}
    )
    
    # 解析JSON响应
    content = response.choices[0].message.content
    parsed_content = json.loads(content)
    
    return parsed_content
```

### 3.2 前端实现

#### 3.2.1 组件结构

- **JobRequirementList.vue**：招聘需求列表页面
- **JobRequirementDetail.vue**：招聘需求详情页面
- **JobRequirementEdit.vue**：招聘需求编辑页面
- **JobRequirementForm.vue**：招聘需求表单组件（用于创建和编辑）

#### 3.2.2 API服务

```javascript
// 解析招聘需求文档（不保存）
export const parseJobRequirementDocument = (formData) => {
  return apiClient.post('/jobs/parse', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => response.data)
}

// 上传并解析招聘需求文档
export const uploadJobRequirementDocument = (formData) => {
  return apiClient.post('/jobs/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => response.data)
}
```

#### 3.2.3 路由配置

```javascript
// 招聘需求路由
{
  path: '/jobs',
  name: 'JobList',
  component: () => import('../views/job/JobRequirementList.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/jobs/create',
  name: 'JobCreate',
  component: () => import('../views/job/JobRequirementEdit.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/jobs/:id',
  name: 'JobDetail',
  component: () => import('../views/job/JobRequirementDetail.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/jobs/:id/edit',
  name: 'JobEdit',
  component: () => import('../views/job/JobRequirementEdit.vue'),
  meta: { requiresAuth: true }
},
{
  path: '/jobs/upload',
  name: 'JobUpload',
  component: () => import('../views/job/JobUpload.vue'),
  meta: { requiresAuth: true }
}
```

## 4. 测试覆盖

### 4.1 后端测试

- **单元测试**：测试招聘需求的CRUD操作
- **集成测试**：测试文档解析和上传功能
- **模拟测试**：使用模拟服务测试GPT-4O API集成

### 4.2 前端测试

- **组件测试**：测试各个组件的渲染和交互
- **E2E测试**：测试完整的用户流程

## 5. 未来改进

- **批量导入**：支持批量导入招聘需求
- **模板管理**：提供招聘需求模板管理功能
- **多语言支持**：支持多语言招聘需求解析
- **智能推荐**：基于历史数据智能推荐招聘需求内容
