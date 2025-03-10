<template>
  <div class="resume-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!resume" class="empty-container">
      <el-empty description="请选择一个简历查看详情" />
    </div>
    
    <div v-else class="detail-container">
      <!-- 标题和操作按钮 -->
      <div class="header">
        <h2 class="title">{{ resume.candidate_name }}</h2>
        <div class="actions">
          <el-button type="primary" @click="handleEdit">编辑</el-button>
          <el-button type="success" @click="handleMatch">匹配职位</el-button>
          <el-button type="danger" @click="handleDelete">删除</el-button>
        </div>
      </div>
      
      <!-- 基本信息 -->
      <el-descriptions :column="2" border>
        <el-descriptions-item label="联系电话">{{ resume.phone }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ resume.email }}</el-descriptions-item>
        <el-descriptions-item label="最高学历">{{ resume.education }}</el-descriptions-item>
        <el-descriptions-item label="工作经验">{{ resume.experience }}</el-descriptions-item>
      </el-descriptions>
      
      <!-- 标签 -->
      <div class="tags-container">
        <h3>技能标签</h3>
        <div class="tags">
          <el-tag
            v-for="(tag, index) in resume.skills"
            :key="index"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
      
      <!-- 工作经历 -->
      <div class="section">
        <h3>工作经历</h3>
        <div class="content">
          <p v-if="!resume.workHistory">暂无工作经历</p>
          <div v-else>
            <p v-for="(item, index) in formatWorkHistory(resume.workHistory)" :key="index">
              {{ item }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- 教育经历 -->
      <div class="section">
        <h3>教育经历</h3>
        <div class="content">
          <p v-if="!resume.educationHistory">暂无教育经历</p>
          <div v-else>
            <p v-for="(item, index) in formatEducationHistory(resume.educationHistory)" :key="index">
              {{ item }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- 自我评价 -->
      <div class="section">
        <h3>自我评价</h3>
        <div class="content">
          <p v-if="!resume.selfEvaluation">暂无自我评价</p>
          <p v-else>{{ resume.selfEvaluation }}</p>
        </div>
      </div>
      
      <!-- 人才画像 -->
      <div class="section">
        <h3>人才画像</h3>
        <div class="content">
          <p v-if="!resume.talentPortrait">暂无人才画像</p>
          <p v-else>{{ resume.talentPortrait }}</p>
        </div>
      </div>
      
      <!-- 匹配职位 -->
      <div v-if="matchedJobs.length > 0" class="section">
        <h3>匹配职位</h3>
        <el-table :data="matchedJobs" style="width: 100%">
          <el-table-column prop="position_name" label="职位名称" width="150" />
          <el-table-column prop="department" label="部门" width="120" />
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
                @click="viewJob(scope.row)"
              >
                查看职位
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
      <span>确定要删除该简历吗？此操作不可恢复。</span>
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
      title="编辑简历"
      width="60%"
    >
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="候选人姓名">
          <el-input v-model="editForm.candidate_name" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="最高学历">
          <el-select v-model="editForm.education" placeholder="请选择">
            <el-option label="博士" value="博士" />
            <el-option label="硕士" value="硕士" />
            <el-option label="本科" value="本科" />
            <el-option label="大专" value="大专" />
            <el-option label="高中及以下" value="高中及以下" />
          </el-select>
        </el-form-item>
        <el-form-item label="工作经验">
          <el-input v-model="editForm.experience" />
        </el-form-item>
        <el-form-item label="技能标签">
          <el-tag
            v-for="(tag, index) in editForm.skills"
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
          <el-input type="textarea" v-model="editForm.workHistory" :rows="4" />
        </el-form-item>
        <el-form-item label="教育经历">
          <el-input type="textarea" v-model="editForm.educationHistory" :rows="4" />
        </el-form-item>
        <el-form-item label="自我评价">
          <el-input type="textarea" v-model="editForm.selfEvaluation" :rows="3" />
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
  name: 'ResumeDetail',
  props: {
    resumeId: {
      type: [Number, String],
      default: null
    }
  },
  emits: ['refresh', 'view-job'],
  setup(props, { emit }) {
    // 简历详情
    const resume = ref(null);
    
    // 加载状态
    const loading = ref(false);
    const deleting = ref(false);
    const saving = ref(false);
    
    // 删除对话框
    const deleteDialogVisible = ref(false);
    
    // 编辑对话框
    const editDialogVisible = ref(false);
    const editForm = reactive({
      candidate_name: '',
      phone: '',
      email: '',
      education: '',
      experience: '',
      skills: [],
      workHistory: '',
      educationHistory: '',
      selfEvaluation: ''
    });
    
    // 标签输入
    const inputTagVisible = ref(false);
    const inputTagValue = ref('');
    const tagInputRef = ref(null);
    
    // 匹配的职位
    const matchedJobs = ref([]);
    
    // 获取简历详情
    const fetchResumeDetail = async () => {
      if (!props.resumeId) {
        resume.value = null;
        return;
      }
      
      loading.value = true;
      
      try {
        // 调用API获取简历详情
        // const response = await api.getResumeDetail(props.resumeId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            id: props.resumeId,
            candidate_name: '张三',
            phone: '13800138000',
            email: 'zhangsan@example.com',
            education: '本科',
            experience: '3年',
            skills: ['Java', 'Spring Boot', 'MySQL', '微服务'],
            workHistory: '2020-至今 ABC科技有限公司 后端开发工程师\n2018-2020 XYZ科技有限公司 Java开发工程师',
            educationHistory: '2014-2018 某大学 计算机科学与技术 本科',
            selfEvaluation: '热爱编程，善于解决问题，具有良好的团队协作能力。',
            talentPortrait: '该候选人是一名有3年经验的Java后端开发工程师，熟悉Spring Boot和微服务架构，具有扎实的MySQL数据库知识。工作经历表明其有持续学习的能力和稳定的职业发展轨迹。',
            created_at: '2025-03-01T10:00:00Z',
            updated_at: '2025-03-01T10:00:00Z'
          }
        };
        
        // 设置简历详情
        resume.value = response.data;
        
        // 获取匹配的职位
        fetchMatchedJobs();
      } catch (error) {
        console.error('获取简历详情失败:', error);
        ElMessage.error('获取简历详情失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 获取匹配的职位
    const fetchMatchedJobs = async () => {
      if (!props.resumeId) return;
      
      try {
        // 调用API获取匹配的职位
        // const response = await api.getMatchedJobs(props.resumeId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: [
            {
              id: 1,
              job_id: 101,
              position_name: '后端开发工程师',
              department: '技术部',
              match_score: 85,
              match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
            },
            {
              id: 2,
              job_id: 102,
              position_name: '全栈开发工程师',
              department: '技术部',
              match_score: 70,
              match_explanation: '候选人后端技能匹配度高，但前端技能略显不足。'
            }
          ]
        };
        
        // 设置匹配的职位
        matchedJobs.value = response.data;
      } catch (error) {
        console.error('获取匹配职位失败:', error);
        ElMessage.error('获取匹配职位失败，请重试');
      }
    };
    
    // 处理编辑
    const handleEdit = () => {
      if (!resume.value) return;
      
      // 复制简历信息到编辑表单
      Object.keys(editForm).forEach(key => {
        if (key in resume.value) {
          if (key === 'skills') {
            editForm.skills = [...resume.value.skills];
          } else {
            editForm[key] = resume.value[key];
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
        editForm.skills.push(inputTagValue.value);
      }
      inputTagVisible.value = false;
      inputTagValue.value = '';
    };
    
    // 移除标签
    const removeTag = (index) => {
      editForm.skills.splice(index, 1);
    };
    
    // 保存编辑
    const saveEdit = async () => {
      saving.value = true;
      
      try {
        // 调用API保存编辑
        // await api.updateResume(props.resumeId, editForm);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        
        ElMessage.success('保存成功');
        
        // 关闭对话框
        editDialogVisible.value = false;
        
        // 重新获取简历详情
        fetchResumeDetail();
        
        // 通知父组件刷新列表
        emit('refresh');
      } catch (error) {
        console.error('保存失败:', error);
        ElMessage.error('保存失败，请重试');
      } finally {
        saving.value = false;
      }
    };
    
    // 处理匹配职位
    const handleMatch = () => {
      if (!resume.value) return;
      
      // 跳转到匹配职位页面
      // router.push(`/resumes/${resume.value.id}/match`);
      
      // 或者显示匹配职位对话框
      ElMessage.info('正在跳转到职位匹配页面...');
    };
    
    // 处理删除
    const handleDelete = () => {
      if (!resume.value) return;
      
      deleteDialogVisible.value = true;
    };
    
    // 确认删除
    const confirmDelete = async () => {
      if (!resume.value) return;
      
      deleting.value = true;
      
      try {
        // 调用API删除简历
        // await api.deleteResume(resume.value.id);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        
        ElMessage.success('删除成功');
        
        // 关闭对话框
        deleteDialogVisible.value = false;
        
        // 清空简历详情
        resume.value = null;
        
        // 通知父组件刷新列表
        emit('refresh');
      } catch (error) {
        console.error('删除失败:', error);
        ElMessage.error('删除失败，请重试');
      } finally {
        deleting.value = false;
      }
    };
    
    // 查看职位
    const viewJob = (matchedJob) => {
      emit('view-job', matchedJob.job_id);
    };
    
    // 格式化工作经历
    const formatWorkHistory = (workHistory) => {
      if (!workHistory) return [];
      
      // 如果已经是列表形式，直接返回
      if (workHistory.includes('\n')) {
        return workHistory.split('\n');
      }
      
      // 否则直接返回原文本
      return [workHistory];
    };
    
    // 格式化教育经历
    const formatEducationHistory = (educationHistory) => {
      if (!educationHistory) return [];
      
      // 如果已经是列表形式，直接返回
      if (educationHistory.includes('\n')) {
        return educationHistory.split('\n');
      }
      
      // 否则直接返回原文本
      return [educationHistory];
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 监听resumeId变化
    watch(() => props.resumeId, (newVal) => {
      if (newVal) {
        fetchResumeDetail();
      } else {
        resume.value = null;
      }
    }, { immediate: true });
    
    return {
      resume,
      loading,
      deleting,
      saving,
      deleteDialogVisible,
      editDialogVisible,
      editForm,
      inputTagVisible,
      inputTagValue,
      tagInputRef,
      matchedJobs,
      handleEdit,
      showTagInput,
      addTag,
      removeTag,
      saveEdit,
      handleMatch,
      handleDelete,
      confirmDelete,
      viewJob,
      formatWorkHistory,
      formatEducationHistory,
      getMatchScoreColor
    };
  }
};
</script>

<style scoped>
.resume-detail {
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
