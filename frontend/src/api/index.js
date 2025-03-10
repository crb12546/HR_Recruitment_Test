/**
 * API服务主模块
 * 配置Axios实例和请求拦截器
 */
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建axios实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 处理错误响应
    const { response } = error;
    
    if (response) {
      // 服务器返回错误
      const { status, data } = response;
      
      switch (status) {
        case 400:
          ElMessage.error(data.detail || '请求参数错误');
          break;
        case 401:
          ElMessage.error('未授权，请重新登录');
          // 清除token并跳转到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          ElMessage.error('没有权限访问该资源');
          break;
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
        case 500:
          ElMessage.error('服务器错误，请稍后再试');
          break;
        default:
          ElMessage.error(`请求失败: ${data.detail || '未知错误'}`);
      }
    } else {
      // 网络错误或请求被取消
      ElMessage.error('网络错误，请检查您的网络连接');
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
