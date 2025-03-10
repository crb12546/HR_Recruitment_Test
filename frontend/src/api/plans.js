/**
 * 招聘方案API服务
 * 处理招聘方案相关请求
 */
import apiClient from './index';

const plansApi = {
  /**
   * 获取招聘方案列表
   * @param {Object} params - 查询参数
   * @param {number} params.skip - 跳过的记录数
   * @param {number} params.limit - 返回的记录数
   * @param {number} params.job_id - 职位ID（可选）
   * @returns {Promise} - 返回招聘方案列表
   */
  getPlans: (params = {}) => {
    return apiClient.get('/plans', { params });
  },
  
  /**
   * 获取招聘方案详情
   * @param {number} id - 招聘方案ID
   * @returns {Promise} - 返回招聘方案详情
   */
  getPlan: (id) => {
    return apiClient.get(`/plans/${id}`);
  },
  
  /**
   * 创建招聘方案
   * @param {Object} planData - 招聘方案数据
   * @returns {Promise} - 返回创建结果
   */
  createPlan: (planData) => {
    return apiClient.post('/plans', planData);
  },
  
  /**
   * 更新招聘方案
   * @param {number} id - 招聘方案ID
   * @param {Object} planData - 招聘方案数据
   * @returns {Promise} - 返回更新结果
   */
  updatePlan: (id, planData) => {
    return apiClient.put(`/plans/${id}`, planData);
  },
  
  /**
   * 删除招聘方案
   * @param {number} id - 招聘方案ID
   * @returns {Promise} - 返回删除结果
   */
  deletePlan: (id) => {
    return apiClient.delete(`/plans/${id}`);
  },
  
  /**
   * 自动生成招聘方案
   * @param {Object} params - 生成参数
   * @param {number} params.job_id - 职位ID
   * @param {number} params.min_score - 最低匹配分数
   * @param {string} params.title - 方案标题
   * @returns {Promise} - 返回生成结果
   */
  generatePlan: (params) => {
    return apiClient.post('/plans/generate', params);
  },
  
  /**
   * 导出招聘方案
   * @param {number} id - 招聘方案ID
   * @param {string} format - 导出格式（pdf, docx, xlsx）
   * @returns {Promise} - 返回导出结果
   */
  exportPlan: (id, format = 'pdf') => {
    return apiClient.get(`/plans/${id}/export`, {
      params: { format },
      responseType: 'blob'
    });
  }
};

export default plansApi;
