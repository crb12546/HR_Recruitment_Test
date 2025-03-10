<template>
  <div class="resume-filter">
    <el-form :model="filterForm" label-width="80px" class="filter-form">
      <el-form-item label="关键词">
        <el-input
          v-model="filterForm.keyword"
          placeholder="搜索候选人姓名或技能"
          clearable
          @input="handleFilterChange"
        />
      </el-form-item>
      
      <el-form-item label="学历">
        <el-select
          v-model="filterForm.education"
          placeholder="选择学历"
          clearable
          @change="handleFilterChange"
        >
          <el-option
            v-for="item in educationOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="工作经验">
        <el-select
          v-model="filterForm.experience"
          placeholder="选择工作经验"
          clearable
          @change="handleFilterChange"
        >
          <el-option
            v-for="item in experienceOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="技能标签">
        <el-select
          v-model="filterForm.skills"
          placeholder="选择技能标签"
          multiple
          collapse-tags
          clearable
          @change="handleFilterChange"
        >
          <el-option
            v-for="item in skillOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="上传时间">
        <el-date-picker
          v-model="filterForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          @change="handleFilterChange"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="applyFilter">筛选</el-button>
        <el-button @click="resetFilter">重置</el-button>
        <el-button type="text" @click="toggleAdvanced">
          {{ showAdvanced ? '收起高级筛选' : '展开高级筛选' }}
          <el-icon>
            <component :is="showAdvanced ? 'ArrowUp' : 'ArrowDown'" />
          </el-icon>
        </el-button>
      </el-form-item>
    </el-form>
    
    <!-- 高级筛选选项 -->
    <div v-if="showAdvanced" class="advanced-filter">
      <el-form :model="advancedFilterForm" label-width="80px">
        <el-form-item label="匹配度">
          <el-slider
            v-model="advancedFilterForm.matchScore"
            range
            :min="0"
            :max="100"
            :marks="matchScoreMarks"
            @change="handleFilterChange"
          />
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select
            v-model="advancedFilterForm.status"
            placeholder="选择状态"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="来源">
          <el-select
            v-model="advancedFilterForm.source"
            placeholder="选择来源"
            clearable
            @change="handleFilterChange"
          >
            <el-option
              v-for="item in sourceOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 已选筛选条件 -->
    <div v-if="hasActiveFilters" class="active-filters">
      <span class="filter-label">已选条件：</span>
      <el-tag
        v-for="(filter, index) in activeFilters"
        :key="index"
        closable
        @close="removeFilter(filter.key)"
        class="filter-tag"
      >
        {{ filter.label }}: {{ filter.value }}
      </el-tag>
      <el-button type="text" @click="resetFilter">清空全部</el-button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue';

