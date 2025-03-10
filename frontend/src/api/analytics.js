/**
 * 数据分析API服务
 * 处理招聘数据分析相关请求
 * 注意：目前后端尚未实现数据分析API，此处为模拟实现
 */
import apiClient from './index';

// 模拟数据
const mockData = {
  // 招聘漏斗数据
  funnelData: {
    '7days': [
      { stage: '简历投递', count: 120, percentage: 100, conversion_rate: '-', avg_time: '0天' },
      { stage: '简历筛选', count: 80, percentage: 66.7, conversion_rate: '66.7', avg_time: '2天' },
      { stage: '初试', count: 40, percentage: 33.3, conversion_rate: '50.0', avg_time: '5天' },
      { stage: '复试', count: 20, percentage: 16.7, conversion_rate: '50.0', avg_time: '3天' },
      { stage: '终试', count: 10, percentage: 8.3, conversion_rate: '50.0', avg_time: '2天' },
      { stage: '录用', count: 8, percentage: 6.7, conversion_rate: '80.0', avg_time: '3天' },
      { stage: '入职', count: 6, percentage: 5.0, conversion_rate: '75.0', avg_time: '14天' }
    ],
    '30days': [
      { stage: '简历投递', count: 1200, percentage: 100, conversion_rate: '-', avg_time: '0天' },
      { stage: '简历筛选', count: 800, percentage: 66.7, conversion_rate: '66.7', avg_time: '2天' },
      { stage: '初试', count: 400, percentage: 33.3, conversion_rate: '50.0', avg_time: '5天' },
      { stage: '复试', count: 200, percentage: 16.7, conversion_rate: '50.0', avg_time: '3天' },
      { stage: '终试', count: 100, percentage: 8.3, conversion_rate: '50.0', avg_time: '2天' },
      { stage: '录用', count: 80, percentage: 6.7, conversion_rate: '80.0', avg_time: '3天' },
      { stage: '入职', count: 60, percentage: 5.0, conversion_rate: '75.0', avg_time: '14天' }
    ]
  },
  
  // 渠道效果数据
  channelData: {
    '7days': [
      { channel: '智联招聘', count: 50, percentage: 41.7, conversion_rate: 10.0, cost_per_hire: 2000 },
      { channel: '前程无忧', count: 30, percentage: 25.0, conversion_rate: 6.7, cost_per_hire: 3000 },
      { channel: '拉勾网', count: 20, percentage: 16.7, conversion_rate: 15.0, cost_per_hire: 1500 },
      { channel: '内部推荐', count: 15, percentage: 12.5, conversion_rate: 20.0, cost_per_hire: 1000 },
      { channel: '校园招聘', count: 5, percentage: 4.2, conversion_rate: 0.0, cost_per_hire: 0 }
    ],
    '30days': [
      { channel: '智联招聘', count: 500, percentage: 41.7, conversion_rate: 10.0, cost_per_hire: 2000 },
      { channel: '前程无忧', count: 300, percentage: 25.0, conversion_rate: 6.7, cost_per_hire: 3000 },
      { channel: '拉勾网', count: 200, percentage: 16.7, conversion_rate: 15.0, cost_per_hire: 1500 },
      { channel: '内部推荐', count: 150, percentage: 12.5, conversion_rate: 20.0, cost_per_hire: 1000 },
      { channel: '校园招聘', count: 50, percentage: 4.2, conversion_rate: 0.0, cost_per_hire: 0 }
    ]
  },
  
  // 候选人进展数据
  candidateProgressData: {
    '7days': {
      labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      series: [
        { name: '简历投递', data: [20, 15, 25, 30, 10, 10, 10] },
        { name: '初试', data: [10, 8, 12, 15, 5, 0, 0] },
        { name: '复试', data: [5, 4, 6, 8, 2, 0, 0] },
        { name: '录用', data: [2, 1, 3, 4, 0, 0, 0] }
      ]
    },
    '30days': {
      labels: ['第1周', '第2周', '第3周', '第4周'],
      series: [
        { name: '简历投递', data: [300, 350, 250, 300] },
        { name: '初试', data: [150, 175, 125, 150] },
        { name: '复试', data: [75, 88, 62, 75] },
        { name: '录用', data: [20, 25, 15, 20] }
      ]
    }
  },
  
  // 汇总统计
  summaryStats: {
    '7days': [
      { title: '简历总数', value: '120', trend: 12.5, icon: 'Document', type: 'primary' },
      { title: '面试人数', value: '40', trend: 8.3, icon: 'User', type: 'success' },
      { title: '平均招聘周期', value: '18天', trend: -5.2, icon: 'Timer', type: 'warning' },
      { title: 'Offer接受率', value: '85%', trend: 3.8, icon: 'Check', type: 'info' }
    ],
    '30days': [
      { title: '简历总数', value: '1,256', trend: 12.5, icon: 'Document', type: 'primary' },
      { title: '面试人数', value: '328', trend: 8.3, icon: 'User', type: 'success' },
      { title: '平均招聘周期', value: '18天', trend: -5.2, icon: 'Timer', type: 'warning' },
      { title: 'Offer接受率', value: '85%', trend: 3.8, icon: 'Check', type: 'info' }
    ]
  }
};

