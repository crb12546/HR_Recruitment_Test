/**
 * 用户API服务
 * 处理用户管理相关请求
 */
import apiClient from './index';

const userApi = {
  /**
   * 获取当前用户信息
   * @returns {Promise} - 返回当前用户信息
   */
  getCurrentUser: () => {
    return apiClient.get('/auth/me');
  },
  
  /**
   * 更新当前用户信息
   * @param {Object} userData - 用户数据
   * @returns {Promise} - 返回更新结果
   */
  updateCurrentUser: (userData) => {
    return apiClient.put('/auth/me', userData);
  },
  
  /**
   * 获取所有用户列表（仅管理员）
   * @returns {Promise} - 返回用户列表
   */
  getUsers: () => {
    return apiClient.get('/auth/users');
  },
  
  /**
   * 创建新用户（仅管理员）
   * @param {Object} userData - 用户数据
   * @returns {Promise} - 返回创建结果
   */
  createUser: (userData) => {
    return apiClient.post('/auth/users', userData);
  },
  
  /**
   * 获取指定用户信息（仅管理员）
   * @param {number} userId - 用户ID
   * @returns {Promise} - 返回用户信息
   */
  getUser: (userId) => {
    return apiClient.get(`/auth/users/${userId}`);
  },
  
  /**
   * 更新指定用户信息（仅管理员）
   * @param {number} userId - 用户ID
   * @param {Object} userData - 用户数据
   * @returns {Promise} - 返回更新结果
   */
  updateUser: (userId, userData) => {
    return apiClient.put(`/auth/users/${userId}`, userData);
  },
  
  /**
   * 删除指定用户（仅管理员）
   * @param {number} userId - 用户ID
   * @returns {Promise} - 返回删除结果
   */
  deleteUser: (userId) => {
    return apiClient.delete(`/auth/users/${userId}`);
  }
};

export default userApi;
