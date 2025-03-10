/**
 * 匹配API服务
 * 处理简历与职位匹配相关请求
 */
import apiClient from './index';

const matchesApi = {
  /**
   * 获取匹配列表
   * @param {Object} params - 查询参数
   * @param {number} params.skip - 跳过的记录数
   * @param {number} params.limit - 返回的记录数
   * @param {number} params.resume_id - 简历ID（可选）
   * @param {number} params.job_id - 职位ID（可选）
   * @param {number} params.min_score - 最低匹配分数（可选）
   * @returns {Promise} - 返回匹配列表
   */
  getMatches: (params = {}) => {
    return apiClient.get('/matches', { params });
  },
  
  /**
   * 创建匹配
   * @param {Object} matchData - 匹配数据
   * @param {number} matchData.resume_id - 简历ID
   * @param {number} matchData.job_id - 职位ID
   * @returns {Promise} - 返回创建结果
   */
  createMatch: (matchData) => {
    return apiClient.post('/matches', matchData);
  },
  
  /**
   * 批量创建匹配
   * @param {number} jobId - 职位ID
   * @param {Array<number>} resumeIds - 简历ID数组
   * @returns {Promise} - 返回批量创建结果
   */
  batchCreateMatches: (jobId, resumeIds) => {
    return apiClient.post('/matches/batch', {
      job_id: jobId,
      resume_ids: resumeIds
    });
  },
  
  /**
   * 获取职位的最佳匹配简历
   * @param {number} jobId - 职位ID
   * @param {number} limit - 返回的记录数
   * @returns {Promise} - 返回最佳匹配简历列表
   */
  getBestMatchesForJob: (jobId, limit = 10) => {
    return apiClient.get(`/matches/best-for-job/${jobId}`, {
      params: { limit }
    });
  },
  
  /**
   * 获取简历的最佳匹配职位
   * @param {number} resumeId - 简历ID
   * @param {number} limit - 返回的记录数
   * @returns {Promise} - 返回最佳匹配职位列表
   */
  getBestMatchesForResume: (resumeId, limit = 10) => {
    return apiClient.get(`/matches/best-for-resume/${resumeId}`, {
      params: { limit }
    });
  }
};

export default matchesApi;
