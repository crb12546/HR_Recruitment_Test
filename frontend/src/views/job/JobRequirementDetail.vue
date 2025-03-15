<template>
  <div class="job-requirement-detail">
    <div class="page-header">
      <h2>招聘需求详情</h2>
      <div class="header-actions">
        <el-button @click="goBack">
          <el-icon><Back /></el-icon>返回列表
        </el-button>
        <el-button type="primary" @click="handleEdit">
          <el-icon><Edit /></el-icon>编辑
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="detail-card">
      <template v-if="jobDetail">
        <div class="detail-header">
          <h3>{{ jobDetail.position_name }}</h3>
          <div class="detail-meta">
            <span class="meta-item">
              <el-icon><OfficeBuilding /></el-icon>
              {{ jobDetail.department || '未设置部门' }}
            </span>
            <span class="meta-item">
              <el-icon><Money /></el-icon>
              {{ jobDetail.salary_range || '薪资面议' }}
            </span>
            <span class="meta-item">
              <el-icon><Location /></el-icon>
              {{ jobDetail.location || '地点未定' }}
            </span>
          </div>
          <div class="detail-tags">
            <el-tag
              v-for="(tag, index) in jobDetail.tags"
              :key="index"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h4>工作职责</h4>
          <div class="section-content" v-html="formatContent(jobDetail.responsibilities)"></div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h4>任职要求</h4>
          <div class="section-content" v-html="formatContent(jobDetail.requirements)"></div>
        </div>

        <el-divider />

        <div class="detail-footer">
          <p class="create-time">创建时间：{{ formatDate(jobDetail.created_at) }}</p>
          <p class="update-time">更新时间：{{ formatDate(jobDetail.updated_at) }}</p>
        </div>
      </template>

      <template v-else-if="!loading">
        <el-empty description="未找到招聘需求详情" />
      </template>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { Back, Edit, OfficeBuilding, Money, Location } from '@element-plus/icons-vue';
import { getJobRequirement } from '@/api/job';

export default {
  name: 'JobRequirementDetail',
  components: {
    Back,
    Edit,
    OfficeBuilding,
    Money,
    Location
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    // 数据加载状态
    const loading = ref(false);
    
    // 招聘需求详情
    const jobDetail = ref(null);
    
    // 加载招聘需求详情
    const loadJobDetail = async () => {
      const jobId = route.params.id;
      if (!jobId) return;
      
      loading.value = true;
      
      try {
        const response = await getJobRequirement(jobId);
        jobDetail.value = response;
      } catch (error) {
        console.error('获取招聘需求详情失败:', error);
        ElMessage.error('获取招聘需求详情失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 返回列表
    const goBack = () => {
      router.push('/jobs');
    };
    
    // 编辑招聘需求
    const handleEdit = () => {
      router.push(`/jobs/${route.params.id}/edit`);
    };
    
    // 格式化内容（将换行符转换为HTML）
    const formatContent = (content) => {
      if (!content) return '';
      return content.replace(/\n/g, '<br>');
    };
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadJobDetail();
    });
    
    return {
      loading,
      jobDetail,
      goBack,
      handleEdit,
      formatContent,
      formatDate
    };
  }
};
</script>

<style scoped>
.job-requirement-detail {
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

.detail-card {
  margin-bottom: 20px;
}

.detail-header {
  margin-bottom: 20px;
}

.detail-header h3 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #303133;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
}

.detail-tags {
  margin-top: 10px;
}

.tag-item {
  margin-right: 8px;
  margin-bottom: 8px;
}

.detail-section {
  margin: 20px 0;
}

.detail-section h4 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #303133;
}

.section-content {
  line-height: 1.6;
  color: #606266;
}

.detail-footer {
  margin-top: 20px;
  color: #909399;
  font-size: 14px;
}

.create-time, .update-time {
  margin: 5px 0;
}
</style>
