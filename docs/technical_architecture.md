# AI智能招聘系统技术架构文档

## 1. 系统架构概述

AI智能招聘系统采用前后端分离的架构设计，主要分为以下几个部分：

1. **前端应用**：基于Vue.js的单页面应用
2. **后端API服务**：基于FastAPI的RESTful API服务
3. **数据库**：PostgreSQL关系型数据库
4. **AI服务**：集成GPT-4O API的智能分析服务
5. **文件存储服务**：用于存储简历和招聘文档

### 1.1 系统架构图

```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|   前端应用        |<---->|   后端API服务     |<---->|   数据库          |
|   (Vue.js)        |      |   (FastAPI)       |      |   (PostgreSQL)    |
|                   |      |                   |      |                   |
+-------------------+      +------+------+-----+      +-------------------+
                                  |      |
                                  |      |
                          +-------v------v-------+    +-------------------+
                          |                      |    |                   |
                          |   AI服务            |<--->|   文件存储服务    |
                          |   (GPT-4O API)      |    |                   |
                          |                      |    |                   |
                          +----------------------+    +-------------------+
```

## 2. 前端架构

### 2.1 技术栈

- **框架**：Vue.js 3.x (使用Composition API)
- **状态管理**：Pinia
- **路由**：Vue Router
- **UI组件库**：Element Plus
- **HTTP客户端**：Axios
- **数据可视化**：ECharts
- **构建工具**：Vite

### 2.2 目录结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/          # 资源文件（图片、样式等）
│   ├── components/      # 通用组件
│   │   ├── common/      # 公共组件
│   │   ├── resume/      # 简历相关组件
│   │   ├── job/         # 职位相关组件
│   │   ├── interview/   # 面试相关组件
│   │   └── report/      # 报告相关组件
│   ├── views/           # 页面视图
│   │   ├── dashboard/   # 仪表盘页面
│   │   ├── resume/      # 简历管理页面
│   │   ├── job/         # 职位管理页面
│   │   ├── matching/    # 匹配结果页面
│   │   └── plan/        # 招聘方案页面
│   ├── router/          # 路由配置
│   ├── store/           # 状态管理
│   ├── api/             # API请求
│   ├── utils/           # 工具函数
│   ├── hooks/           # 自定义钩子
│   ├── constants/       # 常量定义
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── tests/               # 测试文件
├── .eslintrc.js         # ESLint配置
├── .prettierrc          # Prettier配置
├── vite.config.js       # Vite配置
└── package.json         # 项目依赖
```

### 2.3 组件设计

前端组件采用原子设计模式，分为以下几个层次：

1. **原子组件**：基础UI元素，如按钮、输入框等
2. **分子组件**：由多个原子组件组成的功能组件，如表单、卡片等
3. **有机体组件**：完整的功能模块，如简历上传组件、职位匹配组件等
4. **模板**：页面布局模板
5. **页面**：完整的页面视图

## 3. 后端架构

### 3.1 技术栈

- **框架**：FastAPI
- **ORM**：SQLAlchemy
- **数据库**：PostgreSQL
- **认证**：JWT
- **文档**：Swagger UI / ReDoc
- **测试**：Pytest

### 3.2 目录结构

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/    # API端点
│   │   │   ├── auth.py   # 认证相关
│   │   │   ├── resume.py # 简历相关
│   │   │   ├── job.py    # 职位相关
│   │   │   ├── match.py  # 匹配相关
│   │   │   └── plan.py   # 方案相关
│   │   └── api.py        # API路由注册
│   ├── core/             # 核心模块
│   │   ├── config.py     # 配置
│   │   ├── security.py   # 安全相关
│   │   └── errors.py     # 错误处理
│   ├── db/               # 数据库
│   │   ├── base.py       # 基础模型
│   │   ├── session.py    # 会话管理
│   │   └── init_db.py    # 数据库初始化
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── resume.py     # 简历模型
│   │   ├── job.py        # 职位模型
│   │   ├── match.py      # 匹配模型
│   │   └── plan.py       # 方案模型
│   ├── schemas/          # Pydantic模型
│   │   ├── user.py       # 用户模式
│   │   ├── resume.py     # 简历模式
│   │   ├── job.py        # 职位模式
│   │   ├── match.py      # 匹配模式
│   │   └── plan.py       # 方案模式
│   ├── services/         # 业务逻辑
│   │   ├── ai_service.py # AI服务
│   │   ├── file_service.py # 文件服务
│   │   ├── resume_service.py # 简历服务
│   │   └── job_service.py # 职位服务
│   ├── utils/            # 工具函数
│   └── main.py           # 应用入口
├── tests/                # 测试
├── alembic/              # 数据库迁移
├── .env                  # 环境变量
└── requirements.txt      # 项目依赖
```

