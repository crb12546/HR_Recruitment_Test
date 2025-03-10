<template>
  <div class="match-list-page">
    <div class="page-header">
      <h2>匹配结果列表</h2>
      <div class="header-actions">
        <el-button type="primary" @click="goToMatch">
          <el-icon><Plus /></el-icon>
          新建匹配
        </el-button>
      </div>
    </div>
    
    <div class="content-container">
      <!-- 左侧：匹配列表 -->
      <div class="list-container">
        <div class="filter-bar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索职位或候选人"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="jobFilter"
            placeholder="职位筛选"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="item in jobOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          
          <el-select
            v-model="scoreFilter"
            placeholder="匹配度筛选"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="item in scoreOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </div>
        
        <el-table
          :data="matchList"
          style="width: 100%"
          @row-click="handleSelectMatch"
          highlight-current-row
          v-loading="loading"
        >
          <el-table-column prop="candidate_name" label="候选人" width="120" />
          <el-table-column prop="job_name" label="职位" width="150" />
          <el-table-column prop="match_score" label="匹配度" width="100">
            <template #default="scope">
              <el-progress
                :percentage="scope.row.match_score"
                :color="getMatchScoreColor(scope.row.match_score)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="match_date" label="匹配日期" width="120">
            <template #default="scope">
              {{ formatDate(scope.row.match_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalMatches"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
      
      <!-- 右侧：匹配详情 -->
      <div class="detail-container">
        <match-detail
          :match-id="selectedMatchId"
          @view-resume="handleViewResume"
          @view-job="handleViewJob"
          @add-to-plan="handleAddToPlan"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import MatchDetail from '@/components/match/MatchDetail.vue';

export default {
  name: 'MatchListPage',
  components: {
    MatchDetail
  },
  setup() {
    const router = useRouter();
    
    // 匹配列表
    const matchList = ref([]);
    
    // 选中的匹配ID
    const selectedMatchId = ref(null);
    
    // 加载状态
    const loading = ref(false);
    
    // 分页
    const currentPage = ref(1);
    const pageSize = ref(10);
    const totalMatches = ref(0);
    
    // 筛选
    const searchQuery = ref('');
    const jobFilter = ref('');
    const scoreFilter = ref('');
    
    // 职位选项
    const jobOptions = ref([
      { value: 1, label: '前端开发工程师' },
      { value: 2, label: '后端开发工程师' },
      { value: 3, label: '产品经理' }
    ]);
    
    // 匹配度选项
    const scoreOptions = ref([
      { value: 'high', label: '高匹配度 (80-100%)' },
      { value: 'medium', label: '中匹配度 (60-80%)' },
      { value: 'low', label: '低匹配度 (0-60%)' }
    ]);
    
    // 获取匹配列表
    const fetchMatchList = async () => {
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value || undefined,
          job_id: jobFilter.value || undefined,
          score_range: getScoreRange(scoreFilter.value)
        };
        
        // 调用API获取匹配列表
        // const response = await api.getMatchList(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            items: [
              {
                id: 1,
                candidate_name: '张三',
                job_name: '后端开发工程师',
                match_score: 85,
                match_date: '2025-03-01T10:00:00Z',
                status: '已匹配'
              },
              {
                id: 2,
                candidate_name: '李四',
                job_name: '前端开发工程师',
                match_score: 70,
                match_date: '2025-03-02T10:00:00Z',
                status: '已面试'
              },
              {
                id: 3,
                candidate_name: '王五',
                job_name: '产品经理',
                match_score: 60,
                match_date: '2025-03-03T10:00:00Z',
                status: '已淘汰'
              },
              {
                id: 4,
                candidate_name: '赵六',
                job_name: '后端开发工程师',
                match_score: 75,
                match_date: '2025-03-04T10:00:00Z',
                status: '已录用'
              },
              {
                id: 5,
                candidate_name: '钱七',
                job_name: '前端开发工程师',
                match_score: 65,
                match_date: '2025-03-05T10:00:00Z',
                status: '已匹配'
              }
            ],
            total: 5
          }
        };
        
        // 设置匹配列表
        matchList.value = response.data.items;
        totalMatches.value = response.data.total;
        
        // 如果有匹配结果且未选中任何匹配，则选中第一个
        if (matchList.value.length > 0 && !selectedMatchId.value) {
          selectedMatchId.value = matchList.value[0].id;
        }
      } catch (error) {
        console.error('获取匹配列表失败:', error);
        ElMessage.error('获取匹配列表失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 处理选择匹配
    const handleSelectMatch = (row) => {
      selectedMatchId.value = row.id;
    };
    
    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1;
      fetchMatchList();
    };
    
    // 处理筛选变更
    const handleFilterChange = () => {
      currentPage.value = 1;
      fetchMatchList();
    };
    
    // 处理页码变更
    const handleCurrentChange = (page) => {
      fetchMatchList();
    };
    
    // 处理每页数量变更
    const handleSizeChange = (size) => {
      currentPage.value = 1;
      fetchMatchList();
    };
    
    // 跳转到匹配页面
    const goToMatch = () => {
      router.push('/matches/create');
    };
    
    // 处理查看简历
    const handleViewResume = (resumeId) => {
      router.push(`/resumes/${resumeId}`);
    };
    
    // 处理查看职位
    const handleViewJob = (jobId) => {
      router.push(`/jobs/${jobId}`);
    };
    
    // 处理添加到方案
    const handleAddToPlan = (match) => {
      router.push({
        path: '/plans/create',
        query: {
          job_id: match.job_id,
          match_id: match.id
        }
      });
    };
    
    // 获取匹配分数颜色
    const getMatchScoreColor = (score) => {
      if (score >= 80) return '#67C23A';
      if (score >= 60) return '#E6A23C';
      return '#F56C6C';
    };
    
    // 获取状态类型
    const getStatusType = (status) => {
      const statusMap = {
        '已匹配': 'info',
        '已面试': 'warning',
        '已淘汰': 'danger',
        '已录用': 'success'
      };
      
      return statusMap[status] || 'info';
    };
    
    // 获取分数范围
    const getScoreRange = (scoreFilter) => {
      if (!scoreFilter) return undefined;
      
      const scoreRangeMap = {
        'high': '80,100',
        'medium': '60,80',
        'low': '0,60'
      };
      
      return scoreRangeMap[scoreFilter];
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    };
    
    // 组件挂载时获取匹配列表
    onMounted(() => {
      fetchMatchList();
    });
    
    return {
      matchList,
      selectedMatchId,
      loading,
      currentPage,
      pageSize,
      totalMatches,
      searchQuery,
      jobFilter,
      scoreFilter,
      jobOptions,
      scoreOptions,
      handleSelectMatch,
      handleSearch,
      handleFilterChange,
      handleCurrentChange,
      handleSizeChange,
      goToMatch,
      handleViewResume,
      handleViewJob,
      handleAddToPlan,
      getMatchScoreColor,
      getStatusType,
      formatDate
    };
  }
};
</script>

<style scoped>
.match-list-page {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.content-container {
  display: flex;
  flex: 1;
  gap: 20px;
  min-height: 500px;
}

.list-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.pagination-container {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.detail-container {
  flex: 1;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>
