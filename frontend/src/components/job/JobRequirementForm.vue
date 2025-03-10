<template>
  <div class="job-requirement-form">
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
      <!-- 文件上传区域 -->
      <el-form-item label="需求文档" prop="file">
        <el-upload
          class="upload-area"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          :file-list="fileList"
        >
          <el-icon class="upload-icon"><Upload /></el-icon>
          <div class="upload-text">
            <span>拖拽文件到此处或点击上传</span>
            <p>支持 .doc, .docx, .pdf 格式文件</p>
          </div>
        </el-upload>
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">解析需求</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 解析结果展示 -->
    <div v-if="parseResult" class="parse-result">
      <h3>解析结果</h3>
      <el-form label-width="100px">
        <el-form-item label="职位名称">
          <el-input v-model="parseResult.position_name" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="parseResult.department" />
        </el-form-item>
        <el-form-item label="工作职责">
          <el-input type="textarea" v-model="parseResult.responsibilities" :rows="4" />
        </el-form-item>
        <el-form-item label="任职要求">
          <el-input type="textarea" v-model="parseResult.requirements" :rows="4" />
        </el-form-item>
        <el-form-item label="薪资范围">
          <el-input v-model="parseResult.salary_range" />
        </el-form-item>
        <el-form-item label="工作地点">
          <el-input v-model="parseResult.location" />
        </el-form-item>
        <el-form-item label="技能标签">
          <el-tag
            v-for="(tag, index) in parseResult.tags"
            :key="index"
            class="tag-item"
            closable
            @close="removeTag(index)"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputTagVisible"
            ref="tagInputRef"
            v-model="inputTagValue"
            class="tag-input"
            size="small"
            @keyup.enter="addTag"
            @blur="addTag"
          />
          <el-button v-else class="button-new-tag" size="small" @click="showTagInput">
            + 添加标签
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveJobRequirement" :loading="savingJob">保存需求</el-button>
          <el-button @click="cancelEdit">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, nextTick } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'JobRequirementForm',
  setup() {
    // 表单数据
    const formRef = ref(null);
    const formData = reactive({
      file: null
    });
    
    // 文件列表
    const fileList = ref([]);
    
    // 加载状态
    const loading = ref(false);
    const savingJob = ref(false);
    
    // 解析结果
    const parseResult = ref(null);
    
    // 标签输入
    const inputTagVisible = ref(false);
    const inputTagValue = ref('');
    const tagInputRef = ref(null);
    
    // 表单验证规则
    const rules = {
      file: [
        { required: true, message: '请上传需求文档', trigger: 'change' }
      ]
    };
    
    // 处理文件变更
    const handleFileChange = (file) => {
      formData.file = file.raw;
      fileList.value = [file];
    };
    
    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return;
      
      try {
        await formRef.value.validate();
        
        if (!formData.file) {
          ElMessage.warning('请上传需求文档');
          return;
        }
        
        // 开始解析
        loading.value = true;
        
        // 创建表单数据
        const formDataToSend = new FormData();
        formDataToSend.append('file', formData.file);
        
        try {
          // 调用API解析文档
          // const response = await api.parseJobRequirement(formDataToSend);
          
          // 模拟API响应
          await new Promise(resolve => setTimeout(resolve, 1500));
          const response = {
            data: {
              position_name: '前端开发工程师',
              department: '技术部',
              responsibilities: '负责公司产品的前端开发，包括页面设计和实现，确保良好的用户体验。',
              requirements: '1. 熟练掌握HTML、CSS、JavaScript等前端技术\n2. 熟悉Vue.js或React等前端框架\n3. 具有良好的团队协作能力',
              salary_range: '15k-25k',
              location: '北京',
              tags: ['前端', 'Vue.js', 'JavaScript']
            }
          };
          
          // 设置解析结果
          parseResult.value = response.data;
          
          ElMessage.success('需求解析成功');
        } catch (error) {
          console.error('解析需求文档失败:', error);
          ElMessage.error('解析需求文档失败，请重试');
        } finally {
          loading.value = false;
        }
      } catch (error) {
        console.error('表单验证失败:', error);
      }
    };
    
    // 重置表单
    const resetForm = () => {
      if (formRef.value) {
        formRef.value.resetFields();
      }
      fileList.value = [];
      parseResult.value = null;
    };
    
    // 显示标签输入框
    const showTagInput = () => {
      inputTagVisible.value = true;
      nextTick(() => {
        tagInputRef.value.focus();
      });
    };
    
    // 添加标签
    const addTag = () => {
      if (inputTagValue.value) {
        if (!parseResult.value.tags) {
          parseResult.value.tags = [];
        }
        parseResult.value.tags.push(inputTagValue.value);
      }
      inputTagVisible.value = false;
      inputTagValue.value = '';
    };
    
    // 移除标签
    const removeTag = (index) => {
      parseResult.value.tags.splice(index, 1);
    };
    
    // 保存招聘需求
    const saveJobRequirement = async () => {
      if (!parseResult.value) return;
      
      savingJob.value = true;
      
      try {
        // 调用API保存招聘需求
        // const response = await api.saveJobRequirement(parseResult.value);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        ElMessage.success('招聘需求保存成功');
        
        // 重置表单
        resetForm();
      } catch (error) {
        console.error('保存招聘需求失败:', error);
        ElMessage.error('保存招聘需求失败，请重试');
      } finally {
        savingJob.value = false;
      }
    };
    
    // 取消编辑
    const cancelEdit = () => {
      parseResult.value = null;
    };
    
    return {
      formRef,
      formData,
      fileList,
      loading,
      savingJob,
      parseResult,
      rules,
      handleFileChange,
      submitForm,
      resetForm,
      inputTagVisible,
      inputTagValue,
      tagInputRef,
      showTagInput,
      addTag,
      removeTag,
      saveJobRequirement,
      cancelEdit
    };
  }
};
</script>

<style scoped>
.job-requirement-form {
  padding: 20px;
}

.upload-area {
  width: 100%;
}

.upload-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 10px;
}

.upload-text {
  color: #606266;
}

.parse-result {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px dashed #dcdfe6;
}

.tag-item {
  margin-right: 10px;
  margin-bottom: 10px;
}

.tag-input {
  width: 100px;
  margin-right: 10px;
  vertical-align: bottom;
}

.button-new-tag {
  margin-bottom: 10px;
}
</style>