### 3.3 API设计

API遵循RESTful设计原则，主要包括以下几个部分：

1. **认证API**：用户登录、注册、权限管理
2. **简历API**：简历上传、解析、管理
3. **职位API**：职位需求上传、解析、管理
4. **匹配API**：简历与职位匹配
5. **方案API**：招聘方案生成、管理

## 4. 数据库设计

### 4.1 ER图

```
+---------------+       +---------------+       +---------------+
|    User       |       |    Job        |       |   Resume      |
+---------------+       +---------------+       +---------------+
| id            |       | id            |       | id            |
| username      |       | title         |       | name          |
| email         |       | description   |       | contact       |
| password_hash |       | skills        |       | skills        |
| role          |       | experience    |       | experience    |
| created_at    |       | education     |       | education     |
| updated_at    |       | location      |       | file_path     |
+------+--------+       | created_at    |       | created_at    |
       |                | updated_at    |       | updated_at    |
       |                +-------+-------+       +-------+-------+
       |                        |                       |
       |                        |                       |
       |                        v                       |
       |                +-------+-------+               |
       +--------------->    JobUser     <--------------+
                      +---------------+
                      | id            |
                      | job_id        |
                      | user_id       |
                      | created_at    |
                      +---------------+
                              |
                              |
                              v
                      +-------+-------+       +---------------+
                      |   Match       |       |   Plan        |
                      +---------------+       +---------------+
                      | id            |       | id            |
                      | job_id        |       | job_id        |
                      | resume_id     |       | content       |
                      | total_score   |       | candidates    |
                      | skill_score   |       | created_at    |
                      | exp_score     |       | updated_at    |
                      | edu_score     |       +---------------+
                      | created_at    |
                      +---------------+
```

### 4.2 主要表结构

#### 用户表 (users)
- id: 主键
- username: 用户名
- email: 邮箱
- password_hash: 密码哈希
- role: 角色（管理员、HR等）
- created_at: 创建时间
- updated_at: 更新时间

#### 职位表 (jobs)
- id: 主键
- title: 职位名称
- description: 职位描述
- skills: 技能要求（JSON）
- experience: 经验要求
- education: 学历要求
- location: 工作地点
- created_at: 创建时间
- updated_at: 更新时间

#### 简历表 (resumes)
- id: 主键
- name: 候选人姓名
- contact: 联系方式（JSON）
- skills: 技能（JSON）
- experience: 工作经验（JSON）
- education: 教育背景（JSON）
- file_path: 原始文件路径
- created_at: 创建时间
- updated_at: 更新时间

#### 匹配表 (matches)
- id: 主键
- job_id: 职位ID（外键）
- resume_id: 简历ID（外键）
- total_score: 总匹配分数
- skill_score: 技能匹配分数
- exp_score: 经验匹配分数
- edu_score: 学历匹配分数
- created_at: 创建时间

#### 方案表 (plans)
- id: 主键
- job_id: 职位ID（外键）
- content: 方案内容（JSON）
- candidates: 候选人ID列表（JSON）
- created_at: 创建时间
- updated_at: 更新时间

