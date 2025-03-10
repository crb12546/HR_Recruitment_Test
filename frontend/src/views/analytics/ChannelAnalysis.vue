<template>
  <div class="channel-analysis-page">
    <div class="page-header">
      <h2>招聘渠道分析</h2>
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
      
      <el-select v-model="metricType" placeholder="指标类型" @change="handleFilterChange">
        <el-option label="简历数量" value="resume_count" />
        <el-option label="面试转化率" value="interview_rate" />
        <el-option label="录用率" value="offer_rate" />
        <el-option label="入职率" value="onboard_rate" />
        <el-option label="综合评分" value="overall_score" />
        <el-option label="招聘成本" value="cost_per_hire" />
      </el-select>
    </div>
    
    <div class="content-container">
      <div class="chart-container">
        <channel-effectiveness-chart
          :initial-job-id="jobId"
          :initial-time-range="timeRange"
          :initial-metric-type="metricType"
          ref="channelChartRef"
        />
      </div>
      
      <div class="detail-container">
        <h3>渠道详情分析</h3>
        
        <div class="channel-comparison">
          <el-table :data="channelData" style="width: 100%">
            <el-table-column prop="name" label="招聘渠道" width="150" />
            <el-table-column prop="resume_count" label="简历数量" width="100" />
            <el-table-column prop="interview_rate" label="面试转化率" width="120">
              <template #default="scope">
                {{ scope.row.interview_rate }}%
              </template>
            </el-table-column>
            <el-table-column prop="offer_rate" label="录用率" width="100">
              <template #default="scope">
                {{ scope.row.offer_rate }}%
              </template>
            </el-table-column>
            <el-table-column prop="onboard_rate" label="入职率" width="100">
              <template #default="scope">
                {{ scope.row.onboard_rate }}%
              </template>
            </el-table-column>
            <el-table-column prop="cost_per_hire" label="招聘成本" width="120">
              <template #default="scope">
                {{ scope.row.cost_per_hire }}元
              </template>
            </el-table-column>
            <el-table-column prop="roi" label="投资回报率" width="120">
              <template #default="scope">
                {{ scope.row.roi }}%
              </template>
            </el-table-column>
          </el-table>
        </div>
        
        <div class="channel-insights">
          <h4>渠道洞察</h4>
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
        
        <div class="channel-recommendations">
          <h4>渠道优化建议</h4>
          <el-collapse>
            <el-collapse-item title="预算分配优化" name="1">
              <p>根据各渠道的招聘效果和成本，建议调整预算分配：</p>
              <ul>
                <li>增加内部推荐计划预算，提高奖励金额</li>
                <li>减少前程无忧的投入，转向拉勾网和BOSS直聘</li>
                <li>保持猎聘网的投入，专注高级职位招聘</li>
              </ul>
            </el-collapse-item>
            <el-collapse-item title="渠道组合策略" name="2">
              <p>针对不同职位类型，采用不同的渠道组合：</p>
              <ul>
                <li>技术岗位：BOSS直聘 + 拉勾网 + 内部推荐</li>
                <li>产品岗位：拉勾网 + 智联招聘 + 校园招聘</li>
                <li>管理岗位：猎聘网 + 内部推荐</li>
              </ul>
            </el-collapse-item>
            <el-collapse-item title="渠道效果提升" name="3">
              <p>提高各渠道的招聘效果：</p>
              <ul>
                <li>优化职位描述和关键词，提高搜索匹配度</li>
                <li>改进简历筛选流程，减少筛选时间</li>
                <li>加强雇主品牌建设，提高求职者关注度</li>
              </ul>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </div>
    
    <!-- 导出对话框 -->
    <el-dialog
      v-model="showExporter"
      title="导出招聘渠道数据"
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
import ChannelEffectivenessChart from '@/components/analytics/ChannelEffectivenessChart.vue';
import DataExporter from '@/components/analytics/DataExporter.vue';

export default {
  name: 'ChannelAnalysis',
  components: {
    ChannelEffectivenessChart,
    DataExporter
  },
  setup() {
    const router = useRouter();
    
    // 图表引用
    const channelChartRef = ref(null);
    
    // 时间范围
    const timeRange = ref('30days');
    
    // 职位ID
    const jobId = ref(null);
    
    // 指标类型
    const metricType = ref('resume_count');
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 渠道数据
    const channelData = ref([
      {
        name: '智联招聘',
        resume_count: 320,
        interview_rate: 45.5,
        offer_rate: 28.3,
        onboard_rate: 85.2,
        cost_per_hire: 3200,
        roi: 125.6
      },
      {
        name: '前程无忧',
        resume_count: 280,
        interview_rate: 42.8,
        offer_rate: 25.6,
        onboard_rate: 82.5,
        cost_per_hire: 3500,
        roi: 108.3
      },
      {
        name: 'BOSS直聘',
        resume_count: 420,
        interview_rate: 38.2,
        offer_rate: 22.1,
        onboard_rate: 78.6,
        cost_per_hire: 2800,
        roi: 142.5
      },
      {
        name: '拉勾网',
        resume_count: 180,
        interview_rate: 52.3,
        offer_rate: 32.5,
        onboard_rate: 88.7,
        cost_per_hire: 4200,
        roi: 118.2
      },
      {
        name: '猎聘网',
        resume_count: 150,
        interview_rate: 58.6,
        offer_rate: 35.2,
        onboard_rate: 90.1,
        cost_per_hire: 5500,
        roi: 95.8
      },
      {
        name: '内部推荐',
        resume_count: 85,
        interview_rate: 68.2,
        offer_rate: 42.3,
        onboard_rate: 95.6,
        cost_per_hire: 2000,
        roi: 215.3
      },
      {
        name: '校园招聘',
        resume_count: 220,
        interview_rate: 35.8,
        offer_rate: 28.6,
        onboard_rate: 82.3,
        cost_per_hire: 2500,
        roi: 156.7
      }
    ]);
    
    // 渠道洞察
    const insights = ref([
      {
        title: '内部推荐效果最佳',
        description: '内部推荐的面试转化率(68.2%)和录用率(42.3%)均为最高，且招聘成本最低，投资回报率最高(215.3%)。',
        icon: 'Star',
        type: 'success'
      },
      {
        title: 'BOSS直聘简历数量最多',
        description: 'BOSS直聘提供了最多的简历数量(420)，但面试转化率较低(38.2%)，需要优化筛选效率。',
        icon: 'DataLine',
        type: 'primary'
      },
      {
        title: '猎聘网成本较高',
        description: '猎聘网的招聘成本最高(5500元/人)，投资回报率最低(95.8%)，建议仅用于招聘高级职位。',
        icon: 'Warning',
        type: 'warning'
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
      channelChartRef,
      timeRange,
      jobId,
      metricType,
      jobOptions,
      channelData,
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
.channel-analysis-page {
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
  overflow-y: auto;
}

.detail-container h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #303133;
}

.channel-comparison {
  margin-bottom: 20px;
}

.channel-insights {
  margin-bottom: 20px;
}

.channel-insights h4,
.channel-recommendations h4 {
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

.channel-recommendations {
  margin-top: auto;
}

.channel-recommendations ul {
  margin: 0;
  padding-left: 20px;
}

.channel-recommendations li {
  margin-bottom: 5px;
}
</style>
