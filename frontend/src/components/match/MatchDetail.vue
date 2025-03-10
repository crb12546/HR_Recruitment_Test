<template>
  <div class="match-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="!match" class="empty-container">
      <el-empty description="请选择一个匹配结果查看详情" />
    </div>
    
    <div v-else class="detail-container">
      <!-- 标题和操作按钮 -->
      <div class="header">
        <h2 class="title">{{ match.candidate_name }} - 匹配详情</h2>
        <div class="actions">
          <el-button type="primary" @click="viewResume">查看简历</el-button>
          <el-button type="success" @click="viewJob">查看职位</el-button>
          <el-button type="warning" @click="addToPlan">加入方案</el-button>
        </div>
      </div>
      
      <!-- 匹配分数 -->
      <div class="score-container">
        <div class="score-card">
          <h3>总体匹配度</h3>
          <el-progress
            type="dashboard"
            :percentage="match.match_score"
            :color="getMatchScoreColor(match.match_score)"
            :stroke-width="10"
          />
          <p class="score-description">{{ getMatchScoreDescription(match.match_score) }}</p>
        </div>
        
        <div class="score-details">
          <div class="score-item">
            <span class="score-label">技能匹配</span>
            <el-progress
              :percentage="match.skill_match_score"
              :color="getMatchScoreColor(match.skill_match_score)"
            />
          </div>
          <div class="score-item">
            <span class="score-label">经验匹配</span>
            <el-progress
              :percentage="match.experience_match_score"
              :color="getMatchScoreColor(match.experience_match_score)"
            />
          </div>
          <div class="score-item">
            <span class="score-label">学历匹配</span>
            <el-progress
              :percentage="match.education_match_score"
              :color="getMatchScoreColor(match.education_match_score)"
            />
          </div>
        </div>
      </div>
      
      <!-- 匹配说明 -->
      <div class="section">
        <h3>匹配说明</h3>
        <div class="content">
          <p>{{ match.match_explanation }}</p>
        </div>
      </div>
      
      <!-- 技能匹配详情 -->
      <div class="section">
        <h3>技能匹配详情</h3>
        <el-table :data="skillMatchDetails" style="width: 100%">
          <el-table-column prop="skill" label="技能" width="150" />
          <el-table-column prop="required_level" label="需求水平" width="100" />
          <el-table-column prop="candidate_level" label="候选人水平" width="100" />
          <el-table-column prop="match_score" label="匹配度" width="200">
            <template #default="scope">
              <el-progress
                :percentage="scope.row.match_score"
                :color="getMatchScoreColor(scope.row.match_score)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="comment" label="说明" />
        </el-table>
      </div>
      
      <!-- 经验匹配详情 -->
      <div class="section">
        <h3>经验匹配详情</h3>
        <div class="content">
          <p>{{ match.experience_match_explanation || '暂无经验匹配详情' }}</p>
        </div>
      </div>
      
      <!-- 学历匹配详情 -->
      <div class="section">
        <h3>学历匹配详情</h3>
        <div class="content">
          <p>{{ match.education_match_explanation || '暂无学历匹配详情' }}</p>
        </div>
      </div>
      
      <!-- 优势与不足 -->
      <div class="section">
        <h3>优势与不足</h3>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="advantage-card">
              <h4>优势</h4>
              <ul>
                <li v-for="(item, index) in match.advantages" :key="'adv-' + index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="disadvantage-card">
              <h4>不足</h4>
              <ul>
                <li v-for="(item, index) in match.disadvantages" :key="'dis-' + index">
                  {{ item }}
                </li>
              </ul>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 面试建议 -->
      <div class="section">
        <h3>面试建议</h3>
        <div class="content">
          <p>{{ match.interview_suggestion || '暂无面试建议' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  name: 'MatchDetail',
  props: {
    matchId: {
      type: [Number, String],
      default: null
    }
  },
  emits: ['view-resume', 'view-job', 'add-to-plan'],
  setup(props, { emit }) {
    // 匹配详情
    const match = ref(null);
    
    // 加载状态
    const loading = ref(false);
    
    // 技能匹配详情
    const skillMatchDetails = ref([]);
    
    // 获取匹配详情
    const fetchMatchDetail = async () => {
      if (!props.matchId) {
        match.value = null;
        return;
      }
      
      loading.value = true;
      
      try {
        // 调用API获取匹配详情
        // const response = await api.getMatchDetail(props.matchId);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            id: props.matchId,
            resume_id: 1,
            job_id: 1,
            candidate_name: '张三',
            match_score: 85,
            skill_match_score: 90,
            experience_match_score: 80,
            education_match_score: 85,
            match_explanation: '候选人技能与职位要求高度匹配，具有相关工作经验。该候选人在Java开发方面有丰富经验，熟悉Spring Boot和微服务架构，符合职位对后端开发的要求。工作经验略显不足，但技能水平较高，可以考虑面试。',
            experience_match_explanation: '候选人有3年相关工作经验，职位要求3-5年经验，基本符合要求。',
            education_match_explanation: '候选人具有本科学历，符合职位对学历的要求。',
            advantages: [
              '技术栈与职位要求高度匹配',
              '有良好的项目经验',
              '沟通能力强',
              '有团队协作经验'
            ],
            disadvantages: [
              '工作经验略显不足',
              '缺乏大型项目经验',
              '管理经验不足'
            ],
            interview_suggestion: '建议重点考察候选人的实际项目经验和技术深度，可以通过技术面试了解其解决问题的能力。同时，关注其团队协作能力和沟通能力。'
          }
        };
        
        // 设置匹配详情
        match.value = response.data;
        
        // 设置技能匹配详情
        skillMatchDetails.value = [
          {
            skill: 'Java',
            required_level: '精通',
            candidate_level: '精通',
            match_score: 95,
            comment: '候选人在Java开发方面有丰富经验，熟悉Java 8新特性。'
          },
          {
            skill: 'Spring Boot',
            required_level: '熟练',
            candidate_level: '熟练',
            match_score: 90,
            comment: '候选人熟悉Spring Boot框架，有实际项目经验。'
          },
          {
            skill: '微服务',
            required_level: '了解',
            candidate_level: '熟悉',
            match_score: 100,
            comment: '候选人对微服务架构有深入理解，超出职位要求。'
          },
          {
            skill: 'MySQL',
            required_level: '熟练',
            candidate_level: '熟悉',
            match_score: 80,
            comment: '候选人熟悉MySQL数据库，但缺乏性能优化经验。'
          },
          {
            skill: 'Docker',
            required_level: '熟悉',
            candidate_level: '了解',
            match_score: 60,
            comment: '候选人对Docker有基本了解，但缺乏实际使用经验。'
          }
        ];
      } catch (error) {
        console.error('获取匹配详情失败:', error);
        ElMessage.error('获取匹配详情失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 查看简历
    const viewResume = () => {
      if (!match.value) return;
      
      emit('view-resume', match.value.resume_id);
    };
    
    // 查看职位
    const viewJob = () => {
      if (!match.value) return;
      
      emit('view-job', match.value.job_id);
    };
    
    // 加入方案
    const addToPlan = () => {
      if (!match.value) return;
      
      emit('add-to-plan', match.value);
      ElMessage.success(`已将 ${match.value.candidate_name} 添加到方案`);
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 获取匹配分数描述
    const getMatchScoreDescription = (score) => {
      if (score >= 80) return '非常匹配';
      if (score >= 60) return '基本匹配';
      return '匹配度低';
    };
    
    // 监听matchId变化
    watch(() => props.matchId, (newVal) => {
      if (newVal) {
        fetchMatchDetail();
      } else {
        match.value = null;
      }
    }, { immediate: true });
    
    return {
      match,
      loading,
      skillMatchDetails,
      viewResume,
      viewJob,
      addToPlan,
      getMatchScoreColor,
      getMatchScoreDescription
    };
  }
};
</script>

<style scoped>
.match-detail {
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

.score-container {
  display: flex;
  margin-bottom: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 20px;
}

.score-card {
  flex: 0 0 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 20px;
  border-right: 1px solid #ebeef5;
}

.score-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #303133;
}

.score-description {
  margin-top: 10px;
  color: #606266;
  font-weight: bold;
}

.score-details {
  flex: 1;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.score-item {
  margin-bottom: 15px;
}

.score-label {
  display: inline-block;
  width: 80px;
  color: #606266;
}

.section {
  margin: 20px 0;
}

.section h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.content {
  color: #606266;
  line-height: 1.6;
}

.advantage-card, .disadvantage-card {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
  height: 100%;
}

.advantage-card h4, .disadvantage-card h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #303133;
}

.advantage-card {
  border-left: 4px solid #67C23A;
}

.disadvantage-card {
  border-left: 4px solid #F56C6C;
}

.advantage-card ul, .disadvantage-card ul {
  margin: 0;
  padding-left: 20px;
}

.advantage-card li, .disadvantage-card li {
  margin-bottom: 5px;
  color: #606266;
}
</style>
