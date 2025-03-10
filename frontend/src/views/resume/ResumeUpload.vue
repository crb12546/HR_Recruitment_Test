<template>
  <div class="resume-upload-page">
    <div class="page-header">
      <h2>上传简历</h2>
      <p class="description">上传候选人简历，系统将自动解析简历信息</p>
    </div>
    
    <div class="content-container">
      <!-- 左侧：表单区域 -->
      <div class="form-container">
        <resume-upload @resume-saved="handleResumeSaved" />
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
import ResumeUpload from '@/components/resume/ResumeUpload.vue';

export default {
  name: 'ResumeUploadPage',
  components: {
    ResumeUpload
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
    
    // 处理简历保存
    const handleResumeSaved = () => {
      ElMessage.success('简历保存成功');
      // 清空预览
      if (previewUrl.value) {
        URL.revokeObjectURL(previewUrl.value);
        previewUrl.value = '';
      }
    };
    
    return {
      previewUrl,
      handleFileUploaded,
      handleResumeSaved
    };
  }
};
</script>

<style scoped>
.resume-upload-page {
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
