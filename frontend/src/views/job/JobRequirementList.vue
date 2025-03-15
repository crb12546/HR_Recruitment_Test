<template>
  <div class="job-requirement-list">
    <div class="page-header">
      <h2>招聘需求管理</h2>
      <div class="header-actions">
        <el-button type="primary" @click="goToUpload">
          <el-icon><Plus /></el-icon>上传需求
        </el-button>
        <el-button type="success" @click="goToCreate">
          <el-icon><Edit /></el-icon>创建需求
        </el-button>
      </div>
    </div>

    <!-- 搜索过滤区域 -->
    <div class="filter-container">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="职位名称">
          <el-input v-model="filterForm.position_name" placeholder="输入职位名称" clearable />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="filterForm.department" placeholder="输入部门" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据表格 -->
    <el-table
      v-loading="loading"
      :data="jobRequirements"
      border
      style="width: 100%"
      @row-click="handleRowClick"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="position_name" label="职位名称" min-width="150" />
      <el-table-column prop="department" label="部门" width="120" />
      <el-table-column prop="salary_range" label="薪资范围" width="120" />
      <el-table-column prop="location" label="工作地点" width="120" />
      <el-table-column label="标签" width="200">
        <template #default="scope">
          <el-tag
            v-for="(tag, index) in scope.row.tags"
            :key="index"
            size="small"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="scope">
          <el-button size="small" @click.stop="handleEdit(scope.row)">
            编辑
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click.stop="handleDelete(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
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
          <el-button type="danger" @click="confirmDelete" :loading="deleting">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Edit, Search, Refresh } from '@element-plus/icons-vue';
import { getJobRequirements, deleteJobRequirement } from '@/api/job';

export default {
  name: 'JobRequirementList',
  components: {
    Plus,
    Edit,
    Search,
    Refresh
  },
  setup() {
    const router = useRouter();
    
    // 数据加载状态
    const loading = ref(false);
    
    // 招聘需求列表
    const jobRequirements = ref([]);
    
    // 分页相关
    const currentPage = ref(1);
    const pageSize = ref(10);
    const total = ref(0);
    
    // 过滤表单
    const filterForm = reactive({
      position_name: '',
      department: ''
    });
    
    // 删除相关
    const deleteDialogVisible = ref(false);
    const currentJob = ref(null);
    const deleting = ref(false);
    
    // 加载招聘需求列表
    const loadJobRequirements = async () => {
      loading.value = true;
      
      try {
        const params = {
          skip: (currentPage.value - 1) * pageSize.value,
          limit: pageSize.value,
          ...filterForm
        };
        
        const response = await getJobRequirements(params);
        jobRequirements.value = response;
        total.value = response.length; // 实际项目中应从后端获取总数
        
      } catch (error) {
        console.error('获取招聘需求列表失败:', error);
        ElMessage.error('获取招聘需求列表失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 处理过滤
    const handleFilter = () => {
      currentPage.value = 1;
      loadJobRequirements();
    };
    
    // 重置过滤
    const resetFilter = () => {
      filterForm.position_name = '';
      filterForm.department = '';
      handleFilter();
    };
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      loadJobRequirements();
    };
    
    // 处理每页条数变化
    const handleSizeChange = (size) => {
      pageSize.value = size;
      currentPage.value = 1;
      loadJobRequirements();
    };
    
    // 处理行点击
    const handleRowClick = (row) => {
      router.push(`/jobs/${row.id}`);
    };
    
    // 跳转到上传页面
    const goToUpload = () => {
      router.push('/jobs/upload');
    };
    
    // 跳转到创建页面
    const goToCreate = () => {
      router.push('/jobs/create');
    };
    
    // 处理编辑
    const handleEdit = (row) => {
      router.push(`/jobs/${row.id}/edit`);
    };
    
    // 处理删除
    const handleDelete = (row) => {
      currentJob.value = row;
      deleteDialogVisible.value = true;
    };
    
    // 确认删除
    const confirmDelete = async () => {
      if (!currentJob.value) return;
      
      deleting.value = true;
      
      try {
        await deleteJobRequirement(currentJob.value.id);
        ElMessage.success('删除成功');
        loadJobRequirements();
      } catch (error) {
        console.error('删除招聘需求失败:', error);
        ElMessage.error('删除招聘需求失败，请重试');
      } finally {
        deleting.value = false;
        deleteDialogVisible.value = false;
      }
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
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadJobRequirements();
    });
    
    return {
      loading,
      jobRequirements,
      currentPage,
      pageSize,
      total,
      filterForm,
      deleteDialogVisible,
      deleting,
      handleFilter,
      resetFilter,
      handleCurrentChange,
      handleSizeChange,
      handleRowClick,
      goToUpload,
      goToCreate,
      handleEdit,
      handleDelete,
      confirmDelete,
      formatDate
    };
  }
};
</script>

<style scoped>
.job-requirement-list {
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

.filter-container {
  margin-bottom: 20px;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
}

.tag-item {
  margin-right: 5px;
  margin-bottom: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
