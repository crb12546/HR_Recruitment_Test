<template>
  <div class="job-upload-page">
    <div class="page-header">
      <h2>上传招聘需求</h2>
      <p class="description">上传招聘需求文档，系统将自动解析职位信息</p>
    </div>
    
    <div class="content-container">
      <!-- 左侧：表单区域 -->
      <div class="form-container">
        <job-requirement-form @job-saved="handleJobSaved" />
      </div>
      
      <!-- 右侧：原始文档预览 -->
      <div class="preview-container" v-if="previewUrl">
        <h3>原始文档预览</h3>
        <div class="document-preview">
          <iframe :src="previewUrl" class="preview-frame"></iframe>
        </div>
      </div>
      <div class="preview-container empty" v-else>
        <el-empty description="暂无文档预览" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import JobRequirementForm from '@/components/job/JobRequirementForm.vue';

export default {
  name: 'JobUpload',
  components: {
    JobRequirementForm
  },
  setup() {
    // 文档预览URL
    const previewUrl = ref('');
    
    // 处理文件上传
    const handleFileUploaded = (file) => {
      if (file) {
        // 创建文件预览URL
        previewUrl.value = URL.createObjectURL(file);
      }
    };
    
    // 处理职位保存
    const handleJobSaved = () => {
      ElMessage.success('招聘需求保存成功');
      // 清空预览
      if (previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value);
        previewUrl.value = '';
      }
    };
    
    return {
      previewUrl,
      handleFileUploaded,
      handleJobSaved
    };
  }
};
</script>

<style scoped>
.job-upload-page {
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

.content-container {
  display: flex;
  flex: 1;
  gap: 20px;
  min-height: 500px;
}

.form-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.preview-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.preview-container h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.document-preview {
  flex: 1;
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  overflow: hidden;
}

.preview-frame {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-container.empty {
  justify-content: center;
  align-items: center;
}
</style>
