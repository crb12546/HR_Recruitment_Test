<template>
  <div class="recruitment-funnel-chart">
    <div class="chart-header">
      <h3>招聘漏斗分析</h3>
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
      </div>
    </div>
    
    <div v-loading="loading" class="chart-container">
      <div ref="chartRef" class="echarts-container"></div>
    </div>
    
    <div class="chart-footer">
      <div class="funnel-stats">
        <div v-for="(stage, index) in funnelData" :key="index" class="stat-item">
          <div class="stat-label">{{ stage.name }}</div>
          <div class="stat-value">{{ stage.value }}</div>
          <div class="stat-rate" v-if="index > 0">
            转化率: {{ calculateConversionRate(index) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
import analyticsApi from '@/api/analytics';

export default {
  name: 'RecruitmentFunnelChart',
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
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 漏斗数据
    const funnelData = ref([]);
    
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
        
        // 调用API获取漏斗数据
        const response = await analyticsApi.getFunnelData(params);
        
        // 转换数据格式
        const data = response.data.data.map(item => ({
          name: item.stage,
          value: item.count
        }));
        
        // 设置漏斗数据
        funnelData.value = data;
        
        // 更新图表
        updateChart();
      } catch (error) {
        console.error('获取招聘漏斗数据失败:', error);
        ElMessage.error('获取招聘漏斗数据失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 更新图表
    const updateChart = () => {
      if (!chart || funnelData.value.length === 0) return;
      
      // 准备数据
      const data = funnelData.value.map(item => ({
        value: item.value,
        name: item.name
      }));
      
      // 设置图表选项
      const option = {
        title: {
          text: '招聘流程漏斗图',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: funnelData.value.map(item => item.name)
        },
        series: [
          {
            name: '招聘流程',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: data[0].value,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
              show: true,
              position: 'inside'
            },
            labelLine: {
              length: 10,
              lineStyle: {
                width: 1,
                type: 'solid'
              }
            },
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 1
            },
            emphasis: {
              label: {
                fontSize: 20
              }
            },
            data: data
          }
        ]
      };
      
      // 设置图表选项
      chart.setOption(option);
    };
    
    // 计算转化率
    const calculateConversionRate = (index) => {
      if (index <= 0 || !funnelData.value[index] || !funnelData.value[index - 1]) return 0;
      
      const current = funnelData.value[index].value;
      const previous = funnelData.value[index - 1].value;
      
      if (previous === 0) return 0;
      
      return ((current / previous) * 100).toFixed(2);
    };
    
    // 监听时间范围变化
    watch(timeRange, () => {
      fetchData();
    });
    
    // 监听职位ID变化
    watch(jobId, () => {
      fetchData();
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
      jobOptions,
      funnelData,
      fetchData,
      calculateConversionRate
    };
  }
};
</script>

<style scoped>
.recruitment-funnel-chart {
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

.funnel-stats {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.stat-item {
  flex: 1;
  min-width: 120px;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 10px;
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-rate {
  font-size: 12px;
  color: #67C23A;
}
</style>
