<template>
  <div class="tab-bar-container">
    <el-tabs
      v-model="activeTab"
      type="card"
      closable
      @tab-click="handleTabClick"
      @tab-remove="handleTabRemove"
    >
      <el-tab-pane
        v-for="tab in tabs"
        :key="tab.path"
        :label="tab.title"
        :name="tab.path"
      >
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  name: 'TabBar',
  data() {
    return {
      activeTab: '',
      tabs: []
    };
  },
  methods: {
    // 添加新标签页
    addTab(tab) {
      // 检查标签页是否已存在
      const isExist = this.tabs.some(item => item.path === tab.path);
      if (!isExist) {
        this.tabs.push(tab);
      }
      this.activeTab = tab.path;
    },
    // 处理标签页点击事件
    handleTabClick(tab) {
      this.$router.push(tab.name);
    },
    // 处理标签页关闭事件
    handleTabRemove(targetPath) {
      // 找到要关闭的标签页索引
      const tabs = this.tabs;
      let activeTab = this.activeTab;
      
      // 如果关闭的是当前激活的标签页，则需要激活其他标签页
      if (activeTab === targetPath) {
        tabs.forEach((tab, index) => {
          if (tab.path === targetPath) {
            const nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeTab = nextTab.path;
              this.$router.push(nextTab.path);
            } else {
              // 如果没有其他标签页，则跳转到首页
              activeTab = '/dashboard';
              this.$router.push('/dashboard');
            }
          }
        });
      }
      
      // 移除标签页
      this.activeTab = activeTab;
      this.tabs = tabs.filter(tab => tab.path !== targetPath);
    },
    // 根据路由更新标签页
    updateTabsByRoute(route) {
      const { path, meta } = route;
      
      // 如果路由有标题，则添加标签页
      if (meta && meta.title) {
        this.addTab({
          title: meta.title,
          path: path
        });
      }
    }
  },
  watch: {
    // 监听路由变化，更新标签页
    '$route'(to) {
      this.updateTabsByRoute(to);
    }
  },
  mounted() {
    // 初始化时根据当前路由添加标签页
    this.updateTabsByRoute(this.$route);
  }
};
</script>

<style scoped>
.tab-bar-container {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 15px;
}

.el-tabs {
  margin-bottom: -1px;
}
</style>
