/**
 * 招聘需求API服务
 * 处理招聘需求相关请求
 */
import apiClient from './index';

const jobsApi = {
  /**
   * 获取招聘需求列表
   * @param {Object} params - 查询参数
   * @param {number} params.skip - 跳过的记录数
   * @param {number} params.limit - 返回的记录数
   * @param {string} params.position_name - 职位名称（可选）
   * @param {string} params.department - 部门（可选）
   * @returns {Promise} - 返回招聘需求列表
   */
  getJobs: (params = {}) => {
    return apiClient.get('/jobs', { params });
  },
  
  /**
   * 获取招聘需求详情
   * @param {number} id - 招聘需求ID
   * @returns {Promise} - 返回招聘需求详情
   */
  getJob: (id) => {
    return apiClient.get(`/jobs/${id}`);
  },
  
  /**
   * 创建招聘需求
   * @param {Object} jobData - 招聘需求数据
   * @returns {Promise} - 返回创建结果
   */
  createJob: (jobData) => {
    return apiClient.post('/jobs', jobData);
  },
  
  /**
   * 更新招聘需求
   * @param {number} id - 招聘需求ID
   * @param {Object} jobData - 招聘需求数据
   * @returns {Promise} - 返回更新结果
   */
  updateJob: (id, jobData) => {
    return apiClient.put(`/jobs/${id}`, jobData);
  },
  
  /**
   * 删除招聘需求
   * @param {number} id - 招聘需求ID
   * @returns {Promise} - 返回删除结果
   */
  deleteJob: (id) => {
    return apiClient.delete(`/jobs/${id}`);
  },
  
  /**
   * 上传招聘需求文档
   * @param {File} file - 招聘需求文档
   * @param {Object} data - 附加数据
   * @param {string} data.position_name - 职位名称
   * @param {string} data.department - 部门（可选）
   * @returns {Promise} - 返回上传结果
   */
  uploadJobDocument: (file, data) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('position_name', data.position_name);
    
    if (data.department) {
      formData.append('department', data.department);
    }
    
    return apiClient.post('/jobs/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  }
};

export default jobsApi;
