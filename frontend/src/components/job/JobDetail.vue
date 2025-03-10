<template>
  <div class="job-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!job" class="empty-container">
      <el-empty description="请选择一个职位查看详情" />
    </div>
    
    <div v-else class="detail-container">
      <!-- 标题和操作按钮 -->
      <div class="header">
        <h2 class="title">{{ job.position_name }}</h2>
        <div class="actions">
          <el-button type="primary" @click="handleEdit">编辑</el-button>
          <el-button type="success" @click="handleMatch">匹配简历</el-button>
          <el-button type="danger" @click="handleDelete">删除</el-button>
        </div>
      </div>
      
      <!-- 基本信息 -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="部门">{{ job.department }}</el-descriptions-item>
        <el-descriptions-item label="工作地点">{{ job.location }}</el-descriptions-item>
        <el-descriptions-item label="薪资范围">{{ job.salary_range }}</el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ formatDate(job.created_at) }}</el-descriptions-item>
      </el-descriptions>
      
      <!-- 标签 -->
      <div class="tags-container">
        <h3>技能标签</h3>
        <div class="tags">
          <el-tag
            v-for="(tag, index) in job.tags"
            :key="index"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
      
      <!-- 工作职责 -->
      <div class="section">
        <h3>工作职责</h3>
        <div class="content">
          <p v-if="!job.responsibilities">暂无工作职责</p>
          <p v-else>{{ job.responsibilities }}</p>
        </div>
      </div>
      
      <!-- 任职要求 -->
      <div class="section">
        <h3>任职要求</h3>
        <div class="content">
          <p v-if="!job.requirements">暂无任职要求</p>
          <div v-else>
            <p v-for="(item, index) in formatRequirements(job.requirements)" :key="index">
              {{ item }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- 匹配简历 -->
      <div v-if="matchedResumes.length > 0" class="section">
        <h3>匹配简历</h3>
        <el-table :data="matchedResumes" style="width: 100%">
          <el-table-column prop="candidate_name" label="候选人" width="120" />
          <el-table-column prop="match_score" label="匹配度" width="100">
            <template #default="scope">
              <el-progress
                :percentage="scope.row.match_score"
                :color="getMatchScoreColor(scope.row.match_score)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="match_explanation" label="匹配说明" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="viewResume(scope.row)"
              >
                查看简历
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    
    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <span>确定要删除该招聘需求吗？此操作不可恢复。</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete" :loading="deleting">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 编辑对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑招聘需求"
      width="60%"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="职位名称">
          <el-input v-model="editForm.position_name" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="editForm.department" />
        </el-form-item>
        <el-form-item label="工作职责">
          <el-input type="textarea" v-model="editForm.responsibilities" :rows="4" />
        </el-form-item>
        <el-form-item label="任职要求">
          <el-input type="textarea" v-model="editForm.requirements" :rows="4" />
        </el-form-item>
        <el-form-item label="薪资范围">
          <el-input v-model="editForm.salary_range" />
        </el-form-item>
        <el-form-item label="工作地点">
          <el-input v-model="editForm.location" />
        </el-form-item>
        <el-form-item label="技能标签">
          <el-tag
            v-for="(tag, index) in editForm.tags"
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
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveEdit" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, nextTick, watch } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'JobDetail',
  props: {
    jobId: {
      type: [Number, String],
      default: null
    }
  },
  emits: ['refresh', 'view-resume'],
  setup(props, { emit }) {
    // 职位详情
    const job = ref(null);
    
    // 加载状态
    const loading = ref(false);
    const deleting = ref(false);
    const saving = ref(false);
    
    // 删除对话框
    const deleteDialogVisible = ref(false);
    
    // 编辑对话框
    const editDialogVisible = ref(false);
    const editForm = reactive({
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
    
    // 匹配的简历
    const matchedResumes = ref([]);
    
    // 获取职位详情
    const fetchJobDetail = async () => {
      if (!props.jobId) {
        job.value = null;
        return;
      }
      
      loading.value = true;
      
      try {
        // 调用API获取职位详情
        // const response = await api.getJobDetail(props.jobId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            id: props.jobId,
            position_name: '前端开发工程师',
            department: '技术部',
            responsibilities: '负责公司产品的前端开发，包括页面设计和实现，确保良好的用户体验。',
            requirements: '1. 熟练掌握HTML、CSS、JavaScript等前端技术\n2. 熟悉Vue.js或React等前端框架\n3. 具有良好的团队协作能力',
            salary_range: '15k-25k',
            location: '北京',
            tags: ['前端', 'Vue.js', 'JavaScript'],
            created_at: '2025-03-01T10:00:00Z',
            updated_at: '2025-03-01T10:00:00Z'
          }
        };
        
        // 设置职位详情
        job.value = response.data;
        
        // 获取匹配的简历
        fetchMatchedResumes();
      } catch (error) {
        console.error('获取职位详情失败:', error);
        ElMessage.error('获取职位详情失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 获取匹配的简历
    const fetchMatchedResumes = async () => {
      if (!props.jobId) return;
      
      try {
        // 调用API获取匹配的简历
        // const response = await api.getMatchedResumes(props.jobId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: [
            {
              id: 1,
              resume_id: 101,
              candidate_name: '张三',
              match_score: 85,
              match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
            },
            {
              id: 2,
              resume_id: 102,
              candidate_name: '李四',
              match_score: 70,
              match_explanation: '候选人具备基本技能要求，但工作经验略显不足。'
            }
          ]
        };
        
        // 设置匹配的简历
        matchedResumes.value = response.data;
      } catch (error) {
        console.error('获取匹配简历失败:', error);
        ElMessage.error('获取匹配简历失败，请重试');
      }
    };
    
    // 处理编辑
    const handleEdit = () => {
      if (!job.value) return;
      
      // 复制职位信息到编辑表单
      Object.keys(editForm).forEach(key => {
        if (key in job.value) {
          if (key === 'tags') {
            editForm.tags = [...job.value.tags];
          } else {
            editForm[key] = job.value[key];
          }
        }
      });
      
      // 显示编辑对话框
      editDialogVisible.value = true;
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
        editForm.tags.push(inputTagValue.value);
      }
      inputTagVisible.value = false;
      inputTagValue.value = '';
    };
    
    // 移除标签
    const removeTag = (index) => {
      editForm.tags.splice(index, 1);
    };
    
    // 保存编辑
    const saveEdit = async () => {
      saving.value = true;
      
      try {
        // 调用API保存编辑
        // await api.updateJob(props.jobId, editForm);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        
        ElMessage.success('保存成功');
        
        // 关闭对话框
        editDialogVisible.value = false;
        
        // 重新获取职位详情
        fetchJobDetail();
        
        // 通知父组件刷新列表
        emit('refresh');
      } catch (error) {
        console.error('保存失败:', error);
        ElMessage.error('保存失败，请重试');
      } finally {
        saving.value = false;
      }
    };
    
    // 处理匹配简历
    const handleMatch = () => {
      if (!job.value) return;
      
      // 跳转到匹配简历页面
      // router.push(`/jobs/${job.value.id}/match`);
      
      // 或者显示匹配简历对话框
      ElMessage.info('正在跳转到简历匹配页面...');
    };
    
    // 处理删除
    const handleDelete = () => {
      if (!job.value) return;
      
      deleteDialogVisible.value = true;
    };
    
    // 确认删除
    const confirmDelete = async () => {
      if (!job.value) return;
      
      deleting.value = true;
      
      try {
        // 调用API删除职位
        // await api.deleteJob(job.value.id);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        
        ElMessage.success('删除成功');
        
        // 关闭对话框
        deleteDialogVisible.value = false;
        
        // 清空职位详情
        job.value = null;
        
        // 通知父组件刷新列表
        emit('refresh');
      } catch (error) {
        console.error('删除失败:', error);
        ElMessage.error('删除失败，请重试');
      } finally {
        deleting.value = false;
      }
    };
    
    // 查看简历
    const viewResume = (matchedResume) => {
      emit('view-resume', matchedResume.resume_id);
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 格式化任职要求
    const formatRequirements = (requirements) => {
      if (!requirements) return [];
      
      // 如果已经是列表形式，直接返回
      if (requirements.includes('\n')) {
        return requirements.split('\n');
      }
      
      // 否则尝试按数字分割
      const matches = requirements.match(/\d+\.\s+[^0-9]+/g);
      if (matches && matches.length > 0) {
        return matches;
      }
      
      // 如果没有明确的分隔符，直接返回原文本
      return [requirements];
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 监听jobId变化
    watch(() => props.jobId, (newVal) => {
      if (newVal) {
        fetchJobDetail();
      } else {
        job.value = null;
      }
    }, { immediate: true });
    
    return {
      job,
      loading,
      deleting,
      saving,
      deleteDialogVisible,
      editDialogVisible,
      editForm,
      inputTagVisible,
      inputTagValue,
      tagInputRef,
      matchedResumes,
      handleEdit,
      showTagInput,
      addTag,
      removeTag,
      saveEdit,
      handleMatch,
      handleDelete,
      confirmDelete,
      viewResume,
      formatDate,
      formatRequirements,
      getMatchScoreColor
    };
  }
};
</script>

<style scoped>
.job-detail {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.loading-container, .empty-container {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.actions {
  display: flex;
  gap: 10px;
}

.tags-container {
  margin: 20px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  margin-right: 5px;
  margin-bottom: 5px;
}

.section {
  margin: 20px 0;
}

.section h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.content {
  color: #606266;
  line-height: 1.6;
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
