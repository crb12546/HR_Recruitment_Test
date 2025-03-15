# 认证模块实现文档

## 1. 概述

认证模块是HR招聘系统的核心组件，负责用户身份验证、权限控制和用户管理。本文档详细描述了认证模块的实现细节、API接口和使用方法。

## 2. 技术架构

### 2.1 认证流程

```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|   前端应用        |----->|   认证API         |----->|   数据库          |
|   (Vue.js)        |      |   (FastAPI)       |      |   (SQLite/MySQL)  |
|                   |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
        |                          |
        |                          |
        v                          v
+-------------------+      +-------------------+
|                   |      |                   |
|   本地存储        |      |   JWT令牌         |
|   (LocalStorage)  |      |                   |
|                   |      |                   |
+-------------------+      +-------------------+
```

### 2.2 技术栈

- **后端**：FastAPI + SQLAlchemy + JWT
- **前端**：Vue.js + Axios + Pinia
- **安全**：Bcrypt密码哈希 + JWT令牌

## 3. 后端实现

### 3.1 数据模型

用户模型（`app/models/user.py`）定义：

```python
class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 3.2 依赖注入

认证依赖（`app/api/deps.py`）实现：

```python
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """获取当前用户"""
    # 解析JWT令牌获取用户ID
    # 从数据库获取用户信息
    # 返回用户对象或抛出异常

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户"""
    # 检查用户是否活跃
    # 返回用户对象或抛出异常

def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前超级用户"""
    # 检查用户是否为超级用户
    # 返回用户对象或抛出异常
```

### 3.3 API端点

认证API（`app/api/endpoints/auth.py`）实现：

```python
@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """用户登录"""
    # 验证用户名和密码
    # 生成JWT令牌
    # 返回令牌

@router.post("/register", response_model=schemas.User)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名和邮箱是否已存在
    # 创建新用户
    # 返回用户信息

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    # 返回当前用户信息

@router.put("/me", response_model=schemas.User)
def update_user_me(
    user_in: schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """更新当前用户信息"""
    # 更新用户信息
    # 返回更新后的用户信息

@router.get("/users", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser),
):
    """获取用户列表（仅超级用户）"""
    # 获取用户列表
    # 返回用户列表
```

### 3.4 安全实现

安全模块（`app/core/security.py`）实现：

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # 使用Bcrypt验证密码

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    # 使用Bcrypt生成密码哈希

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """创建访问令牌"""
    # 使用PyJWT生成JWT令牌
```

## 4. 前端实现

### 4.1 API服务

认证API服务（`src/api/auth.js`）实现：

```javascript
const authApi = {
  /**
   * 用户登录
   * @param {Object} credentials - 登录凭证
   * @returns {Promise} - 返回登录结果
   */
  login: (credentials) => {
    return apiClient.post('/auth/login', credentials);
  },
  
  /**
   * 用户注册
   * @param {Object} userData - 用户数据
   * @returns {Promise} - 返回注册结果
   */
  register: (userData) => {
    return apiClient.post('/auth/register', userData);
  },
  
  /**
   * 获取当前用户信息
   * @returns {Promise} - 返回当前用户信息
   */
  getCurrentUser: () => {
    return apiClient.get('/auth/me');
  }
};
```

### 4.2 状态管理

认证状态管理（`src/store/index.js`）实现：

```javascript
// 方法：设置用户登录状态
setUserLoggedIn(username, token) {
  this.state.isLoggedIn = true;
  this.state.token = token;
  localStorage.setItem('token', token);
  
  // 设置API客户端的认证头
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  
  // 获取用户信息
  this.fetchUserInfo();
},

// 方法：设置用户信息
setUserInfo(user) {
  this.state.user = user;
},

// 方法：获取用户信息
async fetchUserInfo() {
  try {
    const response = await apiClient.get('/auth/me');
    this.setUserInfo(response.data);
  } catch (error) {
    console.error('获取用户信息失败:', error);
    // 如果获取用户信息失败，可能是token无效，执行登出
    if (error.response && error.response.status === 401) {
      this.logout();
    }
  }
},

// 方法：检查是否已认证
isAuthenticated() {
  // 检查本地存储中是否有token
  const token = localStorage.getItem('token');
  if (token) {
    // 如果有token但状态中没有，更新状态
    if (!this.state.token) {
      this.state.token = token;
      this.state.isLoggedIn = true;
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // 获取用户信息
      this.fetchUserInfo();
    }
    return true;
  }
  return false;
},

// 方法：用户登出
logout() {
  this.state.isLoggedIn = false;
  this.state.user = null;
  this.state.token = '';
  localStorage.removeItem('token');
  
  // 移除API客户端的认证头
  delete apiClient.defaults.headers.common['Authorization'];
}
```

### 4.3 路由守卫

路由守卫（`src/router/index.js`）实现：

```javascript
// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 检查路由是否需要认证
  if (to.meta.requiresAuth && !store.isAuthenticated()) {
    // 需要认证但未登录，重定向到登录页
    next({ name: 'Login' });
    return;
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin) {
    try {
      // 获取当前用户信息
      const currentUser = store.state.user;
      
      // 如果用户信息不存在或不是管理员，重定向到首页
      if (!currentUser || !currentUser.is_superuser) {
        next({ name: 'Home' });
        return;
      }
    } catch (error) {
      console.error('获取用户信息失败:', error);
      next({ name: 'Home' });
      return;
    }
  }
  
  // 不需要认证或已通过权限检查，正常导航
  next();
});
```

## 5. 用户界面

### 5.1 登录界面

登录界面（`src/views/Login.vue`）实现了以下功能：

- 用户名/密码登录表单
- 表单验证
- 错误提示
- 记住登录状态
- 跳转到注册页面

### 5.2 用户管理界面

用户管理界面（`src/views/admin/UserManagement.vue`）实现了以下功能：

- 用户列表展示
- 用户搜索和筛选
- 用户创建、编辑和删除
- 权限管理
- 分页功能

### 5.3 个人信息界面

个人信息界面（`src/views/Profile.vue`）实现了以下功能：

- 个人信息展示
- 个人信息编辑
- 密码修改
- 表单验证

## 6. 测试

### 6.1 后端测试

认证模块测试（`tests/api/test_auth_api.py`）包含以下测试用例：

- 用户登录测试
- 错误密码登录测试
- 用户注册测试
- 注册已存在用户名测试
- 获取当前用户信息测试
- 更新当前用户信息测试
- 普通用户获取用户列表测试（应该失败）
- 超级用户获取用户列表测试
- 超级用户创建用户测试
- 超级用户删除用户测试

### 6.2 前端测试

前端测试包含以下测试用例：

- 登录组件测试
- 注册组件测试
- 用户管理组件测试
- 个人信息组件测试
- 路由守卫测试
- 状态管理测试

## 7. 安全考虑

### 7.1 密码安全

- 使用Bcrypt进行密码哈希
- 密码强度验证
- 防止暴力破解攻击

### 7.2 令牌安全

- JWT令牌过期时间设置
- 令牌刷新机制
- HTTPS传输

### 7.3 权限控制

- 基于角色的访问控制
- API端点权限验证
- 前端路由守卫

## 8. 未来改进

### 8.1 功能改进

- 实现密码重置功能
- 添加多因素认证
- 实现OAuth2.0第三方登录
- 添加用户活动日志

### 8.2 性能改进

- 令牌缓存
- 用户信息缓存
- 批量用户操作

### 8.3 安全改进

- 添加请求频率限制
- 实现IP黑名单
- 增强密码策略
- 添加安全审计日志
