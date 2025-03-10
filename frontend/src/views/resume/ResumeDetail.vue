<template>
  <div class="resume-detail-page">
    <div class="page-header">
      <h2>简历详情</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>
          返回列表
        </el-button>
      </div>
    </div>
    
    <div class="content-container">
      <resume-detail 
        :resume-id="resumeId" 
        @view-job="handleViewJob"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ResumeDetail from '@/components/resume/ResumeDetail.vue';

export default {
  name: 'ResumeDetailPage',
  components: {
    ResumeDetail
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    // 简历ID
    const resumeId = ref(null);
    
    // 返回列表
    const goBack = () => {
      router.push('/resumes');
    };
    
    // 处理查看职位
    const handleViewJob = (jobId) => {
      router.push(`/jobs/${jobId}`);
    };
    
    // 组件挂载时获取简历ID
    onMounted(() => {
      resumeId.value = route.params.id;
    });
    
    return {
      resumeId,
      goBack,
      handleViewJob
    };
  }
};
</script>

<style scoped>
.resume-detail-page {
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
