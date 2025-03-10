<template>
  <div class="channel-effectiveness-chart">
    <div class="chart-header">
      <h3>招聘渠道效果分析</h3>
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
        
        <el-select v-model="metricType" placeholder="指标类型" size="small" @change="fetchData">
          <el-option label="简历数量" value="resume_count" />
          <el-option label="面试转化率" value="interview_rate" />
          <el-option label="录用率" value="offer_rate" />
          <el-option label="入职率" value="onboard_rate" />
          <el-option label="综合评分" value="overall_score" />
        </el-select>
      </div>
    </div>
    
    <div v-loading="loading" class="chart-container">
      <div ref="chartRef" class="echarts-container"></div>
    </div>
    
    <div class="chart-footer">
      <div class="channel-stats">
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
          <el-table-column prop="overall_score" label="综合评分" width="100">
            <template #default="scope">
              <el-rate
                v-model="scope.row.overall_score"
                disabled
                :max="5"
                :colors="['#F56C6C', '#E6A23C', '#67C23A']"
                :allow-half="true"
              />
            </template>
          </el-table-column>
          <el-table-column prop="cost_per_hire" label="招聘成本" width="120">
            <template #default="scope">
              {{ scope.row.cost_per_hire }}元
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
  name: 'ChannelEffectivenessChart',
  props: {
    initialJobId: {
      type: [Number, String],
      default: null
    },
    initialTimeRange: {
      type: String,
      default: '30days'
    },
    initialMetricType: {
      type: String,
      default: 'resume_count'
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
    
    // 指标类型
    const metricType = ref(props.initialMetricType);
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 渠道数据
    const channelData = ref([]);
    
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
          job_id: jobId.value || undefined,
          metric_type: metricType.value
        };
        
        // 调用API获取渠道数据
        // const response = await api.getChannelEffectivenessData(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: [
            {
              name: '智联招聘',
              resume_count: 320,
              interview_rate: 45.5,
              offer_rate: 28.3,
              onboard_rate: 85.2,
              overall_score: 4.2,
              cost_per_hire: 3200
            },
            {
              name: '前程无忧',
              resume_count: 280,
              interview_rate: 42.8,
              offer_rate: 25.6,
              onboard_rate: 82.5,
              overall_score: 4.0,
              cost_per_hire: 3500
            },
            {
              name: 'BOSS直聘',
              resume_count: 420,
              interview_rate: 38.2,
              offer_rate: 22.1,
              onboard_rate: 78.6,
              overall_score: 3.8,
              cost_per_hire: 2800
            },
            {
              name: '拉勾网',
              resume_count: 180,
              interview_rate: 52.3,
              offer_rate: 32.5,
              onboard_rate: 88.7,
              overall_score: 4.5,
              cost_per_hire: 4200
            },
            {
              name: '猎聘网',
              resume_count: 150,
              interview_rate: 58.6,
              offer_rate: 35.2,
              onboard_rate: 90.1,
              overall_score: 4.7,
              cost_per_hire: 5500
            },
            {
              name: '内部推荐',
              resume_count: 85,
              interview_rate: 68.2,
              offer_rate: 42.3,
              onboard_rate: 95.6,
              overall_score: 4.9,
              cost_per_hire: 2000
            },
            {
              name: '校园招聘',
              resume_count: 220,
              interview_rate: 35.8,
              offer_rate: 28.6,
              onboard_rate: 82.3,
              overall_score: 3.5,
              cost_per_hire: 2500
            }
          ]
        };
        
        // 设置渠道数据
        channelData.value = response.data;
        
        // 更新图表
        updateChart();
      } catch (error) {
        console.error('获取招聘渠道数据失败:', error);
        ElMessage.error('获取招聘渠道数据失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 更新图表
    const updateChart = () => {
      if (!chart || channelData.value.length === 0) return;
      
      // 准备数据
      const categories = channelData.value.map(item => item.name);
      const data = channelData.value.map(item => item[metricType.value]);
      
      // 获取指标名称
      const metricName = getMetricName(metricType.value);
      
      // 设置图表选项
      const option = {
        title: {
          text: `招聘渠道${metricName}对比`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: categories,
          axisLabel: {
            interval: 0,
            rotate: 30
          }
        },
        yAxis: {
          type: 'value',
          name: metricName
        },
        series: [
          {
            name: metricName,
            type: 'bar',
            data: data,
            itemStyle: {
              color: function(params) {
                // 根据数值设置不同的颜色
                const value = params.value;
                if (metricType.value === 'resume_count') {
                  if (value > 300) return '#67C23A';
                  if (value > 200) return '#E6A23C';
                  return '#F56C6C';
                } else {
                  if (value > 80) return '#67C23A';
                  if (value > 50) return '#E6A23C';
                  return '#F56C6C';
                }
              }
            },
            label: {
              show: true,
              position: 'top',
              formatter: function(params) {
                if (metricType.value !== 'resume_count' && metricType.value !== 'overall_score' && metricType.value !== 'cost_per_hire') {
                  return params.value + '%';
                }
                return params.value;
              }
            }
          }
        ]
      };
      
      // 设置图表选项
      chart.setOption(option);
    };
    
    // 获取指标名称
    const getMetricName = (metricType) => {
      const metricNameMap = {
        'resume_count': '简历数量',
        'interview_rate': '面试转化率',
        'offer_rate': '录用率',
        'onboard_rate': '入职率',
        'overall_score': '综合评分',
        'cost_per_hire': '招聘成本'
      };
      
      return metricNameMap[metricType] || '数据';
    };
    
    // 监听时间范围变化
    watch(timeRange, () => {
      fetchData();
    });
    
    // 监听职位ID变化
    watch(jobId, () => {
      fetchData();
    });
    
    // 监听指标类型变化
    watch(metricType, () => {
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
      metricType,
      jobOptions,
      channelData,
      fetchData
    };
  }
};
</script>

<style scoped>
.channel-effectiveness-chart {
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

.channel-stats {
  width: 100%;
}
</style>
