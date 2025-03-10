<template>
  <div class="resume-upload">
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
      <!-- 文件上传区域 -->
      <el-form-item label="简历文件" prop="file">
        <el-upload
          class="upload-area"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          :file-list="fileList"
          :accept="acceptFileTypes"
        >
          <el-icon class="upload-icon"><Upload /></el-icon>
          <div class="upload-text">
            <span>拖拽文件到此处或点击上传</span>
            <p>支持 .pdf, .doc, .docx 格式文件</p>
          </div>
        </el-upload>
      </el-form-item>

      <!-- 候选人基本信息 -->
      <el-form-item label="候选人姓名" prop="candidateName">
        <el-input v-model="formData.candidateName" placeholder="请输入候选人姓名" />
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="loading">解析简历</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 解析结果展示 -->
    <div v-if="parseResult" class="parse-result">
      <h3>解析结果</h3>
      <el-form label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="parseResult.name" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="parseResult.phone" />
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input v-model="parseResult.email" />
        </el-form-item>
        <el-form-item label="最高学历">
          <el-select v-model="parseResult.education" placeholder="请选择">
            <el-option label="博士" value="博士" />
            <el-option label="硕士" value="硕士" />
            <el-option label="本科" value="本科" />
            <el-option label="大专" value="大专" />
            <el-option label="高中及以下" value="高中及以下" />
          </el-select>
        </el-form-item>
        <el-form-item label="工作经验">
          <el-input v-model="parseResult.experience" placeholder="例如：3年" />
        </el-form-item>
        <el-form-item label="技能标签">
          <el-tag
            v-for="(tag, index) in parseResult.skills"
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
        <el-form-item label="工作经历">
          <el-input type="textarea" v-model="parseResult.workHistory" :rows="4" />
        </el-form-item>
        <el-form-item label="教育经历">
          <el-input type="textarea" v-model="parseResult.educationHistory" :rows="4" />
        </el-form-item>
        <el-form-item label="自我评价">
          <el-input type="textarea" v-model="parseResult.selfEvaluation" :rows="3" />
        </el-form-item>
        <el-form-item label="人才画像">
          <el-input type="textarea" v-model="parseResult.talentPortrait" :rows="4" disabled />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveResume" :loading="savingResume">保存简历</el-button>
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
  name: 'ResumeUpload',
  setup() {
    // 表单数据
    const formRef = ref(null);
    const formData = reactive({
      file: null,
      candidateName: ''
    });
    
    // 文件列表
    const fileList = ref([]);
    
    // 加载状态
    const loading = ref(false);
    const savingResume = ref(false);
    
    // 解析结果
    const parseResult = ref(null);
    
    // 标签输入
    const inputTagVisible = ref(false);
    const inputTagValue = ref('');
    const tagInputRef = ref(null);
    
    // 接受的文件类型
    const acceptFileTypes = '.pdf,.doc,.docx';
    
    // 表单验证规则
    const rules = {
      file: [
        { required: true, message: '请上传简历文件', trigger: 'change' }
      ],
      candidateName: [
        { required: true, message: '请输入候选人姓名', trigger: 'blur' }
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
          ElMessage.warning('请上传简历文件');
          return;
        }
        
        // 开始解析
        loading.value = true;
        
        // 创建表单数据
        const formDataToSend = new FormData();
        formDataToSend.append('file', formData.file);
        formDataToSend.append('candidate_name', formData.candidateName);
        
        try {
          // 调用API解析简历
          // const response = await api.parseResume(formDataToSend);
          
          // 模拟API响应
          await new Promise(resolve => setTimeout(resolve, 1500));
          const response = {
            data: {
              name: formData.candidateName || '张三',
              phone: '13800138000',
              email: 'zhangsan@example.com',
              education: '本科',
              experience: '3年',
              skills: ['Java', 'Spring Boot', 'MySQL', '微服务'],
              workHistory: '2020-至今 ABC科技有限公司 后端开发工程师\n2018-2020 XYZ科技有限公司 Java开发工程师',
              educationHistory: '2014-2018 某大学 计算机科学与技术 本科',
              selfEvaluation: '热爱编程，善于解决问题，具有良好的团队协作能力。',
              talentPortrait: '该候选人是一名有3年经验的Java后端开发工程师，熟悉Spring Boot和微服务架构，具有扎实的MySQL数据库知识。工作经历表明其有持续学习的能力和稳定的职业发展轨迹。'
            }
          };
          
          // 设置解析结果
          parseResult.value = response.data;
          
          ElMessage.success('简历解析成功');
        } catch (error) {
          console.error('解析简历失败:', error);
          ElMessage.error('解析简历失败，请重试');
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
        if (!parseResult.value.skills) {
          parseResult.value.skills = [];
        }
        parseResult.value.skills.push(inputTagValue.value);
      }
      inputTagVisible.value = false;
      inputTagValue.value = '';
    };
    
    // 移除标签
    const removeTag = (index) => {
      parseResult.value.skills.splice(index, 1);
    };
    
    // 保存简历
    const saveResume = async () => {
      if (!parseResult.value) return;
      
      savingResume.value = true;
      
      try {
        // 调用API保存简历
        // const response = await api.saveResume(parseResult.value);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        ElMessage.success('简历保存成功');
        
        // 重置表单
        resetForm();
      } catch (error) {
        console.error('保存简历失败:', error);
        ElMessage.error('保存简历失败，请重试');
      } finally {
        savingResume.value = false;
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
      savingResume,
      parseResult,
      rules,
      acceptFileTypes,
      handleFileChange,
      submitForm,
      resetForm,
      inputTagVisible,
      inputTagValue,
      tagInputRef,
      showTagInput,
      addTag,
      removeTag,
      saveResume,
      cancelEdit
    };
  }
};
</script>

<style scoped>
.resume-upload {
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
