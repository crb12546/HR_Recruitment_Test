<template>
  <div class="plan-generator">
    <el-form :model="planForm" label-width="100px">
      <!-- 方案基本信息 -->
      <el-form-item label="方案名称" prop="name">
        <el-input v-model="planForm.name" placeholder="请输入方案名称" />
      </el-form-item>
      
      <el-form-item label="招聘需求" prop="jobId">
        <el-select
          v-model="planForm.jobId"
          placeholder="选择招聘需求"
          filterable
          clearable
          @change="handleJobChange"
          :disabled="!!selectedJob"
        >
          <el-option
            v-for="job in jobOptions"
            :key="job.value"
            :label="job.label"
            :value="job.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="方案描述" prop="description">
        <el-input
          v-model="planForm.description"
          type="textarea"
          :rows="3"
          placeholder="请输入方案描述"
        />
      </el-form-item>
      
      <!-- 职位信息 -->
      <div v-if="selectedJob" class="section">
        <h3>职位信息</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="职位名称">{{ selectedJob.position_name }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ selectedJob.department }}</el-descriptions-item>
          <el-descriptions-item label="工作地点">{{ selectedJob.location }}</el-descriptions-item>
          <el-descriptions-item label="薪资范围">{{ selectedJob.salary_range }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <!-- 候选人列表 -->
      <div class="section">
        <div class="section-header">
          <h3>候选人列表</h3>
          <el-button type="primary" size="small" @click="showCandidateSelector = true">
            添加候选人
          </el-button>
        </div>
        
        <el-table
          v-if="selectedCandidates.length > 0"
          :data="selectedCandidates"
          style="width: 100%"
        >
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
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button
                size="small"
                type="danger"
                @click="removeCandidate(scope.$index)"
              >
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-else description="暂无候选人，请添加候选人" />
      </div>
      
      <!-- 招聘策略 -->
      <div class="section">
        <h3>招聘策略</h3>
        <el-form-item label="面试轮次" prop="interviewRounds">
          <el-input-number v-model="planForm.interviewRounds" :min="1" :max="5" />
        </el-form-item>
        
        <el-form-item label="面试方式">
          <el-checkbox-group v-model="planForm.interviewMethods">
            <el-checkbox label="线上面试">线上面试</el-checkbox>
            <el-checkbox label="现场面试">现场面试</el-checkbox>
            <el-checkbox label="技术测试">技术测试</el-checkbox>
            <el-checkbox label="团队面试">团队面试</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="招聘周期" prop="recruitmentCycle">
          <el-input v-model="planForm.recruitmentCycle" placeholder="例如：30天" />
        </el-form-item>
        
        <el-form-item label="招聘建议" prop="recruitmentSuggestion">
          <el-input
            v-model="planForm.recruitmentSuggestion"
            type="textarea"
            :rows="4"
            placeholder="请输入招聘建议"
          />
        </el-form-item>
      </div>
      
      <!-- 操作按钮 -->
      <el-form-item>
        <el-button type="primary" @click="generatePlan" :loading="generating">生成方案</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 候选人选择器对话框 -->
    <el-dialog
      v-model="showCandidateSelector"
      title="选择候选人"
      width="70%"
    >
      <el-table
        :data="candidateOptions"
        style="width: 100%"
        @selection-change="handleCandidateSelectionChange"
      >
        <el-table-column type="selection" width="55" />
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
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCandidateSelector = false">取消</el-button>
          <el-button type="primary" @click="confirmCandidateSelection">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'PlanGenerator',
  props: {
    initialJobId: {
      type: [Number, String],
      default: null
    },
    initialCandidates: {
      type: Array,
      default: () => []
    }
  },
  emits: ['plan-generated'],
  setup(props, { emit }) {
    // 方案表单
    const planForm = reactive({
      name: '',
      jobId: null,
      description: '',
      interviewRounds: 3,
      interviewMethods: ['线上面试', '现场面试'],
      recruitmentCycle: '30天',
      recruitmentSuggestion: ''
    });
    
    // 职位选项
    const jobOptions = ref([]);
    
    // 选中的职位
    const selectedJob = ref(null);
    
    // 候选人选项
    const candidateOptions = ref([]);
    
    // 选中的候选人
    const selectedCandidates = ref([]);
    
    // 临时选中的候选人
    const tempSelectedCandidates = ref([]);
    
    // 是否显示候选人选择器
    const showCandidateSelector = ref(false);
    
    // 生成状态
    const generating = ref(false);
    
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
    
    // 获取职位详情
    const fetchJobDetail = async (jobId) => {
      if (!jobId) {
        selectedJob.value = null;
        return;
      }
      
      try {
        // 调用API获取职位详情
        // const response = await api.getJobDetail(jobId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: {
            id: jobId,
            position_name: '后端开发工程师',
            department: '技术部',
            location: '北京',
            salary_range: '20k-30k',
            responsibilities: '负责公司产品的后端开发，包括API设计和实现，确保系统的稳定性和性能。',
            requirements: '1. 熟练掌握Java、Spring Boot等后端技术\n2. 熟悉MySQL数据库和微服务架构\n3. 具有良好的团队协作能力',
            created_at: '2025-03-01T10:00:00Z',
            updated_at: '2025-03-01T10:00:00Z'
          }
        };
        
        // 设置选中的职位
        selectedJob.value = response.data;
      } catch (error) {
        console.error('获取职位详情失败:', error);
        ElMessage.error('获取职位详情失败，请重试');
      }
    };
    
    // 获取候选人选项
    const fetchCandidateOptions = async (jobId) => {
      if (!jobId) {
        candidateOptions.value = [];
        return;
      }
      
      try {
        // 调用API获取候选人选项
        // const response = await api.getMatchedCandidates(jobId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = {
          data: [
            {
              id: 1,
              resume_id: 1,
              job_id: jobId,
              candidate_name: '张三',
              match_score: 85,
              match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。'
            },
            {
              id: 2,
              resume_id: 2,
              job_id: jobId,
              candidate_name: '李四',
              match_score: 70,
              match_explanation: '候选人具备基本技能要求，但工作经验略显不足。'
            },
            {
              id: 3,
              resume_id: 3,
              job_id: jobId,
              candidate_name: '王五',
              match_score: 60,
              match_explanation: '候选人技能与职位要求部分匹配，缺乏核心技能。'
            },
            {
              id: 4,
              resume_id: 4,
              job_id: jobId,
              candidate_name: '赵六',
              match_score: 75,
              match_explanation: '候选人技能匹配度较高，但缺乏团队协作经验。'
            },
            {
              id: 5,
              resume_id: 5,
              job_id: jobId,
              candidate_name: '钱七',
              match_score: 65,
              match_explanation: '候选人具备部分技能要求，需要进一步培训。'
            }
          ]
        };
        
        // 设置候选人选项
        candidateOptions.value = response.data;
      } catch (error) {
        console.error('获取候选人选项失败:', error);
        ElMessage.error('获取候选人选项失败，请重试');
      }
    };
    
    // 处理职位变更
    const handleJobChange = (jobId) => {
      if (!jobId) {
        selectedJob.value = null;
        candidateOptions.value = [];
        selectedCandidates.value = [];
        return;
      }
      
      fetchJobDetail(jobId);
      fetchCandidateOptions(jobId);
      
      // 设置方案名称
      const selectedJobOption = jobOptions.value.find(option => option.value === jobId);
      if (selectedJobOption) {
        planForm.name = `${selectedJobOption.label}招聘方案`;
      }
    };
    
    // 处理候选人选择变更
    const handleCandidateSelectionChange = (selection) => {
      tempSelectedCandidates.value = selection;
    };
    
    // 确认候选人选择
    const confirmCandidateSelection = () => {
      // 合并已选择的候选人和新选择的候选人
      const existingIds = selectedCandidates.value.map(candidate => candidate.id);
      const newCandidates = tempSelectedCandidates.value.filter(candidate => !existingIds.includes(candidate.id));
      
      selectedCandidates.value = [...selectedCandidates.value, ...newCandidates];
      showCandidateSelector.value = false;
    };
    
    // 移除候选人
    const removeCandidate = (index) => {
      selectedCandidates.value.splice(index, 1);
    };
    
    // 生成方案
    const generatePlan = async () => {
      if (!planForm.jobId) {
        ElMessage.warning('请选择招聘需求');
        return;
      }
      
      if (selectedCandidates.value.length === 0) {
        ElMessage.warning('请添加候选人');
        return;
      }
      
      if (!planForm.name) {
        ElMessage.warning('请输入方案名称');
        return;
      }
      
      generating.value = true;
      
      try {
        // 构建方案数据
        const planData = {
          name: planForm.name,
          job_id: planForm.jobId,
          description: planForm.description,
          candidates: selectedCandidates.value.map(candidate => candidate.id),
          interview_rounds: planForm.interviewRounds,
          interview_methods: planForm.interviewMethods,
          recruitment_cycle: planForm.recruitmentCycle,
          recruitment_suggestion: planForm.recruitmentSuggestion
        };
        
        // 调用API生成方案
        // const response = await api.generatePlan(planData);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 1500));
        const response = {
          data: {
            id: 1,
            ...planData,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          }
        };
        
        ElMessage.success('招聘方案生成成功');
        
        // 发送方案生成事件
        emit('plan-generated', response.data);
        
        // 重置表单
        resetForm();
      } catch (error) {
        console.error('生成方案失败:', error);
        ElMessage.error('生成方案失败，请重试');
      } finally {
        generating.value = false;
      }
    };
    
    // 重置表单
    const resetForm = () => {
      planForm.name = '';
      planForm.jobId = null;
      planForm.description = '';
      planForm.interviewRounds = 3;
      planForm.interviewMethods = ['线上面试', '现场面试'];
      planForm.recruitmentCycle = '30天';
      planForm.recruitmentSuggestion = '';
      
      selectedJob.value = null;
      selectedCandidates.value = [];
      candidateOptions.value = [];
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 初始化
    onMounted(() => {
      fetchJobOptions();
      
      // 如果有初始职位ID，设置职位ID并获取职位详情
      if (props.initialJobId) {
        planForm.jobId = props.initialJobId;
        handleJobChange(props.initialJobId);
      }
      
      // 如果有初始候选人，设置候选人
      if (props.initialCandidates && props.initialCandidates.length > 0) {
        selectedCandidates.value = [...props.initialCandidates];
      }
    });
    
    return {
      planForm,
      jobOptions,
      selectedJob,
      candidateOptions,
      selectedCandidates,
      tempSelectedCandidates,
      showCandidateSelector,
      generating,
      handleJobChange,
      handleCandidateSelectionChange,
      confirmCandidateSelection,
      removeCandidate,
      generatePlan,
      resetForm,
      getMatchScoreColor
    };
  }
};
</script>

<style scoped>
.plan-generator {
  padding: 20px;
}

.section {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  margin: 0;
}
</style>
