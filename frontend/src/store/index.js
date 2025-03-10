import { reactive } from 'vue'

// 创建一个简单的状态存储
export const store = reactive({
  // 用户状态
  user: {
    isLoggedIn: false,
    username: '',
    token: ''
  },
  
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
  },
  
  // 方法：设置用户登录状态
  setUserLoggedIn(username, token) {
    this.user.isLoggedIn = true
    this.user.username = username
    this.user.token = token
    localStorage.setItem('token', token)
  },
  
  // 方法：用户登出
  logout() {
    this.user.isLoggedIn = false
    this.user.username = ''
    this.user.token = ''
    localStorage.removeItem('token')
  },
  
  // 方法：设置招聘需求列表
  setJobs(jobs) {
    this.jobs.list = jobs
  },
  
  // 方法：设置当前招聘需求
  setCurrentJob(job) {
    this.jobs.current = job
  },
  
  // 方法：设置简历列表
  setResumes(resumes) {
    this.resumes.list = resumes
  },
  
  // 方法：设置当前简历
  setCurrentResume(resume) {
    this.resumes.current = resume
  },
  
  // 方法：设置匹配结果列表
  setMatches(matches) {
    this.matches.list = matches
  },
  
  // 方法：设置当前匹配结果
  setCurrentMatch(match) {
    this.matches.current = match
  },
  
  // 方法：设置招聘方案列表
  setPlans(plans) {
    this.plans.list = plans
  },
  
  // 方法：设置当前招聘方案
  setCurrentPlan(plan) {
    this.plans.current = plan
  }
})