export default {
  name: 'ResumeFilter',
  emits: ['filter-change'],
  setup(props, { emit }) {
    // 基本筛选表单
    const filterForm = reactive({
      keyword: '',
      education: '',
      experience: '',
      skills: [],
      dateRange: []
    });
    
    // 高级筛选表单
    const advancedFilterForm = reactive({
      matchScore: [0, 100],
      status: '',
      source: ''
    });
    
    // 是否显示高级筛选
    const showAdvanced = ref(false);
    
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
    
    // 状态选项
    const statusOptions = [
      { value: '待筛选', label: '待筛选' },
      { value: '已通过', label: '已通过' },
      { value: '已淘汰', label: '已淘汰' },
      { value: '面试中', label: '面试中' },
      { value: '已录用', label: '已录用' }
    ];
    
    // 来源选项
    const sourceOptions = [
      { value: '内部推荐', label: '内部推荐' },
      { value: '招聘网站', label: '招聘网站' },
      { value: '猎头', label: '猎头' },
      { value: '校园招聘', label: '校园招聘' },
      { value: '其他', label: '其他' }
    ];
    
    // 匹配度标记
    const matchScoreMarks = {
      0: '0%',
      25: '25%',
      50: '50%',
      75: '75%',
      100: '100%'
    };
    
    // 切换高级筛选
    const toggleAdvanced = () => {
      showAdvanced.value = !showAdvanced.value;
    };
    
    // 处理筛选变化
    const handleFilterChange = () => {
      // 延迟发送筛选变化事件，避免频繁触发
      if (filterChangeTimer) {
        clearTimeout(filterChangeTimer);
      }
      
      filterChangeTimer = setTimeout(() => {
        emitFilterChange();
      }, 300);
    };
    
    // 应用筛选
    const applyFilter = () => {
      emitFilterChange();
    };
    
    // 重置筛选
    const resetFilter = () => {
      // 重置基本筛选表单
      Object.keys(filterForm).forEach(key => {
        if (Array.isArray(filterForm[key])) {
          filterForm[key] = [];
        } else {
          filterForm[key] = '';
        }
      });
      
      // 重置高级筛选表单
      advancedFilterForm.matchScore = [0, 100];
      advancedFilterForm.status = '';
      advancedFilterForm.source = '';
      
      // 发送筛选变化事件
      emitFilterChange();
    };
    
    // 移除筛选条件
    const removeFilter = (key) => {
      if (key.startsWith('advanced.')) {
        const advancedKey = key.replace('advanced.', '');
        if (advancedKey === 'matchScore') {
          advancedFilterForm.matchScore = [0, 100];
        } else {
          advancedFilterForm[advancedKey] = '';
        }
      } else {
        if (Array.isArray(filterForm[key])) {
          filterForm[key] = [];
        } else {
          filterForm[key] = '';
        }
      }
      
      // 发送筛选变化事件
      emitFilterChange();
    };
    
    // 发送筛选变化事件
    const emitFilterChange = () => {
      const filters = {
        ...getActiveBasicFilters(),
        ...getActiveAdvancedFilters()
      };
      
      emit('filter-change', filters);
    };
    
    // 获取激活的基本筛选条件
    const getActiveBasicFilters = () => {
      const filters = {};
      
      Object.keys(filterForm).forEach(key => {
        const value = filterForm[key];
        if (Array.isArray(value)) {
          if (value.length > 0) {
            filters[key] = value;
          }
        } else if (value) {
          filters[key] = value;
        }
      });
      
      return filters;
    };
    
    // 获取激活的高级筛选条件
    const getActiveAdvancedFilters = () => {
      const filters = {};
      
      if (advancedFilterForm.matchScore[0] > 0 || advancedFilterForm.matchScore[1] < 100) {
        filters.matchScore = advancedFilterForm.matchScore;
      }
      
      if (advancedFilterForm.status) {
        filters.status = advancedFilterForm.status;
      }
      
      if (advancedFilterForm.source) {
        filters.source = advancedFilterForm.source;
      }
      
      return filters;
    };
    
    // 是否有激活的筛选条件
    const hasActiveFilters = computed(() => {
      return activeFilters.value.length > 0;
    });
    
    // 激活的筛选条件
    const activeFilters = computed(() => {
      const filters = [];
      
      // 基本筛选条件
      Object.keys(filterForm).forEach(key => {
        const value = filterForm[key];
        if (Array.isArray(value)) {
          if (value.length > 0) {
            filters.push({
              key,
              label: getFilterLabel(key),
              value: value.join(', ')
            });
          }
        } else if (value) {
          filters.push({
            key,
            label: getFilterLabel(key),
            value
          });
        }
      });
      
      // 高级筛选条件
      if (advancedFilterForm.matchScore[0] > 0 || advancedFilterForm.matchScore[1] < 100) {
        filters.push({
          key: 'advanced.matchScore',
          label: '匹配度',
          value: `${advancedFilterForm.matchScore[0]}% - ${advancedFilterForm.matchScore[1]}%`
        });
      }
      
      if (advancedFilterForm.status) {
        filters.push({
          key: 'advanced.status',
          label: '状态',
          value: advancedFilterForm.status
        });
      }
      
      if (advancedFilterForm.source) {
        filters.push({
          key: 'advanced.source',
          label: '来源',
          value: advancedFilterForm.source
        });
      }
      
      return filters;
    });
    
    // 获取筛选条件标签
    const getFilterLabel = (key) => {
      const labelMap = {
        keyword: '关键词',
        education: '学历',
        experience: '工作经验',
        skills: '技能标签',
        dateRange: '上传时间'
      };
      
      return labelMap[key] || key;
    };
    
    // 筛选变化定时器
    let filterChangeTimer = null;
    
    return {
      filterForm,
      advancedFilterForm,
      showAdvanced,
      educationOptions,
      experienceOptions,
      skillOptions,
      statusOptions,
      sourceOptions,
      matchScoreMarks,
      hasActiveFilters,
      activeFilters,
      toggleAdvanced,
      handleFilterChange,
      applyFilter,
      resetFilter,
      removeFilter
    };
  }
};
</script>

<style scoped>
.resume-filter {
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.filter-form {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.filter-form .el-form-item:last-child {
  grid-column: 1 / -1;
  margin-bottom: 0;
}

.advanced-filter {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px dashed #dcdfe6;
}

.active-filters {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.filter-label {
  margin-right: 10px;
  color: #606266;
}

.filter-tag {
  margin-right: 10px;
  margin-bottom: 5px;
}
</style>
