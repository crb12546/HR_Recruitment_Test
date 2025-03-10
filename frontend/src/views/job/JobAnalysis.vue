<template>
  <div class="job-analysis-page">
    <div class="page-header">
      <h2>招聘需求分析</h2>
      <p class="description">分析招聘需求的匹配情况和招聘进展</p>
    </div>
    
    <div class="filter-container">
      <el-select
        v-model="selectedJob"
        placeholder="选择招聘需求"
        filterable
        clearable
        @change="handleJobChange"
      >
        <el-option
          v-for="job in jobOptions"
          :key="job.value"
          :label="job.label"
          :value="job.value"
        />
      </el-select>
      
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleDateChange"
      />
      
      <el-button type="primary" @click="fetchAnalysisData">分析</el-button>
    </div>
    
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!selectedJob" class="empty-container">
      <el-empty description="请选择一个招聘需求进行分析" />
    </div>
    
    <div v-else class="analysis-container">
      <!-- 匹配度分布 -->
      <div class="chart-card">
        <h3>简历匹配度分布</h3>
        <div class="chart-container" ref="matchDistributionChart"></div>
      </div>
      
      <!-- 招聘漏斗 -->
      <div class="chart-card">
        <h3>招聘漏斗</h3>
        <div class="chart-container" ref="recruitmentFunnelChart"></div>
      </div>
      
      <!-- 技能匹配分析 -->
      <div class="chart-card">
        <h3>技能匹配分析</h3>
        <div class="chart-container" ref="skillMatchChart"></div>
      </div>
      
      <!-- 候选人来源分析 -->
      <div class="chart-card">
        <h3>候选人来源分析</h3>
        <div class="chart-container" ref="candidateSourceChart"></div>
      </div>
      
      <!-- 匹配简历列表 -->
      <div class="data-card">
        <h3>匹配简历列表</h3>
        <el-table :data="matchedResumes" style="width: 100%">
          <el-table-column prop="candidate_name" label="候选人" width="120" />
          <el-table-column prop="match_score" label="匹配度" width="100">
            <template #default="scope">
              <el-progress
                :percentage="scope.row.match_score"
                :color="getMatchScoreColor(scope.row.match_score)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="match_explanation" label="匹配说明" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="viewResume(scope.row)"
              >
                查看简历
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';

