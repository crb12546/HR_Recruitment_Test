<template>
  <div class="header-container">
    <!-- 左侧区域 -->
    <div class="header-left">
      <div class="breadcrumb-container">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item v-for="(item, index) in breadcrumbs" :key="index" :to="item.path">
            {{ item.title }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    
    <!-- 右侧区域 -->
    <div class="header-right">
      <!-- 搜索框 -->
      <div class="search-container">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索..."
          prefix-icon="el-icon-search"
          clearable
          @keyup.enter.native="handleSearch"
        ></el-input>
      </div>
      
      <!-- 用户信息 -->
      <div class="user-container">
        <el-dropdown trigger="click" @command="handleCommand">
          <div class="user-info">
            <el-avatar :size="32" :src="userAvatar"></el-avatar>
            <span class="username">{{ username }}</span>
            <i class="el-icon-caret-bottom"></i>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人信息</el-dropdown-item>
              <el-dropdown-item command="settings">系统设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      // 搜索关键词
      searchKeyword: '',
      // 用户头像
      userAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      // 用户名
      username: '管理员',
      // 面包屑导航
      breadcrumbs: [
        { title: '首页', path: '/dashboard' }
      ]
    };
  },
  methods: {
    // 处理搜索
    handleSearch() {
      if (this.searchKeyword.trim()) {
        this.$emit('search', this.searchKeyword);
        // 可以在这里实现全局搜索逻辑
        console.log('搜索关键词:', this.searchKeyword);
      }
    },
    // 处理下拉菜单命令
    handleCommand(command) {
      switch (command) {
        case 'profile':
          this.$router.push('/profile');
          break;
        case 'settings':
          this.$router.push('/settings');
          break;
        case 'logout':
          this.handleLogout();
          break;
      }
    },
    // 处理退出登录
    handleLogout() {
      // 清除用户信息和令牌
      // this.$store.dispatch('user/logout');
      // 跳转到登录页
      this.$router.push('/login');
    },
    // 更新面包屑导航
    updateBreadcrumbs() {
      const { matched } = this.$route;
      if (matched.length > 0) {
        this.breadcrumbs = matched.map(route => {
          return {
            title: route.meta.title || '未命名',
            path: route.path
          };
        });
      } else {
        this.breadcrumbs = [{ title: '首页', path: '/dashboard' }];
      }
    }
  },
  watch: {
    // 监听路由变化，更新面包屑导航
    '$route'() {
      this.updateBreadcrumbs();
    }
  },
  mounted() {
    // 初始化时更新面包屑导航
    this.updateBreadcrumbs();
  }
};
</script>

<style scoped>
.header-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-left, .header-right {
  display: flex;
  align-items: center;
}

.breadcrumb-container {
  margin-right: 20px;
}

.search-container {
  margin-right: 20px;
}

.search-container .el-input {
  width: 200px;
  transition: width 0.3s;
}

.search-container .el-input:focus-within {
  width: 250px;
}

.user-container {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  margin: 0 5px;
  color: #606266;
}
</style>
