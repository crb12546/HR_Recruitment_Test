<template>
  <div class="plan-exporter">
    <div class="export-options">
      <h3>导出选项</h3>
      <el-form :model="exportOptions" label-width="100px">
        <el-form-item label="导出格式">
          <el-radio-group v-model="exportOptions.format">
            <el-radio label="pdf">PDF</el-radio>
            <el-radio label="docx">Word</el-radio>
            <el-radio label="xlsx">Excel</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="内容选择">
          <el-checkbox-group v-model="exportOptions.sections">
            <el-checkbox label="basic_info">基本信息</el-checkbox>
            <el-checkbox label="job_info">职位信息</el-checkbox>
            <el-checkbox label="candidates">候选人列表</el-checkbox>
            <el-checkbox label="strategy">招聘策略</el-checkbox>
            <el-checkbox label="timeline">招聘时间线</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="包含图表">
          <el-switch v-model="exportOptions.includeCharts" />
        </el-form-item>
        
        <el-form-item label="包含附件">
          <el-switch v-model="exportOptions.includeAttachments" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="exportPlan" :loading="exporting">导出方案</el-button>
          <el-button @click="resetOptions">重置选项</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="preview-container" v-if="showPreview">
      <h3>预览</h3>
      <div class="preview-content">
        <div class="preview-header">
          <h2>{{ plan.name }}</h2>
          <p class="preview-date">生成日期：{{ formatDate(new Date()) }}</p>
        </div>
        
        <div v-if="exportOptions.sections.includes('basic_info')" class="preview-section">
          <h3>基本信息</h3>
          <p><strong>方案名称：</strong>{{ plan.name }}</p>
          <p><strong>方案描述：</strong>{{ plan.description || '无' }}</p>
          <p><strong>招聘周期：</strong>{{ plan.recruitment_cycle || '30天' }}</p>
        </div>
        
        <div v-if="exportOptions.sections.includes('job_info')" class="preview-section">
          <h3>职位信息</h3>
          <p><strong>职位名称：</strong>{{ plan.job?.position_name || '未知' }}</p>
          <p><strong>部门：</strong>{{ plan.job?.department || '未知' }}</p>
          <p><strong>工作地点：</strong>{{ plan.job?.location || '未知' }}</p>
          <p><strong>薪资范围：</strong>{{ plan.job?.salary_range || '未知' }}</p>
          <p><strong>职位描述：</strong>{{ plan.job?.responsibilities || '无' }}</p>
          <p><strong>任职要求：</strong>{{ plan.job?.requirements || '无' }}</p>
        </div>
        
        <div v-if="exportOptions.sections.includes('candidates')" class="preview-section">
          <h3>候选人列表</h3>
          <el-table :data="plan.candidates || []" style="width: 100%">
            <el-table-column prop="candidate_name" label="候选人" width="120" />
            <el-table-column prop="match_score" label="匹配度" width="100">
              <template #default="scope">
                <el-progress
                  :percentage="scope.row.match_score"
                  :color="getMatchScoreColor(scope.row.match_score)"
                  :stroke-width="6"
                />
              </template>
            </el-table-column>
            <el-table-column prop="match_explanation" label="匹配说明" />
          </el-table>
        </div>
        
        <div v-if="exportOptions.sections.includes('strategy')" class="preview-section">
          <h3>招聘策略</h3>
          <p><strong>面试轮次：</strong>{{ plan.interview_rounds || 3 }}轮</p>
          <p><strong>面试方式：</strong>{{ (plan.interview_methods || []).join('、') }}</p>
          <p><strong>招聘建议：</strong>{{ plan.recruitment_suggestion || '无' }}</p>
        </div>
        
        <div v-if="exportOptions.sections.includes('timeline')" class="preview-section">
          <h3>招聘时间线</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(activity, index) in recruitmentTimeline"
              :key="index"
              :timestamp="activity.time"
              :type="activity.type"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <div v-if="exportOptions.includeCharts" class="preview-section">
          <h3>匹配分析图表</h3>
          <div class="chart-placeholder">
            <p>此处将显示候选人匹配度分析图表</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'PlanExporter',
  props: {
    plan: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    // 导出选项
    const exportOptions = reactive({
      format: 'pdf',
      sections: ['basic_info', 'job_info', 'candidates', 'strategy', 'timeline'],
      includeCharts: true,
      includeAttachments: false
    });
    
    // 导出状态
    const exporting = ref(false);
    
    // 是否显示预览
    const showPreview = ref(true);
    
    // 招聘时间线
    const recruitmentTimeline = computed(() => {
      const timeline = [];
      const now = new Date();
      
      // 开始日期
      timeline.push({
        content: '开始招聘',
        time: formatDate(now),
        type: 'primary'
      });
      
      // 简历筛选
      const screeningDate = new Date(now);
      screeningDate.setDate(screeningDate.getDate() + 7);
      timeline.push({
        content: '完成简历筛选',
        time: formatDate(screeningDate),
        type: 'success'
      });
      
      // 面试阶段
      const interviewRounds = props.plan.interview_rounds || 3;
      let lastDate = new Date(screeningDate);
      
      for (let i = 1; i <= interviewRounds; i++) {
        lastDate.setDate(lastDate.getDate() + 5);
        timeline.push({
          content: `第${i}轮面试`,
          time: formatDate(new Date(lastDate)),
          type: 'info'
        });
      }
      
      // 录用决策
      lastDate.setDate(lastDate.getDate() + 3);
      timeline.push({
        content: '做出录用决策',
        time: formatDate(new Date(lastDate)),
        type: 'warning'
      });
      
      // 入职
      lastDate.setDate(lastDate.getDate() + 14);
      timeline.push({
        content: '候选人入职',
        time: formatDate(new Date(lastDate)),
        type: 'success'
      });
      
      return timeline;
    });
    
    // 导出方案
    const exportPlan = async () => {
      if (exportOptions.sections.length === 0) {
        ElMessage.warning('请至少选择一个导出内容');
        return;
      }
      
      exporting.value = true;
      
      try {
        // 构建导出参数
        const params = {
          plan_id: props.plan.id,
          format: exportOptions.format,
          sections: exportOptions.sections,
          include_charts: exportOptions.includeCharts,
          include_attachments: exportOptions.includeAttachments
        };
        
        // 调用API导出方案
        // const response = await api.exportPlan(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // 模拟下载文件
        const fileName = `${props.plan.name}.${exportOptions.format}`;
        ElMessage.success(`方案已导出为 ${fileName}`);
        
        // 实际项目中，这里应该处理文件下载
        // const url = window.URL.createObjectURL(new Blob([response.data]));
        // const link = document.createElement('a');
        // link.href = url;
        // link.setAttribute('download', fileName);
        // document.body.appendChild(link);
        // link.click();
        // document.body.removeChild(link);
      } catch (error) {
        console.error('导出方案失败:', error);
        ElMessage.error('导出方案失败，请重试');
      } finally {
        exporting.value = false;
      }
    };
    
    // 重置选项
    const resetOptions = () => {
      exportOptions.format = 'pdf';
      exportOptions.sections = ['basic_info', 'job_info', 'candidates', 'strategy', 'timeline'];
      exportOptions.includeCharts = true;
      exportOptions.includeAttachments = false;
    };
    
    // 格式化日期
    const formatDate = (date) => {
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    return {
      exportOptions,
      exporting,
      showPreview,
      recruitmentTimeline,
      exportPlan,
      resetOptions,
      formatDate,
      getMatchScoreColor
    };
  }
};
</script>

<style scoped>
.plan-exporter {
  padding: 20px;
  display: flex;
  gap: 20px;
}

.export-options {
  flex: 0 0 300px;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
}

.export-options h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.preview-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.preview-container h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.preview-content {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 20px;
  background-color: #fff;
}

.preview-header {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.preview-header h2 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #303133;
}

.preview-date {
  color: #606266;
  margin: 0;
}

.preview-section {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.preview-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.preview-section p {
  margin: 5px 0;
  color: #606266;
}

.chart-placeholder {
  height: 200px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
}
</style>
