<template>
  <div class="candidate-progress-chart">
    <div class="chart-header">
      <h3>候选人进展分析</h3>
      <div class="chart-actions">
        <el-select v-model="timeRange" placeholder="时间范围" size="small" @change="fetchData">
          <el-option label="最近7天" value="7days" />
          <el-option label="最近30天" value="30days" />
          <el-option label="最近90天" value="90days" />
          <el-option label="今年" value="thisYear" />
          <el-option label="全部" value="all" />
        </el-select>
        
        <el-select v-model="jobId" placeholder="职位筛选" size="small" clearable @change="fetchData">
          <el-option
            v-for="job in jobOptions"
            :key="job.value"
            :label="job.label"
            :value="job.value"
          />
        </el-select>
        
        <el-select v-model="chartType" placeholder="图表类型" size="small" @change="updateChart">
          <el-option label="状态分布" value="status" />
          <el-option label="时间趋势" value="trend" />
        </el-select>
      </div>
    </div>
    
    <div v-loading="loading" class="chart-container">
      <div ref="chartRef" class="echarts-container"></div>
    </div>
    
    <div class="chart-footer">
      <div class="progress-stats">
        <el-row :gutter="20">
          <el-col :span="8" v-for="(stat, index) in progressStats" :key="index">
            <div class="stat-card">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-trend" :class="{ 'up': stat.trend > 0, 'down': stat.trend < 0 }">
                <el-icon v-if="stat.trend > 0"><ArrowUp /></el-icon>
                <el-icon v-else-if="stat.trend < 0"><ArrowDown /></el-icon>
                <span>{{ Math.abs(stat.trend) }}%</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <div class="candidate-table">
        <h4>候选人状态明细</h4>
        <el-table :data="candidateData" style="width: 100%" height="250">
          <el-table-column prop="name" label="候选人" width="120" />
          <el-table-column prop="job" label="应聘职位" width="150" />
          <el-table-column prop="status" label="当前状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="days_in_process" label="流程天数" width="100" />
          <el-table-column prop="next_step" label="下一步" />
          <el-table-column prop="updated_at" label="更新时间" width="120">
            <template #default="scope">
              {{ formatDate(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';

export default {
  name: 'CandidateProgressChart',
  props: {
    initialJobId: {
      type: [Number, String],
      default: null
    },
    initialTimeRange: {
      type: String,
      default: '30days'
    }
  },
  setup(props) {
    // 图表引用
    const chartRef = ref(null);
    let chart = null;
    
    // 加载状态
    const loading = ref(false);
    
    // 时间范围
    const timeRange = ref(props.initialTimeRange);
    
    // 职位ID
    const jobId = ref(props.initialJobId);
    
    // 图表类型
    const chartType = ref('status');
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 候选人数据
    const candidateData = ref([]);
    
    // 进展统计
    const progressStats = ref([]);
    
    // 状态数据
    const statusData = ref({});
    
    // 趋势数据
    const trendData = ref({});
    
    // 初始化图表
    const initChart = () => {
      if (!chartRef.value) return;
      
      // 创建图表实例
      chart = echarts.init(chartRef.value);
      
      // 设置响应式
      window.addEventListener('resize', handleResize);
      
      // 获取数据
      fetchData();
    };
    
    // 处理窗口大小变化
    const handleResize = () => {
      if (chart) {
        chart.resize();
      }
    };
    
    // 获取数据
    const fetchData = async () => {
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          time_range: timeRange.value,
          job_id: jobId.value || undefined
        };
        
        // 调用API获取候选人进展数据
        // const response = await api.getCandidateProgressData(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            candidates: [
              {
                name: '张三',
                job: '后端开发工程师',
                status: '简历筛选',
                days_in_process: 2,
                next_step: '安排初试',
                updated_at: '2025-03-08T10:00:00Z'
              },
              {
                name: '李四',
                job: '前端开发工程师',
                status: '初试',
                days_in_process: 5,
                next_step: '安排复试',
                updated_at: '2025-03-07T10:00:00Z'
              },
              {
                name: '王五',
                job: '产品经理',
                status: '复试',
                days_in_process: 8,
                next_step: '安排终试',
                updated_at: '2025-03-06T10:00:00Z'
              },
              {
                name: '赵六',
                job: '后端开发工程师',
                status: '终试',
                days_in_process: 12,
                next_step: '发放offer',
                updated_at: '2025-03-05T10:00:00Z'
              },
              {
                name: '钱七',
                job: '前端开发工程师',
                status: 'Offer',
                days_in_process: 15,
                next_step: '等待入职',
                updated_at: '2025-03-04T10:00:00Z'
              },
              {
                name: '孙八',
                job: '产品经理',
                status: '已入职',
                days_in_process: 25,
                next_step: '完成入职',
                updated_at: '2025-03-03T10:00:00Z'
              },
              {
                name: '周九',
                job: '后端开发工程师',
                status: '已淘汰',
                days_in_process: 7,
                next_step: '流程结束',
                updated_at: '2025-03-02T10:00:00Z'
              }
            ],
            stats: [
              {
                title: '在招人数',
                value: 35,
                trend: 12.5
              },
              {
                title: '平均招聘周期',
                value: '18天',
                trend: -5.2
              },
              {
                title: 'Offer接受率',
                value: '85%',
                trend: 3.8
              }
            ],
            status_data: {
              categories: ['简历筛选', '初试', '复试', '终试', 'Offer', '已入职', '已淘汰'],
              values: [120, 80, 40, 20, 15, 10, 30]
            },
            trend_data: {
              dates: ['03-01', '03-02', '03-03', '03-04', '03-05', '03-06', '03-07', '03-08', '03-09', '03-10'],
              series: [
                {
                  name: '简历筛选',
                  data: [30, 32, 35, 38, 40, 42, 45, 48, 50, 52]
                },
                {
                  name: '初试',
                  data: [20, 22, 23, 25, 26, 28, 30, 32, 33, 35]
                },
                {
                  name: '复试',
                  data: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
                },
                {
                  name: '终试',
                  data: [5, 6, 6, 7, 7, 8, 8, 9, 9, 10]
                },
                {
                  name: 'Offer',
                  data: [3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
                },
                {
                  name: '已入职',
                  data: [2, 2, 3, 3, 3, 4, 4, 4, 5, 5]
                }
              ]
            }
          }
        };
        
        // 设置候选人数据
        candidateData.value = response.data.candidates;
        
        // 设置进展统计
        progressStats.value = response.data.stats;
        
        // 设置状态数据
        statusData.value = response.data.status_data;
        
        // 设置趋势数据
        trendData.value = response.data.trend_data;
        
        // 更新图表
        updateChart();
      } catch (error) {
        console.error('获取候选人进展数据失败:', error);
        ElMessage.error('获取候选人进展数据失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 更新图表
    const updateChart = () => {
      if (!chart) return;
      
      if (chartType.value === 'status') {
        renderStatusChart();
      } else {
        renderTrendChart();
      }
    };
    
    // 渲染状态分布图表
    const renderStatusChart = () => {
      if (!statusData.value || !statusData.value.categories) return;
      
      const option = {
        title: {
          text: '候选人状态分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: statusData.value.categories
        },
        series: [
          {
            name: '候选人数量',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: statusData.value.categories.map((category, index) => ({
              value: statusData.value.values[index],
              name: category
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      
      chart.setOption(option);
    };
    
    // 渲染时间趋势图表
    const renderTrendChart = () => {
      if (!trendData.value || !trendData.value.dates) return;
      
      const option = {
        title: {
          text: '候选人状态趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: trendData.value.series.map(item => item.name),
          bottom: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: trendData.value.dates
        },
        yAxis: {
          type: 'value'
        },
        series: trendData.value.series.map(item => ({
          name: item.name,
          type: 'line',
          data: item.data
        }))
      };
      
      chart.setOption(option);
    };
    
    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        '简历筛选': 'info',
        '初试': 'primary',
        '复试': 'primary',
        '终试': 'warning',
        'Offer': 'success',
        '已入职': 'success',
        '已淘汰': 'danger'
      };
      
      return statusMap[status] || 'info';
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    };
    
    // 监听时间范围变化
    watch(timeRange, () => {
      fetchData();
    });
    
    // 监听职位ID变化
    watch(jobId, () => {
      fetchData();
    });
    
    // 监听图表类型变化
    watch(chartType, () => {
      updateChart();
    });
    
    // 组件挂载时初始化图表
    onMounted(() => {
      initChart();
    });
    
    // 组件卸载时销毁图表
    onUnmounted(() => {
      if (chart) {
        chart.dispose();
        chart = null;
      }
      
      window.removeEventListener('resize', handleResize);
    });
    
    return {
      chartRef,
      loading,
      timeRange,
      jobId,
      chartType,
      jobOptions,
      candidateData,
      progressStats,
      fetchData,
      updateChart,
      getStatusType,
      formatDate
    };
  }
};
</script>

<style scoped>
.candidate-progress-chart {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.chart-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.chart-actions {
  display: flex;
  gap: 10px;
}

.chart-container {
  flex: 1;
  position: relative;
  min-height: 300px;
}

.echarts-container {
  width: 100%;
  height: 100%;
}

.chart-footer {
  margin-top: 15px;
}

.progress-stats {
  margin-bottom: 20px;
}

.stat-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
  height: 100%;
}

.stat-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.stat-trend.up {
  color: #67C23A;
}

.stat-trend.down {
  color: #F56C6C;
}

.candidate-table h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
}
</style>
