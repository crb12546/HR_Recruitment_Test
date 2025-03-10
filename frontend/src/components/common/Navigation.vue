<template>
  <div class="navigation">
    <div class="logo">
      <img src="@/assets/logo.png" alt="Logo" />
      <h2>AI智能招聘系统</h2>
    </div>
    <el-menu
      :default-active="activeIndex"
      class="menu"
      @select="handleSelect"
      :collapse="isCollapse"
    >
      <el-sub-menu index="1">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>招聘管理</span>
        </template>
        <el-menu-item index="1-1">上传需求</el-menu-item>
        <el-menu-item index="1-2">招聘需求查看</el-menu-item>
        <el-menu-item index="1-3">招聘需求分析</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="2">
        <template #title>
          <el-icon><Files /></el-icon>
          <span>简历库管理</span>
        </template>
        <el-menu-item index="2-1">上传简历</el-menu-item>
        <el-menu-item index="2-2">简历列表</el-menu-item>
        <el-menu-item index="2-3">简历筛选</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="3">
        <template #title>
          <el-icon><Connection /></el-icon>
          <span>招聘方案</span>
        </template>
        <el-menu-item index="3-1">生成方案</el-menu-item>
        <el-menu-item index="3-2">方案列表</el-menu-item>
      </el-sub-menu>
      
      <el-sub-menu index="4">
        <template #title>
          <el-icon><DataAnalysis /></el-icon>
          <span>数据分析</span>
        </template>
        <el-menu-item index="4-1">招聘漏斗</el-menu-item>
        <el-menu-item index="4-2">渠道分析</el-menu-item>
        <el-menu-item index="4-3">候选人分析</el-menu-item>
      </el-sub-menu>
    </el-menu>
    
    <div class="collapse-btn" @click="toggleCollapse">
      <el-icon v-if="isCollapse"><Expand /></el-icon>
      <el-icon v-else><Fold /></el-icon>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      activeIndex: '1',
      isCollapse: false,
      menuItems: [
        {
          index: '1-1',
          route: '/jobs/upload'
        },
        {
          index: '1-2',
          route: '/jobs'
        },
        {
          index: '1-3',
          route: '/jobs/analysis'
        },
        {
          index: '2-1',
          route: '/resumes/upload'
        },
        {
          index: '2-2',
          route: '/resumes'
        },
        {
          index: '2-3',
          route: '/resumes/filter'
        },
        {
          index: '3-1',
          route: '/plans/create'
        },
        {
          index: '3-2',
          route: '/plans'
        },
        {
          index: '4-1',
          route: '/analytics/funnel'
        },
        {
          index: '4-2',
          route: '/analytics/channels'
        },
        {
          index: '4-3',
          route: '/analytics/candidates'
        }
      ]
    }
  },
  methods: {
    handleSelect(key) {
      const menuItem = this.menuItems.find(item => item.index === key)
      if (menuItem) {
        this.$router.push(menuItem.route)
      }
    },
    toggleCollapse() {
      this.isCollapse = !this.isCollapse
    }
  }
}
</script>

<style scoped>
.navigation {
  width: 260px;
  height: 100%;
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.navigation.collapsed {
  width: 64px;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e6e6e6;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.logo h2 {
  font-size: 18px;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu {
  flex: 1;
  border-right: none;
}

.collapse-btn {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-top: 1px solid #e6e6e6;
}
</style>
