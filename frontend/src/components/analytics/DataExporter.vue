<template>
  <div class="data-exporter">
    <div class="exporter-header">
      <h3>数据导出</h3>
      <p class="description">导出招聘数据分析报告，支持多种格式和自定义内容</p>
    </div>
    
    <el-form :model="exportForm" label-width="100px">
      <el-form-item label="报告名称" prop="name">
        <el-input v-model="exportForm.name" placeholder="请输入报告名称" />
      </el-form-item>
      
      <el-form-item label="时间范围" prop="timeRange">
        <el-date-picker
          v-model="exportForm.timeRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      
      <el-form-item label="职位筛选" prop="jobIds">
        <el-select
          v-model="exportForm.jobIds"
          multiple
          collapse-tags
          placeholder="请选择职位（可多选）"
          clearable
        >
          <el-option
            v-for="job in jobOptions"
            :key="job.value"
            :label="job.label"
            :value="job.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="导出格式" prop="format">
        <el-radio-group v-model="exportForm.format">
          <el-radio label="pdf">PDF</el-radio>
          <el-radio label="excel">Excel</el-radio>
          <el-radio label="word">Word</el-radio>
          <el-radio label="csv">CSV</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="报告内容">
        <el-checkbox-group v-model="exportForm.sections">
          <el-checkbox label="recruitment_funnel">招聘漏斗分析</el-checkbox>
          <el-checkbox label="channel_effectiveness">渠道效果分析</el-checkbox>
          <el-checkbox label="candidate_progress">候选人进展分析</el-checkbox>
          <el-checkbox label="time_to_hire">招聘周期分析</el-checkbox>
          <el-checkbox label="cost_analysis">招聘成本分析</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      
      <el-form-item label="包含图表">
        <el-switch v-model="exportForm.includeCharts" />
      </el-form-item>
      
      <el-form-item label="包含原始数据">
        <el-switch v-model="exportForm.includeRawData" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="exportData" :loading="exporting">导出数据</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <div class="export-history">
      <h4>导出历史</h4>
      <el-table :data="exportHistory" style="width: 100%">
        <el-table-column prop="name" label="报告名称" width="200" />
        <el-table-column prop="format" label="格式" width="100">
          <template #default="scope">
            <el-tag>{{ getFormatLabel(scope.row.format) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="size" label="文件大小" width="120" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="downloadReport(scope.row)"
            >
              下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'DataExporter',
  setup() {
    // 导出表单
    const exportForm = reactive({
      name: '招聘数据分析报告',
      timeRange: [
        new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
        new Date().toISOString().split('T')[0]
      ],
      jobIds: [],
      format: 'pdf',
      sections: ['recruitment_funnel', 'channel_effectiveness', 'candidate_progress'],
      includeCharts: true,
      includeRawData: false
    });
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 导出历史
    const exportHistory = ref([]);
    
    // 导出状态
    const exporting = ref(false);
    
    // 获取导出历史
    const fetchExportHistory = async () => {
      try {
        // 调用API获取导出历史
        // const response = await api.getExportHistory();
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: [
            {
              id: 1,
              name: '2025年Q1招聘数据分析报告',
              format: 'pdf',
              created_at: '2025-03-08T10:00:00Z',
              size: '2.5MB',
              url: '#'
            },
            {
              id: 2,
              name: '技术部招聘效果分析',
              format: 'excel',
              created_at: '2025-03-05T10:00:00Z',
              size: '1.8MB',
              url: '#'
            },
            {
              id: 3,
              name: '产品经理招聘漏斗分析',
              format: 'word',
              created_at: '2025-03-01T10:00:00Z',
              size: '3.2MB',
              url: '#'
            }
          ]
        };
        
        // 设置导出历史
        exportHistory.value = response.data;
      } catch (error) {
        console.error('获取导出历史失败:', error);
        ElMessage.error('获取导出历史失败，请重试');
      }
    };
    
    // 导出数据
    const exportData = async () => {
      if (exportForm.sections.length === 0) {
        ElMessage.warning('请至少选择一个报告内容');
        return;
      }
      
      exporting.value = true;
      
      try {
        // 构建导出参数
        const params = {
          name: exportForm.name,
          start_date: exportForm.timeRange[0],
          end_date: exportForm.timeRange[1],
          job_ids: exportForm.jobIds.length > 0 ? exportForm.jobIds : undefined,
          format: exportForm.format,
          sections: exportForm.sections,
          include_charts: exportForm.includeCharts,
          include_raw_data: exportForm.includeRawData
        };
        
        // 调用API导出数据
        // const response = await api.exportData(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // 模拟下载文件
        const fileName = `${exportForm.name}.${exportForm.format}`;
        ElMessage.success(`报告已导出为 ${fileName}`);
        
        // 刷新导出历史
        fetchExportHistory();
        
        // 实际项目中，这里应该处理文件下载
        // const url = window.URL.createObjectURL(new Blob([response.data]));
        // const link = document.createElement('a');
        // link.href = url;
        // link.setAttribute('download', fileName);
        // document.body.appendChild(link);
        // link.click();
        // document.body.removeChild(link);
      } catch (error) {
        console.error('导出数据失败:', error);
        ElMessage.error('导出数据失败，请重试');
      } finally {
        exporting.value = false;
      }
    };
    
    // 重置表单
    const resetForm = () => {
      exportForm.name = '招聘数据分析报告';
      exportForm.timeRange = [
        new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
        new Date().toISOString().split('T')[0]
      ];
      exportForm.jobIds = [];
      exportForm.format = 'pdf';
      exportForm.sections = ['recruitment_funnel', 'channel_effectiveness', 'candidate_progress'];
      exportForm.includeCharts = true;
      exportForm.includeRawData = false;
    };
    
    // 下载报告
    const downloadReport = (report) => {
      // 实际项目中，这里应该处理文件下载
      // window.open(report.url, '_blank');
      
      ElMessage.success(`正在下载 ${report.name}`);
    };
    
    // 获取格式标签
    const getFormatLabel = (format) => {
      const formatMap = {
        'pdf': 'PDF',
        'excel': 'Excel',
        'word': 'Word',
        'csv': 'CSV'
      };
      
      return formatMap[format] || format;
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 组件挂载时获取导出历史
    onMounted(() => {
      fetchExportHistory();
    });
    
    return {
      exportForm,
      jobOptions,
      exportHistory,
      exporting,
      exportData,
      resetForm,
      downloadReport,
      getFormatLabel,
      formatDate
    };
  }
};
</script>

<style scoped>
.data-exporter {
  padding: 20px;
}

.exporter-header {
  margin-bottom: 20px;
}

.exporter-header h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.description {
  color: #606266;
  margin: 0;
}

.export-history {
  margin-top: 30px;
}

.export-history h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #303133;
}
</style>
