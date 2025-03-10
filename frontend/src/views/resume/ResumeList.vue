<template>
  <div class="resume-list-page">
    <div class="page-header">
      <h2>简历列表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="goToUpload">
          <el-icon><Plus /></el-icon>
          上传简历
        </el-button>
      </div>
    </div>
    
    <!-- 筛选区域 -->
    <div class="filter-container">
      <resume-filter @filter-change="handleFilterChange" />
    </div>
    
    <div class="content-container">
      <!-- 左侧：简历列表 -->
      <div class="list-container">
        <resume-list @select-resume="handleSelectResume" ref="resumeListRef" />
      </div>
      
      <!-- 右侧：简历详情 -->
      <div class="detail-container">
        <resume-detail 
          :resume-id="selectedResumeId" 
          @refresh="refreshResumeList"
          @view-job="handleViewJob"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ResumeList from '@/components/resume/ResumeList.vue';
import ResumeDetail from '@/components/resume/ResumeDetail.vue';
import ResumeFilter from '@/components/resume/ResumeFilter.vue';

export default {
  name: 'ResumeListPage',
  components: {
    ResumeList,
    ResumeDetail,
    ResumeFilter
  },
  setup() {
    const router = useRouter();
    
    // 选中的简历ID
    const selectedResumeId = ref(null);
    
    // 简历列表组件引用
    const resumeListRef = ref(null);
    
    // 处理选择简历
    const handleSelectResume = (resume) => {
      selectedResumeId.value = resume.id;
    };
    
    // 刷新简历列表
    const refreshResumeList = () => {
      if (resumeListRef.value) {
        resumeListRef.value.fetchResumeList();
      }
    };
    
    // 跳转到上传页面
    const goToUpload = () => {
      router.push('/resumes/upload');
    };
    
    // 处理查看职位
    const handleViewJob = (jobId) => {
      router.push(`/jobs/${jobId}`);
    };
    
    // 处理筛选变化
    const handleFilterChange = (filters) => {
      if (resumeListRef.value) {
        // 将筛选条件传递给简历列表组件
        resumeListRef.value.applyFilters(filters);
      }
    };
    
    return {
      selectedResumeId,
      resumeListRef,
      handleSelectResume,
      refreshResumeList,
      goToUpload,
      handleViewJob,
      handleFilterChange
    };
  }
};
</script>

<style scoped>
.resume-list-page {
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

.filter-container {
  margin-bottom: 20px;
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
