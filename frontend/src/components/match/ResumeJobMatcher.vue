<template>
  <div class="resume-job-matcher">
    <el-form :model="matchForm" label-width="100px">
      <!-- 选择职位 -->
      <el-form-item label="招聘需求" prop="jobId">
        <el-select
          v-model="matchForm.jobId"
          placeholder="选择招聘需求"
          filterable
          clearable
          @change="handleJobChange"
        >
          <el-option
            v-for="job in jobOptions"
            :key="job.value"
            :label="job.label"
            :value="job.value"
          />
        </el-select>
      </el-form-item>
      
      <!-- 选择简历 -->
      <el-form-item label="候选简历" prop="resumeIds">
        <el-select
          v-model="matchForm.resumeIds"
          placeholder="选择候选简历"
          filterable
          multiple
          collapse-tags
          clearable
        >
          <el-option
            v-for="resume in resumeOptions"
            :key="resume.value"
            :label="resume.label"
            :value="resume.value"
          />
        </el-select>
      </el-form-item>
      
      <!-- 匹配设置 -->
      <el-form-item label="匹配设置">
        <el-checkbox v-model="matchForm.includeSkills">技能匹配</el-checkbox>
        <el-checkbox v-model="matchForm.includeExperience">经验匹配</el-checkbox>
        <el-checkbox v-model="matchForm.includeEducation">学历匹配</el-checkbox>
      </el-form-item>
      
      <!-- 匹配阈值 -->
      <el-form-item label="匹配阈值">
        <el-slider
          v-model="matchForm.threshold"
          :min="0"
          :max="100"
          :step="5"
          :marks="thresholdMarks"
        />
      </el-form-item>
      
      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="startMatching" :loading="loading">开始匹配</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 匹配结果 -->
    <div v-if="matchResults.length > 0" class="match-results">
      <h3>匹配结果</h3>
      <el-table :data="matchResults" style="width: 100%">
        <el-table-column prop="candidate_name" label="候选人" width="120" />
        <el-table-column prop="match_score" label="匹配度" width="100">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.match_score"
              :color="getMatchScoreColor(scope.row.match_score)"
            />
          </template>
        </el-table-column>
        <el-table-column label="技能匹配" width="100">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.skill_match_score"
              :color="getMatchScoreColor(scope.row.skill_match_score)"
            />
          </template>
        </el-table-column>
        <el-table-column label="经验匹配" width="100">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.experience_match_score"
              :color="getMatchScoreColor(scope.row.experience_match_score)"
            />
          </template>
        </el-table-column>
        <el-table-column label="学历匹配" width="100">
          <template #default="scope">
            <el-progress
              :percentage="scope.row.education_match_score"
              :color="getMatchScoreColor(scope.row.education_match_score)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="match_explanation" label="匹配说明" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              @click="viewDetail(scope.row)"
            >
              查看详情
            </el-button>
            <el-button
              size="small"
              type="success"
              @click="addToPlan(scope.row)"
            >
              加入方案
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 生成招聘方案按钮 -->
      <div class="generate-plan-container">
        <el-button type="primary" @click="generatePlan" :disabled="selectedMatches.length === 0">
          生成招聘方案
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'ResumeJobMatcher',
  emits: ['view-detail', 'generate-plan'],
  setup(props, { emit }) {
    // 匹配表单
    const matchForm = reactive({
      jobId: null,
      resumeIds: [],
      includeSkills: true,
      includeExperience: true,
      includeEducation: true,
      threshold: 60
    });
    
    // 职位选项
    const jobOptions = ref([]);
    
    // 简历选项
    const resumeOptions = ref([]);
    
    // 匹配结果
    const matchResults = ref([]);
    
    // 选中的匹配结果
    const selectedMatches = ref([]);
    
    // 加载状态
    const loading = ref(false);
    
    // 阈值标记
    const thresholdMarks = {
      0: '0%',
      25: '25%',
      50: '50%',
      75: '75%',
      100: '100%'
    };
    
    // 获取职位选项
    const fetchJobOptions = async () => {
      try {
        // 调用API获取职位列表
        // const response = await api.getJobList();
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: {
            items: [
              { id: 1, position_name: '前端开发工程师' },
              { id: 2, position_name: '后端开发工程师' },
              { id: 3, position_name: '产品经理' }
            ]
          }
        };
        
        // 设置职位选项
        jobOptions.value = response.data.items.map(job => ({
          value: job.id,
          label: job.position_name
        }));
      } catch (error) {
        console.error('获取职位列表失败:', error);
        ElMessage.error('获取职位列表失败，请重试');
      }
    };
    
    // 获取简历选项
    const fetchResumeOptions = async () => {
      try {
        // 调用API获取简历列表
        // const response = await api.getResumeList();
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: {
            items: [
              { id: 1, candidate_name: '张三' },
              { id: 2, candidate_name: '李四' },
              { id: 3, candidate_name: '王五' }
            ]
          }
        };
        
        // 设置简历选项
        resumeOptions.value = response.data.items.map(resume => ({
          value: resume.id,
          label: resume.candidate_name
        }));
      } catch (error) {
        console.error('获取简历列表失败:', error);
        ElMessage.error('获取简历列表失败，请重试');
      }
    };
    
    // 处理职位变更
    const handleJobChange = (jobId) => {
      if (!jobId) return;
      
      // 可以在这里根据选择的职位获取推荐的简历
      // fetchRecommendedResumes(jobId);
    };
    
    // 开始匹配
    const startMatching = async () => {
      if (!matchForm.jobId) {
        ElMessage.warning('请选择招聘需求');
        return;
      }
      
      if (matchForm.resumeIds.length === 0) {
        ElMessage.warning('请选择候选简历');
        return;
      }
      
      loading.value = true;
      
      try {
        // 构建匹配参数
        const params = {
          job_id: matchForm.jobId,
          resume_ids: matchForm.resumeIds,
          include_skills: matchForm.includeSkills,
          include_experience: matchForm.includeExperience,
          include_education: matchForm.includeEducation,
          threshold: matchForm.threshold
        };
        
        // 调用API进行匹配
        // const response = await api.matchResumesWithJob(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1500));
        const response = {
          data: [
            {
              id: 1,
              resume_id: 1,
              job_id: matchForm.jobId,
              candidate_name: '张三',
              match_score: 85,
              skill_match_score: 90,
              experience_match_score: 80,
              education_match_score: 85,
              match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
            },
            {
              id: 2,
              resume_id: 2,
              job_id: matchForm.jobId,
              candidate_name: '李四',
              match_score: 70,
              skill_match_score: 75,
              experience_match_score: 65,
              education_match_score: 70,
              match_explanation: '候选人具备基本技能要求，但工作经验略显不足。'
            },
            {
              id: 3,
              resume_id: 3,
              job_id: matchForm.jobId,
              candidate_name: '王五',
              match_score: 60,
              skill_match_score: 65,
              experience_match_score: 55,
              education_match_score: 60,
              match_explanation: '候选人技能与职位要求部分匹配，缺乏核心技能。'
            }
          ]
        };
        
        // 设置匹配结果
        matchResults.value = response.data;
        
        ElMessage.success('匹配完成');
      } catch (error) {
        console.error('匹配失败:', error);
        ElMessage.error('匹配失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 重置表单
    const resetForm = () => {
      matchForm.jobId = null;
      matchForm.resumeIds = [];
      matchForm.threshold = 60;
      matchResults.value = [];
      selectedMatches.value = [];
    };
    
    // 查看详情
    const viewDetail = (match) => {
      emit('view-detail', match);
    };
    
    // 添加到方案
    const addToPlan = (match) => {
      const index = selectedMatches.value.findIndex(item => item.id === match.id);
      
      if (index === -1) {
        selectedMatches.value.push(match);
        ElMessage.success(`已将 ${match.candidate_name} 添加到方案`);
      } else {
        selectedMatches.value.splice(index, 1);
        ElMessage.info(`已将 ${match.candidate_name} 从方案中移除`);
      }
    };
    
    // 生成招聘方案
    const generatePlan = () => {
      if (selectedMatches.value.length === 0) {
        ElMessage.warning('请先选择候选人');
        return;
      }
      
      emit('generate-plan', {
        jobId: matchForm.jobId,
        matches: selectedMatches.value
      });
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 组件挂载时获取职位和简历选项
    onMounted(() => {
      fetchJobOptions();
      fetchResumeOptions();
    });
    
    return {
      matchForm,
      jobOptions,
      resumeOptions,
      matchResults,
      selectedMatches,
      loading,
      thresholdMarks,
      handleJobChange,
      startMatching,
      resetForm,
      viewDetail,
      addToPlan,
      generatePlan,
      getMatchScoreColor
    };
  }
};
</script>

<style scoped>
.resume-job-matcher {
  padding: 20px;
}

.match-results {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px dashed #dcdfe6;
}

.match-results h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.generate-plan-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