## 5. AI服务集成

### 5.1 GPT-4O API集成

系统将通过OpenAI的API集成GPT-4O，主要用于以下功能：

1. **文档解析**：解析招聘需求文档和简历
2. **智能匹配**：计算简历与职位的匹配度
3. **方案生成**：生成招聘方案和推荐理由

### 5.2 AI服务架构

```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|   后端API服务     |<---->|   AI服务管理器    |<---->|   GPT-4O API      |
|                   |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
                                    |
                                    |
                           +--------v--------+
                           |                 |
                           |   AI模型缓存    |
                           |                 |
                           +-----------------+
```

### 5.3 AI服务实现

AI服务将通过以下类实现：

```python
class GPTService:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    async def parse_document(self, content: str, doc_type: str) -> dict:
        """解析文档内容"""
        # 实现文档解析逻辑
        
    async def match_resume_to_job(self, resume: dict, job: dict) -> dict:
        """匹配简历与职位"""
        # 实现匹配逻辑
        
    async def generate_plan(self, job: dict, matches: list) -> dict:
        """生成招聘方案"""
        # 实现方案生成逻辑
```

## 6. 部署架构

### 6.1 开发环境

- 本地开发环境
- Docker容器化开发

### 6.2 测试环境

- 测试服务器
- CI/CD集成（GitHub Actions）

### 6.3 生产环境

- 云服务器部署
- 容器编排（Kubernetes）
- 负载均衡
- 数据库主从复制

### 6.4 部署流程

```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|   代码仓库        |----->|   CI/CD流水线     |----->|   容器仓库        |
|   (GitHub)        |      |   (GitHub Actions)|      |   (Docker Hub)    |
|                   |      |                   |      |                   |
+-------------------+      +-------------------+      +--------+----------+
                                                               |
                                                               |
                                                               v
+-------------------+      +-------------------+      +--------+----------+
|                   |      |                   |      |                   |
|   监控系统        |<-----|   Kubernetes集群  |<-----|   容器编排        |
|   (Prometheus)    |      |                   |      |   (Kubernetes)    |
|                   |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
```

## 7. 安全架构

### 7.1 认证与授权

- JWT认证
- 基于角色的访问控制（RBAC）
- OAuth2.0集成（可选）

### 7.2 数据安全

- 数据加密存储
- HTTPS传输
- 敏感信息脱敏

### 7.3 安全监控

- 日志审计
- 异常行为检测
- 定期安全扫描

## 8. 性能优化

### 8.1 前端优化

- 代码分割
- 懒加载
- 资源压缩
- CDN加速

### 8.2 后端优化

- 数据库索引优化
- 查询缓存
- 异步处理
- 水平扩展

### 8.3 AI服务优化

- 模型结果缓存
- 批量处理
- 异步调用

## 9. 监控与日志

### 9.1 监控系统

- 系统监控（CPU、内存、磁盘等）
- 应用监控（响应时间、错误率等）
- 业务监控（用户活跃度、功能使用率等）

### 9.2 日志系统

- 应用日志
- 访问日志
- 错误日志
- 安全日志

### 9.3 告警系统

- 阈值告警
- 异常检测
- 多渠道通知（邮件、短信、钉钉等）

## 10. 灾备与恢复

### 10.1 数据备份

- 定时全量备份
- 增量备份
- 多地备份

### 10.2 灾难恢复

- 故障转移
- 数据恢复
- 业务连续性计划

## 11. 扩展性设计

系统设计考虑未来的扩展性，主要包括：

1. **模块化设计**：便于添加新功能
2. **微服务架构**：便于服务独立扩展
3. **API版本控制**：便于API升级
4. **插件系统**：便于第三方集成

## 12. 技术债务管理

为了保持系统的可维护性，将采取以下措施管理技术债务：

1. **代码审查**：确保代码质量
2. **单元测试**：确保功能正确性
3. **重构计划**：定期重构代码
4. **文档更新**：保持文档与代码同步
