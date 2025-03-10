<template>
  <div class="match-detail-page">
    <div class="page-header">
      <h2>匹配详情</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          返回列表
        </el-button>
      </div>
    </div>
    
    <div class="content-container">
      <match-detail 
        :match-id="matchId" 
        @view-resume="handleViewResume"
        @view-job="handleViewJob"
        @add-to-plan="handleAddToPlan"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import MatchDetail from '@/components/match/MatchDetail.vue';

export default {
  name: 'MatchDetailPage',
  components: {
    MatchDetail
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    // 匹配ID
    const matchId = ref(null);
    
    // 返回列表
    const goBack = () => {
      router.push('/matches');
    };
    
    // 处理查看简历
    const handleViewResume = (resumeId) => {
      router.push(`/resumes/${resumeId}`);
    };
    
    // 处理查看职位
    const handleViewJob = (jobId) => {
      router.push(`/jobs/${jobId}`);
    };
    
    // 处理添加到方案
    const handleAddToPlan = (match) => {
      router.push({
        path: '/plans/create',
        query: {
          job_id: match.job_id,
          match_id: match.id
        }
      });
    };
    
    // 组件挂载时获取匹配ID
    onMounted(() => {
      matchId.value = route.params.id;
    });
    
    return {
      matchId,
      goBack,
      handleViewResume,
      handleViewJob,
      handleAddToPlan
    };
  }
};
</script>

<style scoped>
.match-detail-page {
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
</style>
