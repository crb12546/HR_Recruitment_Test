/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  // 招聘需求路由
  {
    path: '/jobs',
    name: 'JobList',
    component: () => import('../views/job/JobList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/jobs/upload',
    name: 'JobUpload',
    component: () => import('../views/job/JobUpload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: () => import('../views/job/JobDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/jobs/analysis',
    name: 'JobAnalysis',
    component: () => import('../views/job/JobAnalysis.vue'),
    meta: { requiresAuth: true }
  },
  // 简历路由
  {
    path: '/resumes',
    name: 'ResumeList',
    component: () => import('../views/resume/ResumeList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/resumes/upload',
    name: 'ResumeUpload',
    component: () => import('../views/resume/ResumeUpload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/resumes/:id',
    name: 'ResumeDetail',
    component: () => import('../views/resume/ResumeDetail.vue'),
    meta: { requiresAuth: true }
  },
  // 匹配路由
  {
    path: '/matches',
    name: 'MatchList',
    component: () => import('../views/match/MatchList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/matches/:id',
    name: 'MatchDetail',
    component: () => import('../views/match/MatchDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/plans/generate',
    name: 'PlanGeneration',
    component: () => import('../views/match/PlanGeneration.vue'),
    meta: { requiresAuth: true }
  },
  // 数据分析路由
  {
    path: '/analytics',
    name: 'AnalyticsDashboard',
    component: () => import('../views/analytics/AnalyticsDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analytics/funnel',
    name: 'RecruitmentFunnel',
    component: () => import('../views/analytics/RecruitmentFunnel.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analytics/channels',
    name: 'ChannelAnalysis',
    component: () => import('../views/analytics/ChannelAnalysis.vue'),
    meta: { requiresAuth: true }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.meta.requiresAuth) {
    // 检查用户是否已登录
    const token = localStorage.getItem('token')
    if (!token) {
      // 未登录，重定向到登录页
      next({ name: 'Login' })
    } else {
      // 已登录，允许访问
      next()
    }
  } else {
    // 不需要认证的路由，直接访问
    next()
  }
})

export default router
