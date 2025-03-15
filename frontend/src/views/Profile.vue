<template>
  <div class="profile-container">
    <div class="profile-card">
      <h1>个人信息</h1>
      
      <el-form 
        :model="userForm" 
        :rules="rules" 
        ref="userFormRef" 
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="用户名">
          <el-input v-model="userForm.username" disabled />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="userForm.full_name" />
        </el-form-item>
        
        <el-form-item label="新密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="留空表示不修改密码" />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="userForm.confirmPassword" type="password" placeholder="留空表示不修改密码" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="updateProfile" :loading="loading">保存修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import userApi from '../api/user'
import { store } from '../store'

export default {
  name: 'ProfileView',
  setup() {
    const userFormRef = ref(null)
    const loading = ref(false)
    
    // 用户表单数据
    const userForm = reactive({
      username: '',
      email: '',
      full_name: '',
      password: '',
      confirmPassword: ''
    })
    
    // 表单验证规则
    const rules = {
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
      ],
      confirmPassword: [
        { 
          validator: (rule, value, callback) => {
            if (userForm.password && value !== userForm.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          }, 
          trigger: 'blur' 
        }
      ]
    }
    
    // 获取用户信息
    const fetchUserInfo = async () => {
      loading.value = true
      try {
        const response = await userApi.getCurrentUser()
        const userData = response.data
        
        // 更新表单数据
        userForm.username = userData.username
        userForm.email = userData.email
        userForm.full_name = userData.full_name
        
        // 更新存储的用户信息
        store.setUserInfo(userData)
      } catch (error) {
        console.error('获取用户信息失败:', error)
        ElMessage.error('获取用户信息失败')
      } finally {
        loading.value = false
      }
    }
    
    // 更新用户信息
    const updateProfile = async () => {
      userFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 创建更新对象，只包含需要更新的字段
            const updateData = {
              email: userForm.email,
              full_name: userForm.full_name
            }
            
            // 如果密码不为空，则更新密码
            if (userForm.password) {
              updateData.password = userForm.password
            }
            
            await userApi.updateCurrentUser(updateData)
            ElMessage.success('个人信息更新成功')
            
            // 清空密码字段
            userForm.password = ''
            userForm.confirmPassword = ''
            
            // 重新获取用户信息
            fetchUserInfo()
          } catch (error) {
            console.error('更新个人信息失败:', error)
            ElMessage.error(error.response?.data?.detail || '更新个人信息失败')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    // 组件挂载时获取用户信息
    onMounted(() => {
      fetchUserInfo()
    })
    
    return {
      userFormRef,
      userForm,
      rules,
      loading,
      updateProfile
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.profile-card {
  width: 600px;
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 30px;
  text-align: center;
  color: #409EFF;
}

.profile-form {
  margin-top: 20px;
}
</style>
