/**
 * 招聘需求API
 */
import apiClient from './index'

/**
 * 获取招聘需求列表
 * @param {Object} params 查询参数
 * @returns {Promise} 响应Promise
 */
export const getJobRequirements = (params = {}) => {
  return apiClient.get('/jobs', { params })
    .then(response => response.data)
}

/**
 * 获取招聘需求详情
 * @param {Number} id 招聘需求ID
 * @returns {Promise} 响应Promise
 */
export const getJobRequirement = (id) => {
  return apiClient.get(`/jobs/${id}`)
    .then(response => response.data)
}

/**
 * 创建招聘需求
 * @param {Object} data 招聘需求数据
 * @returns {Promise} 响应Promise
 */
export const createJobRequirement = (data) => {
  return apiClient.post('/jobs', data)
    .then(response => response.data)
}

/**
 * 更新招聘需求
 * @param {Number} id 招聘需求ID
 * @param {Object} data 更新数据
 * @returns {Promise} 响应Promise
 */
export const updateJobRequirement = (id, data) => {
  return apiClient.put(`/jobs/${id}`, data)
    .then(response => response.data)
}

/**
 * 删除招聘需求
 * @param {Number} id 招聘需求ID
 * @returns {Promise} 响应Promise
 */
export const deleteJobRequirement = (id) => {
  return apiClient.delete(`/jobs/${id}`)
}

/**
 * 解析招聘需求文档（不保存）
 * @param {FormData} formData 包含文件的表单数据
 * @returns {Promise} 响应Promise
 */
export const parseJobRequirementDocument = (formData) => {
  return apiClient.post('/jobs/parse', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => response.data)
}

/**
 * 上传并解析招聘需求文档
 * @param {FormData} formData 包含文件和其他字段的表单数据
 * @returns {Promise} 响应Promise
 */
export const uploadJobRequirementDocument = (formData) => {
  return apiClient.post('/jobs/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then(response => response.data)
}

export default {
  getJobRequirements,
  getJobRequirement,
  createJobRequirement,
  updateJobRequirement,
  deleteJobRequirement,
  parseJobRequirementDocument,
  uploadJobRequirementDocument
}
