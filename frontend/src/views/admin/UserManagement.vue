<template>
  <div class="user-management-container">
    <h1>用户管理</h1>
    
    <!-- 用户列表 -->
    <div class="user-list-container">
      <div class="table-header">
        <h2>用户列表</h2>
        <el-button type="primary" @click="showCreateUserDialog">添加用户</el-button>
      </div>
      
      <el-table :data="users" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="full_name" label="姓名" width="150" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '已激活' : '未激活' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="角色" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_superuser ? 'warning' : 'info'">
              {{ scope.row.is_superuser ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="showEditUserDialog(scope.row)">编辑</el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="confirmDeleteUser(scope.row)"
              :disabled="scope.row.id === currentUser?.id"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 创建用户对话框 -->
    <el-dialog
      v-model="createUserDialogVisible"
      title="添加用户"
      width="500px"
    >
      <el-form :model="newUser" label-width="100px" :rules="userFormRules" ref="createUserForm">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="newUser.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="newUser.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="newUser.password" type="password" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="newUser.full_name" />
        </el-form-item>
        <el-form-item label="是否激活">
          <el-switch v-model="newUser.is_active" />
        </el-form-item>
        <el-form-item label="是否管理员">
          <el-switch v-model="newUser.is_superuser" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createUserDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createUser" :loading="loading">
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="editUserDialogVisible"
      title="编辑用户"
      width="500px"
    >
      <el-form :model="editingUser" label-width="100px" :rules="editUserFormRules" ref="editUserForm">
        <el-form-item label="用户名">
          <el-input v-model="editingUser.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editingUser.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="editingUser.password" type="password" placeholder="留空表示不修改密码" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="editingUser.full_name" />
        </el-form-item>
        <el-form-item label="是否激活">
          <el-switch v-model="editingUser.is_active" />
        </el-form-item>
        <el-form-item label="是否管理员">
          <el-switch v-model="editingUser.is_superuser" :disabled="editingUser.id === currentUser?.id" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editUserDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateUser" :loading="loading">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import userApi from '../../api/user'
import { store } from '../../store'

export default {
  name: 'UserManagement',
  setup() {
    // 用户列表
    const users = ref([])
    const loading = ref(false)
    
    // 当前登录用户
    const currentUser = computed(() => store.state.user)
    
    // 创建用户相关
    const createUserDialogVisible = ref(false)
    const createUserForm = ref(null)
    const newUser = reactive({
      username: '',
      email: '',
      password: '',
      full_name: '',
      is_active: true,
      is_superuser: false
    })
    
    // 编辑用户相关
    const editUserDialogVisible = ref(false)
    const editUserForm = ref(null)
    const editingUser = reactive({
      id: null,
      username: '',
      email: '',
      password: '',
      full_name: '',
      is_active: true,
      is_superuser: false
    })
    
    // 表单验证规则
    const userFormRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
      ]
    }
    
    const editUserFormRules = {
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
      ]
    }
    
    // 获取用户列表
    const fetchUsers = async () => {
      loading.value = true
      try {
        const response = await userApi.getUsers()
        users.value = response.data
      } catch (error) {
        console.error('获取用户列表失败:', error)
        ElMessage.error('获取用户列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 显示创建用户对话框
    const showCreateUserDialog = () => {
      // 重置表单
      Object.assign(newUser, {
        username: '',
        email: '',
        password: '',
        full_name: '',
        is_active: true,
        is_superuser: false
      })
      createUserDialogVisible.value = true
      // 下一帧重置表单验证
      setTimeout(() => {
        createUserForm.value?.resetFields()
      })
    }
    
    // 创建用户
    const createUser = async () => {
      createUserForm.value?.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            await userApi.createUser(newUser)
            ElMessage.success('创建用户成功')
            createUserDialogVisible.value = false
            fetchUsers() // 刷新用户列表
          } catch (error) {
            console.error('创建用户失败:', error)
            ElMessage.error(error.response?.data?.detail || '创建用户失败')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 显示编辑用户对话框
    const showEditUserDialog = (user) => {
      // 复制用户数据
      Object.assign(editingUser, {
        id: user.id,
        username: user.username,
        email: user.email,
        password: '', // 密码留空
        full_name: user.full_name,
        is_active: user.is_active,
        is_superuser: user.is_superuser
      })
      editUserDialogVisible.value = true
      // 下一帧重置表单验证
      setTimeout(() => {
        editUserForm.value?.resetFields()
      })
    }
    
    // 更新用户
    const updateUser = async () => {
      editUserForm.value?.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 创建更新对象，只包含需要更新的字段
            const updateData = {
              email: editingUser.email,
              full_name: editingUser.full_name,
              is_active: editingUser.is_active,
              is_superuser: editingUser.is_superuser
            }
            
            // 如果密码不为空，则更新密码
            if (editingUser.password) {
              updateData.password = editingUser.password
            }
            
            await userApi.updateUser(editingUser.id, updateData)
            ElMessage.success('更新用户成功')
            editUserDialogVisible.value = false
            fetchUsers() // 刷新用户列表
          } catch (error) {
            console.error('更新用户失败:', error)
            ElMessage.error(error.response?.data?.detail || '更新用户失败')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 确认删除用户
    const confirmDeleteUser = (user) => {
      ElMessageBox.confirm(
        `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        deleteUser(user.id)
      }).catch(() => {
        // 取消删除
      })
    }
    
    // 删除用户
    const deleteUser = async (userId) => {
      loading.value = true
      try {
        await userApi.deleteUser(userId)
        ElMessage.success('删除用户成功')
        fetchUsers() // 刷新用户列表
      } catch (error) {
        console.error('删除用户失败:', error)
        ElMessage.error(error.response?.data?.detail || '删除用户失败')
      } finally {
        loading.value = false
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    }
    
    // 组件挂载时获取用户列表
    onMounted(() => {
      fetchUsers()
    })
    
    return {
      users,
      loading,
      currentUser,
      createUserDialogVisible,
      createUserForm,
      newUser,
      editUserDialogVisible,
      editUserForm,
      editingUser,
      userFormRules,
      editUserFormRules,
      showCreateUserDialog,
      createUser,
      showEditUserDialog,
      updateUser,
      confirmDeleteUser,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-management-container {
  padding: 20px;
}

.user-list-container {
  margin-top: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h2 {
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}
</style>
