<template>
  <div class="plan-generation-page">
    <div class="page-header">
      <h2>生成招聘方案</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          返回列表
        </el-button>
      </div>
    </div>
    
    <div class="content-container">
      <plan-generator 
        :initial-job-id="initialJobId" 
        :initial-candidates="initialCandidates"
        @plan-generated="handlePlanGenerated"
      />
    </div>
    
    <!-- 方案生成成功对话框 -->
    <el-dialog
      v-model="showSuccessDialog"
      title="方案生成成功"
      width="50%"
    >
      <div class="success-content">
        <el-result
          icon="success"
          title="招聘方案生成成功"
          sub-title="您可以查看方案详情或导出方案"
        >
          <template #extra>
            <el-button type="primary" @click="viewPlan">查看方案</el-button>
            <el-button @click="exportPlan">导出方案</el-button>
          </template>
        </el-result>
      </div>
    </el-dialog>
    
    <!-- 方案导出对话框 -->
    <el-dialog
      v-model="showExportDialog"
      title="导出招聘方案"
      width="80%"
    >
      <plan-exporter :plan="generatedPlan" />
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import PlanGenerator from '@/components/match/PlanGenerator.vue';
import PlanExporter from '@/components/match/PlanExporter.vue';

export default {
  name: 'PlanGenerationPage',
  components: {
    PlanGenerator,
    PlanExporter
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    // 初始职位ID
    const initialJobId = ref(null);
    
    // 初始候选人
    const initialCandidates = ref([]);
    
    // 生成的方案
    const generatedPlan = ref(null);
    
    // 是否显示成功对话框
    const showSuccessDialog = ref(false);
    
    // 是否显示导出对话框
    const showExportDialog = ref(false);
    
    // 返回列表
    const goBack = () => {
      router.push('/matches');
    };
    
    // 处理方案生成
    const handlePlanGenerated = (plan) => {
      generatedPlan.value = plan;
      showSuccessDialog.value = true;
    };
    
    // 查看方案
    const viewPlan = () => {
      if (!generatedPlan.value) return;
      
      showSuccessDialog.value = false;
      router.push(`/plans/${generatedPlan.value.id}`);
    };
    
    // 导出方案
    const exportPlan = () => {
      if (!generatedPlan.value) return;
      
      showSuccessDialog.value = false;
      showExportDialog.value = true;
    };
    
    // 获取初始数据
    const fetchInitialData = async () => {
      // 从路由参数获取职位ID
      const jobId = route.query.job_id;
      if (jobId) {
        initialJobId.value = parseInt(jobId);
      }
      
      // 从路由参数获取匹配ID
      const matchId = route.query.match_id;
      if (matchId) {
        try {
          // 调用API获取匹配详情
          // const response = await api.getMatchDetail(matchId);
          
          // 模拟API响应
          await new Promise(resolve => setTimeout(resolve, 500));
          const response = {
            data: {
              id: matchId,
              resume_id: 1,
              job_id: initialJobId.value,
              candidate_name: '张三',
              match_score: 85,
              match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
            }
          };
          
          // 添加到初始候选人
          initialCandidates.value = [response.data];
        } catch (error) {
          console.error('获取匹配详情失败:', error);
          ElMessage.error('获取匹配详情失败，请重试');
        }
      }
    };
    
    // 组件挂载时获取初始数据
    onMounted(() => {
      fetchInitialData();
    });
    
    return {
      initialJobId,
      initialCandidates,
      generatedPlan,
      showSuccessDialog,
      showExportDialog,
      goBack,
      handlePlanGenerated,
      viewPlan,
      exportPlan
    };
  }
};
</script>

<style scoped>
.plan-generation-page {
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

.content-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.success-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
