<template>
  <div class="analytics-dashboard">
    <div class="page-header">
      <h2>数据分析仪表盘</h2>
      <div class="header-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
        <el-button @click="showExporter = true">
          <el-icon><Download /></el-icon>
          导出报告
        </el-button>
      </div>
    </div>
    
    <div class="filter-bar">
      <el-select v-model="timeRange" placeholder="时间范围" @change="handleFilterChange">
        <el-option label="最近7天" value="7days" />
        <el-option label="最近30天" value="30days" />
        <el-option label="最近90天" value="90days" />
        <el-option label="今年" value="thisYear" />
        <el-option label="全部" value="all" />
      </el-select>
      
      <el-select v-model="jobId" placeholder="职位筛选" clearable @change="handleFilterChange">
        <el-option
          v-for="job in jobOptions"
          :key="job.value"
          :label="job.label"
          :value="job.value"
        />
      </el-select>
    </div>
    
    <div class="dashboard-summary">
      <el-row :gutter="20">
        <el-col :span="6" v-for="(stat, index) in summaryStats" :key="index">
          <div class="stat-card">
            <div class="stat-icon" :class="stat.type">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-trend" :class="{ 'up': stat.trend > 0, 'down': stat.trend < 0 }">
                <el-icon v-if="stat.trend > 0"><ArrowUp /></el-icon>
                <el-icon v-else-if="stat.trend < 0"><ArrowDown /></el-icon>
                <span>{{ Math.abs(stat.trend) }}%</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
    
    <div class="dashboard-charts">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="chart-card">
            <recruitment-funnel-chart
              :initial-job-id="jobId"
              :initial-time-range="timeRange"
            />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="chart-card">
            <channel-effectiveness-chart
              :initial-job-id="jobId"
              :initial-time-range="timeRange"
            />
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <div class="chart-card">
            <candidate-progress-chart
              :initial-job-id="jobId"
              :initial-time-range="timeRange"
            />
          </div>
        </el-col>
      </el-row>
    </div>
    
    <!-- 数据导出对话框 -->
    <el-dialog
      v-model="showExporter"
      title="导出数据分析报告"
      width="80%"
    >
      <data-exporter />
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import RecruitmentFunnelChart from '@/components/analytics/RecruitmentFunnelChart.vue';
import ChannelEffectivenessChart from '@/components/analytics/ChannelEffectivenessChart.vue';
import CandidateProgressChart from '@/components/analytics/CandidateProgressChart.vue';
import DataExporter from '@/components/analytics/DataExporter.vue';
import analyticsApi from '@/api/analytics';

export default {
  name: 'AnalyticsDashboard',
  components: {
    RecruitmentFunnelChart,
    ChannelEffectivenessChart,
    CandidateProgressChart,
    DataExporter
  },
  setup() {
    // 时间范围
    const timeRange = ref('30days');
    
    // 职位ID
    const jobId = ref(null);
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 汇总统计
    const summaryStats = ref([]);
    
    // 是否显示导出器
    const showExporter = ref(false);
    
    // 获取汇总统计
    const fetchSummaryStats = async () => {
      try {
        // 构建查询参数
        const params = {
          time_range: timeRange.value,
          job_id: jobId.value || undefined
        };
        
        // 调用API获取汇总统计
        const response = await analyticsApi.getSummaryStats(params);
        
        // 设置汇总统计
        summaryStats.value = response.data.data;
      } catch (error) {
        console.error('获取汇总统计失败:', error);
        ElMessage.error('获取汇总统计失败，请重试');
      }
    };
    
    // 处理筛选变更
    const handleFilterChange = () => {
      fetchSummaryStats();
    };
    
    // 刷新数据
    const refreshData = () => {
      fetchSummaryStats();
      ElMessage.success('数据已刷新');
    };
    
    // 组件挂载时获取汇总统计
    onMounted(() => {
      fetchSummaryStats();
    });
    
    return {
      timeRange,
      jobId,
      jobOptions,
      summaryStats,
      showExporter,
      handleFilterChange,
      refreshData
    };
  }
};
</script>

<style scoped>
.analytics-dashboard {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.dashboard-summary {
  margin-bottom: 20px;
}

.stat-card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  font-size: 24px;
  color: #fff;
}

.stat-icon.primary {
  background-color: #409EFF;
}

.stat-icon.success {
  background-color: #67C23A;
}

.stat-icon.warning {
  background-color: #E6A23C;
}

.stat-icon.info {
  background-color: #909399;
}

.stat-content {
  flex: 1;
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

.dashboard-charts {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart-card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
}
</style>
