<template>
  <div class="resume-list">
    <!-- 搜索和过滤区域 -->
    <div class="filter-container">
      <el-input
        v-model="searchQuery"
        placeholder="搜索候选人姓名"
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-select
        v-model="educationFilter"
        placeholder="学历筛选"
        clearable
        @change="handleFilter"
      >
        <el-option
          v-for="item in educationOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select
        v-model="experienceFilter"
        placeholder="工作经验"
        clearable
        @change="handleFilter"
      >
        <el-option
          v-for="item in experienceOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-select
        v-model="skillFilter"
        placeholder="技能标签"
        clearable
        multiple
        collapse-tags
        @change="handleFilter"
      >
        <el-option
          v-for="item in skillOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      
      <el-button type="primary" @click="handleFilter">筛选</el-button>
      <el-button @click="resetFilter">重置</el-button>
    </div>
    
    <!-- 简历列表 -->
    <el-table
      v-loading="loading"
      :data="resumeList"
      style="width: 100%"
      @row-click="handleRowClick"
      highlight-current-row
    >
      <el-table-column prop="candidate_name" label="候选人" min-width="120" />
      <el-table-column prop="education" label="学历" width="100" />
      <el-table-column prop="experience" label="工作经验" width="100" />
      <el-table-column label="技能标签" min-width="200">
        <template #default="scope">
          <el-tag
            v-for="(tag, index) in scope.row.skills"
            :key="index"
            size="small"
            class="tag-item"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="上传时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
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
      <span>确定要删除该简历吗？此操作不可恢复。</span>
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
  name: 'ResumeList',
  emits: ['select-resume'],
  setup(props, { emit }) {
    // 搜索和筛选
    const searchQuery = ref('');
    const educationFilter = ref('');
    const experienceFilter = ref('');
    const skillFilter = ref([]);
    
    // 分页
    const currentPage = ref(1);
    const pageSize = ref(10);
    const total = ref(0);
    
    // 加载状态
    const loading = ref(false);
    const deleting = ref(false);
    
    // 简历列表数据
    const resumeList = ref([]);
    
    // 删除对话框
    const deleteDialogVisible = ref(false);
    const resumeToDelete = ref(null);
    
    // 学历选项
    const educationOptions = [
      { value: '博士', label: '博士' },
      { value: '硕士', label: '硕士' },
      { value: '本科', label: '本科' },
      { value: '大专', label: '大专' },
      { value: '高中及以下', label: '高中及以下' }
    ];
    
    // 工作经验选项
    const experienceOptions = [
      { value: '应届毕业生', label: '应届毕业生' },
      { value: '1-3年', label: '1-3年' },
      { value: '3-5年', label: '3-5年' },
      { value: '5-10年', label: '5-10年' },
      { value: '10年以上', label: '10年以上' }
    ];
    
    // 技能标签选项
    const skillOptions = [
      { value: 'Java', label: 'Java' },
      { value: 'Python', label: 'Python' },
      { value: 'JavaScript', label: 'JavaScript' },
      { value: 'Vue.js', label: 'Vue.js' },
      { value: 'React', label: 'React' },
      { value: 'Spring Boot', label: 'Spring Boot' },
      { value: 'MySQL', label: 'MySQL' },
      { value: '微服务', label: '微服务' },
      { value: '前端开发', label: '前端开发' },
      { value: '后端开发', label: '后端开发' }
    ];
    
    // 获取简历列表
    const fetchResumeList = async () => {
      loading.value = true;
      
      try {
        // 构建查询参数
        const params = {
          page: currentPage.value,
          page_size: pageSize.value,
          search: searchQuery.value || undefined,
          education: educationFilter.value || undefined,
          experience: experienceFilter.value || undefined,
          skills: skillFilter.value.length > 0 ? skillFilter.value.join(',') : undefined
        };
        
        // 调用API获取简历列表
        // const response = await api.getResumeList(params);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 800));
        const response = {
          data: {
            items: [
              {
                id: 1,
                candidate_name: '张三',
                education: '本科',
                experience: '3年',
                skills: ['Java', 'Spring Boot', 'MySQL'],
                created_at: '2025-03-01T10:00:00Z',
                updated_at: '2025-03-01T10:00:00Z'
              },
              {
                id: 2,
                candidate_name: '李四',
                education: '硕士',
                experience: '5年',
                skills: ['Python', 'Django', 'PostgreSQL'],
                created_at: '2025-03-02T10:00:00Z',
                updated_at: '2025-03-02T10:00:00Z'
              },
              {
                id: 3,
                candidate_name: '王五',
                education: '本科',
                experience: '2年',
                skills: ['JavaScript', 'Vue.js', 'Node.js'],
                created_at: '2025-03-03T10:00:00Z',
                updated_at: '2025-03-03T10:00:00Z'
              }
            ],
            total: 3
          }
        };
        
        // 设置简历列表和总数
        resumeList.value = response.data.items;
        total.value = response.data.total;
      } catch (error) {
        console.error('获取简历列表失败:', error);
        ElMessage.error('获取简历列表失败，请重试');
      } finally {
        loading.value = false;
      }
    };
    
    // 处理搜索
    const handleSearch = () => {
      currentPage.value = 1;
      fetchResumeList();
    };
    
    // 处理筛选
    const handleFilter = () => {
      currentPage.value = 1;
      fetchResumeList();
    };
    
    // 重置筛选
    const resetFilter = () => {
      searchQuery.value = '';
      educationFilter.value = '';
      experienceFilter.value = '';
      skillFilter.value = [];
      currentPage.value = 1;
      fetchResumeList();
    };
    
    // 处理页码变化
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      fetchResumeList();
    };
    
    // 处理每页条数变化
    const handleSizeChange = (size) => {
      pageSize.value = size;
      currentPage.value = 1;
      fetchResumeList();
    };
    
    // 处理行点击
    const handleRowClick = (row) => {
      emit('select-resume', row);
    };
    
    // 查看详情
    const viewDetail = (row) => {
      emit('select-resume', row);
    };
    
    // 处理删除
    const handleDelete = (row) => {
      resumeToDelete.value = row;
      deleteDialogVisible.value = true;
    };
    
    // 确认删除
    const confirmDelete = async () => {
      if (!resumeToDelete.value) return;
      
      deleting.value = true;
      
      try {
        // 调用API删除简历
        // await api.deleteResume(resumeToDelete.value.id);
        
        // 模拟API响应
        await new Promise(resolve => setTimeout(resolve, 500));
        
        ElMessage.success('删除成功');
        
        // 关闭对话框
        deleteDialogVisible.value = false;
        
        // 重新获取列表
        fetchResumeList();
      } catch (error) {
        console.error('删除简历失败:', error);
        ElMessage.error('删除简历失败，请重试');
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
    
    // 组件挂载时获取简历列表
    onMounted(() => {
      fetchResumeList();
    });
    
    return {
      searchQuery,
      educationFilter,
      experienceFilter,
      skillFilter,
      educationOptions,
      experienceOptions,
      skillOptions,
      currentPage,
      pageSize,
      total,
      loading,
      deleting,
      resumeList,
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
      formatDate,
      fetchResumeList
    };
  }
};
</script>

<style scoped>
.resume-list {
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
