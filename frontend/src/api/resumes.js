/**
 * 简历API服务
 * 处理简历相关请求
 */
import apiClient from './index';

const resumesApi = {
  /**
   * 获取简历列表
   * @param {Object} params - 查询参数
   * @param {number} params.skip - 跳过的记录数
   * @param {number} params.limit - 返回的记录数
   * @param {string} params.candidate_name - 候选人姓名（可选）
   * @param {string} params.tag - 标签（可选）
   * @returns {Promise} - 返回简历列表
   */
  getResumes: (params = {}) => {
    return apiClient.get('/resumes', { params });
  },
  
  /**
   * 获取简历详情
   * @param {number} id - 简历ID
   * @returns {Promise} - 返回简历详情
   */
  getResume: (id) => {
    return apiClient.get(`/resumes/${id}`);
  },
  
  /**
   * 创建简历
   * @param {Object} resumeData - 简历数据
   * @returns {Promise} - 返回创建结果
   */
  createResume: (resumeData) => {
    return apiClient.post('/resumes', resumeData);
  },
  
  /**
   * 更新简历
   * @param {number} id - 简历ID
   * @param {Object} resumeData - 简历数据
   * @returns {Promise} - 返回更新结果
   */
  updateResume: (id, resumeData) => {
    return apiClient.put(`/resumes/${id}`, resumeData);
  },
  
  /**
   * 删除简历
   * @param {number} id - 简历ID
   * @returns {Promise} - 返回删除结果
   */
  deleteResume: (id) => {
    return apiClient.delete(`/resumes/${id}`);
  },
  
  /**
   * 上传简历文档
   * @param {File} file - 简历文档
   * @param {Object} data - 附加数据
   * @param {string} data.candidate_name - 候选人姓名（可选）
   * @returns {Promise} - 返回上传结果
   */
  uploadResumeDocument: (file, data = {}) => {
    const formData = new FormData();
    formData.append('file', file);
    
    if (data.candidate_name) {
      formData.append('candidate_name', data.candidate_name);
    }
    
    return apiClient.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  /**
   * 批量上传简历
   * @param {Array<File>} files - 简历文档数组
   * @returns {Promise} - 返回上传结果
   */
  batchUploadResumes: (files) => {
    const formData = new FormData();
    
    files.forEach((file, index) => {
      formData.append(`files`, file);
    });
    
    return apiClient.post('/resumes/batch-upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  /**
   * 搜索简历
   * @param {Object} params - 搜索参数
   * @param {string} params.keyword - 关键词
   * @param {Array<string>} params.tags - 标签数组
   * @param {string} params.education - 学历
   * @param {number} params.min_experience - 最小工作经验（年）
   * @returns {Promise} - 返回搜索结果
   */
  searchResumes: (params) => {
    return apiClient.get('/resumes/search', { params });
  }
};

export default resumesApi;
