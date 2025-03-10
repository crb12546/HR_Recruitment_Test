<template>
  <div class="job-list-page">
    <div class="page-header">
      <h2>招聘需求列表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="goToUpload">
          <el-icon><Plus /></el-icon>
          添加需求
        </el-button>
      </div>
    </div>
    
    <div class="content-container">
      <!-- 左侧：职位列表 -->
      <div class="list-container">
        <job-list @select-job="handleSelectJob" ref="jobListRef" />
      </div>
      
      <!-- 右侧：职位详情 -->
      <div class="detail-container">
        <job-detail 
          :job-id="selectedJobId" 
          @refresh="refreshJobList"
          @view-resume="handleViewResume"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import JobList from '@/components/job/JobList.vue';
import JobDetail from '@/components/job/JobDetail.vue';

export default {
  name: 'JobListPage',
  components: {
    JobList,
    JobDetail
  },
  setup() {
    const router = useRouter();
    
    // 选中的职位ID
    const selectedJobId = ref(null);
    
    // 职位列表组件引用
    const jobListRef = ref(null);
    
    // 处理选择职位
    const handleSelectJob = (job) => {
      selectedJobId.value = job.id;
    };
    
    // 刷新职位列表
    const refreshJobList = () => {
      if (jobListRef.value) {
        jobListRef.value.fetchJobList();
      }
    };
    
    // 跳转到上传页面
    const goToUpload = () => {
      router.push('/jobs/upload');
    };
    
    // 处理查看简历
    const handleViewResume = (resumeId) => {
      router.push(`/resumes/${resumeId}`);
    };
    
    return {
      selectedJobId,
      jobListRef,
      handleSelectJob,
      refreshJobList,
      goToUpload,
      handleViewResume
    };
  }
};
</script>

<style scoped>
.job-list-page {
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
  display: flex;
  flex: 1;
  gap: 20px;
  min-height: 500px;
}

.list-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>
