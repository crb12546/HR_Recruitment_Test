import { reactive } from 'vue'
import apiClient from '../api'

// 创建一个简单的状态存储
export const store = reactive({
  // 状态
  state: {
    // 用户状态
    user: null,
    isLoggedIn: false,
    token: '',
    
    // 招聘需求状态
    jobs: {
      list: [],
      current: null,
      loading: false,
      error: null
    },
    
    // 简历状态
    resumes: {
      list: [],
      current: null,
      loading: false,
      error: null
    },
    
    // 匹配结果状态
    matches: {
      list: [],
      current: null,
      loading: false,
      error: null
    },
    
    // 招聘方案状态
    plans: {
      list: [],
      current: null,
      loading: false,
      error: null
    }
  },
  
  // 方法：设置用户登录状态
  setUserLoggedIn(username, token) {
    this.state.isLoggedIn = true
    this.state.token = token
    localStorage.setItem('token', token)
    
    // 设置API客户端的认证头
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    // 获取用户信息
    this.fetchUserInfo()
  },
  
  // 方法：设置用户信息
  setUserInfo(user) {
    this.state.user = user
  },
  
  // 方法：获取用户信息
  async fetchUserInfo() {
    try {
      const response = await apiClient.get('/auth/me')
      this.setUserInfo(response.data)
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 如果获取用户信息失败，可能是token无效，执行登出
      if (error.response && error.response.status === 401) {
        this.logout()
      }
    }
  },
  
  // 方法：检查是否已认证
  isAuthenticated() {
    // 检查本地存储中是否有token
    const token = localStorage.getItem('token')
    if (token) {
      // 如果有token但状态中没有，更新状态
      if (!this.state.token) {
        this.state.token = token
        this.state.isLoggedIn = true
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        // 获取用户信息
        this.fetchUserInfo()
      }
      return true
    }
    return false
  },
  
  // 方法：用户登出
  logout() {
    this.state.isLoggedIn = false
    this.state.user = null
    this.state.token = ''
    localStorage.removeItem('token')
    
    // 移除API客户端的认证头
    delete apiClient.defaults.headers.common['Authorization']
  },
  
  // 方法：设置招聘需求列表
  setJobs(jobs) {
    this.state.jobs.list = jobs
  },
  
  // 方法：设置当前招聘需求
  setCurrentJob(job) {
    this.state.jobs.current = job
  },
  
  // 方法：设置简历列表
  setResumes(resumes) {
    this.state.resumes.list = resumes
  },
  
  // 方法：设置当前简历
  setCurrentResume(resume) {
    this.state.resumes.current = resume
  },
  
  // 方法：设置匹配结果列表
  setMatches(matches) {
    this.state.matches.list = matches
  },
  
  // 方法：设置当前匹配结果
  setCurrentMatch(match) {
    this.state.matches.current = match
  },
  
  // 方法：设置招聘方案列表
  setPlans(plans) {
    this.state.plans.list = plans
  },
  
  // 方法：设置当前招聘方案
  setCurrentPlan(plan) {
    this.state.plans.current = plan
  }
})
