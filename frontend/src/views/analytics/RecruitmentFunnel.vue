<template>
  <div class="recruitment-funnel-page">
    <div class="page-header">
      <h2>招聘漏斗分析</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          返回仪表盘
        </el-button>
        <el-button type="primary" @click="exportData">
          <el-icon><Download /></el-icon>
          导出数据
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
    
    <div class="content-container">
      <div class="chart-container">
        <recruitment-funnel-chart
          :initial-job-id="jobId"
          :initial-time-range="timeRange"
          ref="funnelChartRef"
        />
      </div>
      
      <div class="detail-container">
        <h3>漏斗详情分析</h3>
        
        <div class="funnel-stats">
          <el-table :data="funnelData" style="width: 100%">
            <el-table-column prop="stage" label="招聘阶段" width="150" />
            <el-table-column prop="count" label="候选人数量" width="120" />
            <el-table-column prop="percentage" label="占比" width="120">
              <template #default="scope">
                {{ scope.row.percentage }}%
              </template>
            </el-table-column>
            <el-table-column prop="conversion_rate" label="转化率" width="120">
              <template #default="scope">
                {{ scope.row.conversion_rate }}%
              </template>
            </el-table-column>
            <el-table-column prop="avg_time" label="平均停留时间" />
          </el-table>
        </div>
        
        <div class="funnel-insights">
          <h4>漏斗洞察</h4>
          <div class="insight-card" v-for="(insight, index) in insights" :key="index">
            <div class="insight-icon" :class="insight.type">
              <el-icon><component :is="insight.icon" /></el-icon>
            </div>
            <div class="insight-content">
              <div class="insight-title">{{ insight.title }}</div>
              <div class="insight-description">{{ insight.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 导出对话框 -->
    <el-dialog
      v-model="showExporter"
      title="导出招聘漏斗数据"
      width="80%"
    >
      <data-exporter />
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import RecruitmentFunnelChart from '@/components/analytics/RecruitmentFunnelChart.vue';
import DataExporter from '@/components/analytics/DataExporter.vue';

export default {
  name: 'RecruitmentFunnel',
  components: {
    RecruitmentFunnelChart,
    DataExporter
  },
  setup() {
    const router = useRouter();
    
    // 图表引用
    const funnelChartRef = ref(null);
    
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
    
    // 漏斗数据
    const funnelData = ref([
      {
        stage: '简历投递',
        count: 1200,
        percentage: 100,
        conversion_rate: '-',
        avg_time: '0天'
      },
      {
        stage: '简历筛选',
        count: 800,
        percentage: 66.7,
        conversion_rate: '66.7',
        avg_time: '2天'
      },
      {
        stage: '初试',
        count: 400,
        percentage: 33.3,
        conversion_rate: '50.0',
        avg_time: '5天'
      },
      {
        stage: '复试',
        count: 200,
        percentage: 16.7,
        conversion_rate: '50.0',
        avg_time: '3天'
      },
      {
        stage: '终试',
        count: 100,
        percentage: 8.3,
        conversion_rate: '50.0',
        avg_time: '2天'
      },
      {
        stage: '录用',
        count: 80,
        percentage: 6.7,
        conversion_rate: '80.0',
        avg_time: '3天'
      },
      {
        stage: '入职',
        count: 60,
        percentage: 5.0,
        conversion_rate: '75.0',
        avg_time: '14天'
      }
    ]);
    
    // 漏斗洞察
    const insights = ref([
      {
        title: '简历筛选转化率较低',
        description: '简历筛选阶段的转化率为66.7%，低于行业平均水平(75%)，建议优化职位描述和简历筛选标准。',
        icon: 'Warning',
        type: 'warning'
      },
      {
        title: '面试流程效率高',
        description: '从初试到终试的平均时间为10天，优于行业平均水平(15天)，面试流程效率较高。',
        icon: 'Success',
        type: 'success'
      },
      {
        title: 'Offer接受率高',
        description: 'Offer接受率为75%，高于行业平均水平(65%)，说明公司的薪资福利和雇主品牌具有竞争力。',
        icon: 'Star',
        type: 'primary'
      }
    ]);
    
    // 是否显示导出器
    const showExporter = ref(false);
    
    // 返回仪表盘
    const goBack = () => {
      router.push('/analytics');
    };
    
    // 处理筛选变更
    const handleFilterChange = () => {
      // 实际项目中，这里应该重新获取数据
      ElMessage.success('筛选条件已更新');
    };
    
    // 导出数据
    const exportData = () => {
      showExporter.value = true;
    };
    
    // 组件挂载时获取数据
    onMounted(() => {
      // 实际项目中，这里应该获取数据
    });
    
    return {
      funnelChartRef,
      timeRange,
      jobId,
      jobOptions,
      funnelData,
      insights,
      showExporter,
      goBack,
      handleFilterChange,
      exportData
    };
  }
};
</script>

<style scoped>
.recruitment-funnel-page {
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

.content-container {
  display: flex;
  flex: 1;
  gap: 20px;
}

.chart-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
}

.detail-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.detail-container h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #303133;
}

.funnel-stats {
  margin-bottom: 20px;
}

.funnel-insights h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
}

.insight-card {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.insight-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  font-size: 16px;
  color: #fff;
  flex-shrink: 0;
}

.insight-icon.primary {
  background-color: #409EFF;
}

.insight-icon.success {
  background-color: #67C23A;
}

.insight-icon.warning {
  background-color: #E6A23C;
}

.insight-icon.danger {
  background-color: #F56C6C;
}

.insight-content {
  flex: 1;
}

.insight-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.insight-description {
  font-size: 14px;
  color: #606266;
}
</style>