const analyticsApi = {
  /**
   * 获取招聘漏斗数据
   * @param {Object} params - 查询参数
   * @param {string} params.time_range - 时间范围（7days, 30days, 90days, thisYear, all）
   * @param {number} params.job_id - 职位ID（可选）
   * @returns {Promise} - 返回招聘漏斗数据
   */
  getFunnelData: (params = {}) => {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        const timeRange = params.time_range || '30days';
        const data = mockData.funnelData[timeRange] || mockData.funnelData['30days'];
        
        resolve({
          data: {
            data
          }
        });
      }, 500);
    });
  },
  
  /**
   * 获取渠道效果数据
   * @param {Object} params - 查询参数
   * @param {string} params.time_range - 时间范围（7days, 30days, 90days, thisYear, all）
   * @param {number} params.job_id - 职位ID（可选）
   * @returns {Promise} - 返回渠道效果数据
   */
  getChannelData: (params = {}) => {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        const timeRange = params.time_range || '30days';
        const data = mockData.channelData[timeRange] || mockData.channelData['30days'];
        
        resolve({
          data: {
            data
          }
        });
      }, 500);
    });
  },
  
  /**
   * 获取候选人进展数据
   * @param {Object} params - 查询参数
   * @param {string} params.time_range - 时间范围（7days, 30days, 90days, thisYear, all）
   * @param {number} params.job_id - 职位ID（可选）
   * @returns {Promise} - 返回候选人进展数据
   */
  getCandidateProgressData: (params = {}) => {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        const timeRange = params.time_range || '30days';
        const data = mockData.candidateProgressData[timeRange] || mockData.candidateProgressData['30days'];
        
        resolve({
          data: {
            data
          }
        });
      }, 500);
    });
  },
  
  /**
   * 获取汇总统计数据
   * @param {Object} params - 查询参数
   * @param {string} params.time_range - 时间范围（7days, 30days, 90days, thisYear, all）
   * @param {number} params.job_id - 职位ID（可选）
   * @returns {Promise} - 返回汇总统计数据
   */
  getSummaryStats: (params = {}) => {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        const timeRange = params.time_range || '30days';
        const data = mockData.summaryStats[timeRange] || mockData.summaryStats['30days'];
        
        resolve({
          data: {
            data
          }
        });
      }, 500);
    });
  },
  
  /**
   * 导出分析报告
   * @param {Object} params - 导出参数
   * @param {string} params.time_range - 时间范围
   * @param {number} params.job_id - 职位ID（可选）
   * @param {string} params.format - 导出格式（pdf, xlsx, docx）
   * @returns {Promise} - 返回导出结果
   */
  exportReport: (params) => {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: {
            url: 'https://example.com/reports/sample-report.pdf',
            filename: 'recruitment-analytics-report.pdf'
          }
        });
      }, 1000);
    });
  }
};

export default analyticsApi;
