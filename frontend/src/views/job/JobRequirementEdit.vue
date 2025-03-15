<template>
  <div class="job-requirement-edit">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑招聘需求' : '创建招聘需求' }}</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>返回
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="edit-card">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="100px"
        label-position="top"
      >
        <el-form-item label="职位名称" prop="position_name">
          <el-input v-model="formData.position_name" placeholder="请输入职位名称" />
        </el-form-item>

        <el-form-item label="部门" prop="department">
          <el-input v-model="formData.department" placeholder="请输入部门" />
        </el-form-item>

        <el-form-item label="工作职责" prop="responsibilities">
          <el-input
            v-model="formData.responsibilities"
            type="textarea"
            :rows="6"
            placeholder="请输入工作职责"
          />
        </el-form-item>

        <el-form-item label="任职要求" prop="requirements">
          <el-input
            v-model="formData.requirements"
            type="textarea"
            :rows="6"
            placeholder="请输入任职要求"
          />
        </el-form-item>

        <el-form-item label="薪资范围" prop="salary_range">
          <el-input v-model="formData.salary_range" placeholder="例如：15k-25k" />
        </el-form-item>

        <el-form-item label="工作地点" prop="location">
          <el-input v-model="formData.location" placeholder="请输入工作地点" />
        </el-form-item>

        <el-form-item label="技能标签">
          <el-tag
            v-for="(tag, index) in formData.tags"
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
          <el-button type="primary" @click="submitForm" :loading="saving">
            {{ isEdit ? '保存修改' : '创建需求' }}
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, computed, nextTick, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Back } from '@element-plus/icons-vue';
import { getJobRequirement, createJobRequirement, updateJobRequirement } from '@/api/job';

export default {
  name: 'JobRequirementEdit',
  components: {
    Back
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    // 判断是编辑还是创建
    const isEdit = computed(() => route.path.includes('/edit'));
    
    // 数据加载状态
    const loading = ref(false);
    const saving = ref(false);
    
    // 表单数据
    const formRef = ref(null);
    const formData = reactive({
      position_name: '',
      department: '',
      responsibilities: '',
      requirements: '',
      salary_range: '',
      location: '',
      tags: []
    });
    
    // 标签输入
    const inputTagVisible = ref(false);
    const inputTagValue = ref('');
    const tagInputRef = ref(null);
    
    // 表单验证规则
    const rules = {
      position_name: [
        { required: true, message: '请输入职位名称', trigger: 'blur' }
      ],
      responsibilities: [
        { required: true, message: '请输入工作职责', trigger: 'blur' }
      ],
      requirements: [
        { required: true, message: '请输入任职要求', trigger: 'blur' }
      ]
    };
    
    // 加载招聘需求详情
    const loadJobDetail = async () => {
      if (!isEdit.value) return;
      
      const jobId = route.params.id;
      if (!jobId) return;
      
      loading.value = true;
      
      try {
        const response = await getJobRequirement(jobId);
        
        // 填充表单数据
        formData.position_name = response.position_name || '';
        formData.department = response.department || '';
        formData.responsibilities = response.responsibilities || '';
        formData.requirements = response.requirements || '';
        formData.salary_range = response.salary_range || '';
        formData.location = response.location || '';
        formData.tags = response.tags || [];
        
      } catch (error) {
        console.error('获取招聘需求详情失败:', error);
        ElMessage.error('获取招聘需求详情失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 提交表单
    const submitForm = async () => {
      if (!formRef.value) return;
      
      try {
        await formRef.value.validate();
        
        saving.value = true;
        
        try {
          if (isEdit.value) {
            // 更新招聘需求
            await updateJobRequirement(route.params.id, formData);
            ElMessage.success('招聘需求更新成功');
          } else {
            // 创建招聘需求
            await createJobRequirement(formData);
            ElMessage.success('招聘需求创建成功');
          }
          
          // 返回列表页
          router.push('/jobs');
          
        } catch (error) {
          console.error('保存招聘需求失败:', error);
          ElMessage.error('保存招聘需求失败，请重试');
        } finally {
          saving.value = false;
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
      
      if (isEdit.value) {
        // 如果是编辑模式，重新加载数据
        loadJobDetail();
      } else {
        // 如果是创建模式，清空表单
        formData.position_name = '';
        formData.department = '';
        formData.responsibilities = '';
        formData.requirements = '';
        formData.salary_range = '';
        formData.location = '';
        formData.tags = [];
      }
    };
    
    // 返回列表
    const goBack = () => {
      router.push('/jobs');
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
        if (!formData.tags) {
          formData.tags = [];
        }
        formData.tags.push(inputTagValue.value);
      }
      inputTagVisible.value = false;
      inputTagValue.value = '';
    };
    
    // 移除标签
    const removeTag = (index) => {
      formData.tags.splice(index, 1);
    };
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadJobDetail();
    });
    
    return {
      isEdit,
      loading,
      saving,
      formRef,
      formData,
      rules,
      inputTagVisible,
      inputTagValue,
      tagInputRef,
      submitForm,
      resetForm,
      goBack,
      showTagInput,
      addTag,
      removeTag
    };
  }
};
</script>

<style scoped>
.job-requirement-edit {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.edit-card {
  margin-bottom: 20px;
}

.tag-item {
  margin-right: 8px;
  margin-bottom: 8px;
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