export default {
  name: 'JobAnalysis',
  setup() {
    const router = useRouter();
    
    // 选中的职位
    const selectedJob = ref(null);
    
    // 日期范围
    const dateRange = ref([]);
    
    // 加载状态
    const loading = ref(false);
    
    // 职位选项
    const jobOptions = ref([]);
    
    // 匹配的简历
    const matchedResumes = ref([]);
    
    // 图表引用
    const matchDistributionChart = ref(null);
    const recruitmentFunnelChart = ref(null);
    const skillMatchChart = ref(null);
    const candidateSourceChart = ref(null);
    
    // 图表实例
    let matchDistributionChartInstance = null;
    let recruitmentFunnelChartInstance = null;
    let skillMatchChartInstance = null;
    let candidateSourceChartInstance = null;
    
    // 获取职位选项
    const fetchJobOptions = async () => {
      try {
        // 调用API获取职位列表
        // const response = await api.getJobList();
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: {
            items: [
              { id: 1, position_name: '前端开发工程师' },
              { id: 2, position_name: '后端开发工程师' },
              { id: 3, position_name: '产品经理' }
            ]
          }
        };
        
        // 设置职位选项
        jobOptions.value = response.data.items.map(job => ({
          value: job.id,
          label: job.position_name
        }));
      } catch (error) {
        console.error('获取职位列表失败:', error);
        ElMessage.error('获取职位列表失败，请重试');
      }
    };
    
    // 获取分析数据
    const fetchAnalysisData = async () => {
      if (!selectedJob.value) {
        ElMessage.warning('请选择一个招聘需求');
        return;
      }
      
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          job_id: selectedJob.value,
          start_date: dateRange.value && dateRange.value[0] ? dateRange.value[0].toISOString() : undefined,
          end_date: dateRange.value && dateRange.value[1] ? dateRange.value[1].toISOString() : undefined
        };
        
        // 调用API获取分析数据
        // const response = await api.getJobAnalysis(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            match_distribution: {
              categories: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
              data: [5, 10, 15, 8, 3]
            },
            recruitment_funnel: {
              stages: ['简历筛选', '初试', '复试', '终试', '录用'],
              data: [41, 25, 15, 8, 3]
            },
            skill_match: {
              skills: ['JavaScript', 'Vue.js', 'HTML/CSS', '团队协作', '沟通能力'],
              required: [90, 80, 70, 60, 50],
              average: [70, 65, 75, 55, 60]
            },
            candidate_source: {
              sources: ['内部推荐', '招聘网站', '猎头', '校园招聘', '其他'],
              data: [15, 40, 20, 15, 10]
            },
            matched_resumes: [
              {
                id: 1,
                resume_id: 101,
                candidate_name: '张三',
                match_score: 85,
                status: '初试通过',
                match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
              },
              {
                id: 2,
                resume_id: 102,
                candidate_name: '李四',
                match_score: 70,
                status: '待面试',
                match_explanation: '候选人具备基本技能要求，但工作经验略显不足。'
              },
              {
                id: 3,
                resume_id: 103,
                candidate_name: '王五',
                match_score: 60,
                status: '已淘汰',
                match_explanation: '候选人技能与职位要求部分匹配，缺乏核心技能。'
              }
            ]
          }
        };
        
        // 设置匹配的简历
        matchedResumes.value = response.data.matched_resumes;
        
        // 渲染图表
        nextTick(() => {
          renderMatchDistributionChart(response.data.match_distribution);
          renderRecruitmentFunnelChart(response.data.recruitment_funnel);
          renderSkillMatchChart(response.data.skill_match);
          renderCandidateSourceChart(response.data.candidate_source);
        });
      } catch (error) {
        console.error('获取分析数据失败:', error);
        ElMessage.error('获取分析数据失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 处理职位变更
    const handleJobChange = () => {
      if (selectedJob.value) {
        fetchAnalysisData();
      } else {
        // 清空图表和数据
        matchedResumes.value = [];
        destroyCharts();
      }
    };
    
    // 处理日期变更
    const handleDateChange = () => {
      if (selectedJob.value) {
        fetchAnalysisData();
      }
    };
    
    // 查看简历
    const viewResume = (matchedResume) => {
      router.push(`/resumes/${matchedResume.resume_id}`);
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 获取状态标签类型
    const getStatusTagType = (status) => {
      switch (status) {
        case '已录用':
          return 'success';
        case '初试通过':
        case '复试通过':
          return 'primary';
        case '待面试':
          return 'info';
        case '已淘汰':
          return 'danger';
        default:
          return '';
      }
    };
    
    // 渲染匹配度分布图表
    const renderMatchDistributionChart = (data) => {
      if (!matchDistributionChart.value) return;
      
      if (!matchDistributionChartInstance) {
        matchDistributionChartInstance = echarts.init(matchDistributionChart.value);
      }
      
      const option = {
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
          data: data.categories
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '简历数量',
            type: 'bar',
            data: data.data,
            itemStyle: {
              color: function(params) {
                const colorList = ['#F56C6C', '#E6A23C', '#909399', '#67C23A', '#409EFF'];
                return colorList[params.dataIndex];
              }
            }
          }
        ]
      };
      
      matchDistributionChartInstance.setOption(option);
    };
    
    // 渲染招聘漏斗图表
    const renderRecruitmentFunnelChart = (data) => {
      if (!recruitmentFunnelChart.value) return;
      
      if (!recruitmentFunnelChartInstance) {
        recruitmentFunnelChartInstance = echarts.init(recruitmentFunnelChart.value);
      }
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}'
        },
        series: [
          {
            name: '招聘漏斗',
            type: 'funnel',
            left: '10%',
            top: 60,
            bottom: 60,
            width: '80%',
            min: 0,
            max: Math.max(...data.data) * 1.2,
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
            data: data.stages.map((stage, index) => ({
              value: data.data[index],
              name: `${stage}: ${data.data[index]}`
            }))
          }
        ]
      };
      
      recruitmentFunnelChartInstance.setOption(option);
    };
    
    // 渲染技能匹配图表
    const renderSkillMatchChart = (data) => {
      if (!skillMatchChart.value) return;
      
      if (!skillMatchChartInstance) {
        skillMatchChartInstance = echarts.init(skillMatchChart.value);
      }
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['需求技能', '平均水平']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          max: 100
        },
        yAxis: {
          type: 'category',
          data: data.skills
        },
        series: [
          {
            name: '需求技能',
            type: 'bar',
            data: data.required,
            itemStyle: {
              color: '#409EFF'
            }
          },
          {
            name: '平均水平',
            type: 'bar',
            data: data.average,
            itemStyle: {
              color: '#67C23A'
            }
          }
        ]
      };
      
      skillMatchChartInstance.setOption(option);
    };
    
    // 渲染候选人来源图表
    const renderCandidateSourceChart = (data) => {
      if (!candidateSourceChart.value) return;
      
      if (!candidateSourceChartInstance) {
        candidateSourceChartInstance = echarts.init(candidateSourceChart.value);
      }
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: data.sources
        },
        series: [
          {
            name: '候选人来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: data.sources.map((source, index) => ({
              value: data.data[index],
              name: source
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
      
      candidateSourceChartInstance.setOption(option);
    };
    
    // 销毁图表
    const destroyCharts = () => {
      if (matchDistributionChartInstance) {
        matchDistributionChartInstance.dispose();
        matchDistributionChartInstance = null;
      }
      
      if (recruitmentFunnelChartInstance) {
        recruitmentFunnelChartInstance.dispose();
        recruitmentFunnelChartInstance = null;
      }
      
      if (skillMatchChartInstance) {
        skillMatchChartInstance.dispose();
        skillMatchChartInstance = null;
      }
      
      if (candidateSourceChartInstance) {
        candidateSourceChartInstance.dispose();
        candidateSourceChartInstance = null;
      }
    };
    
    // 监听窗口大小变化
    const handleResize = () => {
      if (matchDistributionChartInstance) {
        matchDistributionChartInstance.resize();
      }
      
      if (recruitmentFunnelChartInstance) {
        recruitmentFunnelChartInstance.resize();
      }
      
      if (skillMatchChartInstance) {
        skillMatchChartInstance.resize();
      }
      
      if (candidateSourceChartInstance) {
        candidateSourceChartInstance.resize();
      }
    };
    
    // 组件挂载时获取职位选项
    onMounted(() => {
      fetchJobOptions();
      window.addEventListener('resize', handleResize);
    });
    
    // 组件卸载时销毁图表
    const onUnmounted = () => {
      destroyCharts();
      window.removeEventListener('resize', handleResize);
    };
    
    return {
      selectedJob,
      dateRange,
      loading,
      jobOptions,
      matchedResumes,
      matchDistributionChart,
      recruitmentFunnelChart,
      skillMatchChart,
      candidateSourceChart,
      handleJobChange,
      handleDateChange,
      fetchAnalysisData,
      viewResume,
      getMatchScoreColor,
      getStatusTagType,
      onUnmounted
    };
  }
};
</script>

<style scoped>
.job-analysis-page {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #303133;
}

.description {
  color: #606266;
  margin: 0;
}

.filter-container {
  display: flex;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.loading-container, .empty-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.analysis-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card, .data-card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-card h3, .data-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.chart-container {
  height: 300px;
}

.data-card {
  grid-column: span 2;
}
</style>
