<template>
  <div class="job-list">
    <!-- 搜索和过滤区域 -->
    <div class="filter-container">
      <el-input
        v-model="searchQuery"
        placeholder="搜索职位名称"
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-select
        v-model="departmentFilter"
        placeholder="部门筛选"
        clearable
        @change="handleFilter"
      >
        <el-option
          v-for="item in departmentOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select
        v-model="locationFilter"
        placeholder="工作地点"
        clearable
        @change="handleFilter"
      >
        <el-option
          v-for="item in locationOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-button type="primary" @click="handleFilter">筛选</el-button>
      <el-button @click="resetFilter">重置</el-button>
    </div>
    
    <!-- 职位列表 -->
    <el-table
      v-loading="loading"
      :data="jobList"
      style="width: 100%"
      @row-click="handleRowClick"
      highlight-current-row
    >
      <el-table-column prop="position_name" label="职位名称" min-width="150" />
      <el-table-column prop="department" label="部门" width="120" />
      <el-table-column prop="location" label="工作地点" width="120" />
      <el-table-column prop="salary_range" label="薪资范围" width="120" />
      <el-table-column prop="created_at" label="发布时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="标签" min-width="200">
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
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button
            size="small"
            type="primary"
            @click.stop="viewDetail(scope.row)"
          >
            查看
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
          <el-button type="danger" @click="confirmDelete" :loading="deleting">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'JobList',
  emits: ['select-job'],
  setup(props, { emit }) {
    // 搜索和筛选
    const searchQuery = ref('');
    const departmentFilter = ref('');
    const locationFilter = ref('');
    
    // 分页
    const currentPage = ref(1);
    const pageSize = ref(10);
    const total = ref(0);
    
    // 加载状态
    const loading = ref(false);
    const deleting = ref(false);
    
    // 职位列表数据
    const jobList = ref([]);
    
    // 删除对话框
    const deleteDialogVisible = ref(false);
    const jobToDelete = ref(null);
    
    // 部门选项
    const departmentOptions = [
      { value: '技术部', label: '技术部' },
      { value: '产品部', label: '产品部' },
      { value: '市场部', label: '市场部' },
      { value: '销售部', label: '销售部' },
      { value: '人力资源部', label: '人力资源部' }
    ];
    
    // 工作地点选项
    const locationOptions = [
      { value: '北京', label: '北京' },
      { value: '上海', label: '上海' },
      { value: '广州', label: '广州' },
      { value: '深圳', label: '深圳' },
      { value: '杭州', label: '杭州' }
    ];
    
    // 获取职位列表
    const fetchJobList = async () => {
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value || undefined,
          department: departmentFilter.value || undefined,
          location: locationFilter.value || undefined
        };
        
        // 调用API获取职位列表
        // const response = await api.getJobList(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            items: [
              {
                id: 1,
                position_name: '前端开发工程师',
                department: '技术部',
                responsibilities: '负责公司产品的前端开发，包括页面设计和实现，确保良好的用户体验。',
                requirements: '1. 熟练掌握HTML、CSS、JavaScript等前端技术\n2. 熟悉Vue.js或React等前端框架\n3. 具有良好的团队协作能力',
                salary_range: '15k-25k',
                location: '北京',
                tags: ['前端', 'Vue.js', 'JavaScript'],
                created_at: '2025-03-01T10:00:00Z',
                updated_at: '2025-03-01T10:00:00Z'
              },
              {
                id: 2,
                position_name: '后端开发工程师',
                department: '技术部',
                responsibilities: '负责公司产品的后端开发，包括API设计和实现，确保系统稳定性和性能。',
                requirements: '1. 熟练掌握Java、Python等后端语言\n2. 熟悉Spring Boot、Django等后端框架\n3. 具有良好的数据库设计能力',
                salary_range: '20k-30k',
                location: '上海',
                tags: ['后端', 'Java', 'Spring Boot'],
                created_at: '2025-03-02T10:00:00Z',
                updated_at: '2025-03-02T10:00:00Z'
              },
              {
                id: 3,
                position_name: '产品经理',
                department: '产品部',
                responsibilities: '负责公司产品的规划和设计，包括需求分析、产品原型设计和产品迭代。',
                requirements: '1. 具有3年以上产品经理经验\n2. 熟悉互联网产品开发流程\n3. 具有良好的沟通能力和团队协作能力',
                salary_range: '25k-35k',
                location: '北京',
                tags: ['产品', '需求分析', '原型设计'],
                created_at: '2025-03-03T10:00:00Z',
                updated_at: '2025-03-03T10:00:00Z'
              }
            ],
            total: 3
          }
        };
        
        // 设置职位列表和总数
        jobList.value = response.data.items;
        total.value = response.data.total;
      } catch (error) {
        console.error('获取职位列表失败:', error);
        ElMessage.error('获取职位列表失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1;
      fetchJobList();
    };
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      fetchJobList();
    };
    
    // 重置筛选
    const resetFilter = () => {
      searchQuery.value = '';
      departmentFilter.value = '';
      locationFilter.value = '';
      currentPage.value = 1;
      fetchJobList();
    };
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      fetchJobList();
    };
    
    // 处理每页条数变化
    const handleSizeChange = (size) => {
      pageSize.value = size;
      currentPage.value = 1;
      fetchJobList();
    };
    
    // 处理行点击
    const handleRowClick = (row) => {
      emit('select-job', row);
    };
    
    // 查看详情
    const viewDetail = (row) => {
      emit('select-job', row);
    };
    
    // 处理删除
    const handleDelete = (row) => {
      jobToDelete.value = row;
      deleteDialogVisible.value = true;
    };
    
    // 确认删除
    const confirmDelete = async () => {
      if (!jobToDelete.value) return;
      
      deleting.value = true;
      
      try {
        // 调用API删除职位
        // await api.deleteJob(jobToDelete.value.id);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        
        ElMessage.success('删除成功');
        
        // 关闭对话框
        deleteDialogVisible.value = false;
        
        // 重新获取列表
        fetchJobList();
      } catch (error) {
        console.error('删除职位失败:', error);
        ElMessage.error('删除职位失败，请重试');
      } finally {
        deleting.value = false;
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
    
    // 组件挂载时获取职位列表
    onMounted(() => {
      fetchJobList();
    });
    
    return {
      searchQuery,
      departmentFilter,
      locationFilter,
      departmentOptions,
      locationOptions,
      currentPage,
      pageSize,
      total,
      loading,
      deleting,
      jobList,
      deleteDialogVisible,
      handleSearch,
      handleFilter,
      resetFilter,
      handleCurrentChange,
      handleSizeChange,
      handleRowClick,
      viewDetail,
      handleDelete,
      confirmDelete,
      formatDate
    };
  }
};
</script>

<style scoped>
.job-list {
  padding: 20px;
}

.filter-container {
  display: flex;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.search-input {
  width: 220px;
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
