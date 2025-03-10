/**
 * 认证API服务
 * 处理用户登录、注册等认证相关请求
 */
import apiClient from './index';

const authApi = {
  /**
   * 用户登录
   * @param {Object} credentials - 登录凭证
   * @param {string} credentials.username - 用户名
   * @param {string} credentials.password - 密码
   * @returns {Promise} - 返回登录结果
   */
  login: (credentials) => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    return apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  
  /**
   * 用户注册
   * @param {Object} userData - 用户数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.email - 邮箱
   * @param {string} userData.password - 密码
   * @param {string} userData.full_name - 姓名
   * @returns {Promise} - 返回注册结果
   */
  register: (userData) => {
    return apiClient.post('/auth/register', userData);
  },
  
  /**
   * 检查当前用户是否已登录
   * @returns {boolean} - 是否已登录
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
  
  /**
   * 退出登录
   */
  logout: () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }
};

export default authApi;
