<template>
  <div class="home">
    <Navigation />
    <div class="content">
      <h1>欢迎使用AI智能招聘系统</h1>
      <el-row :gutter="20">
        <el-col :span="6" v-for="(card, index) in cards" :key="index">
          <el-card class="dashboard-card" shadow="hover" @click="navigateTo(card.route)">
            <div class="card-content">
              <h2>{{ card.title }}</h2>
              <p>{{ card.description }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Navigation from '@/components/common/Navigation.vue'

export default {
  name: 'Home',
  components: {
    Navigation
  },
  data() {
    return {
      cards: [
        {
          title: '招聘需求管理',
          description: '上传、解析和管理招聘需求',
          route: '/jobs'
        },
        {
          title: '简历库管理',
          description: '上传、解析和管理候选人简历',
          route: '/resumes'
        },
        {
          title: '简历匹配',
          description: '将简历与招聘需求进行智能匹配',
          route: '/matches'
        },
        {
          title: '数据分析',
          description: '查看招聘数据分析和报告',
          route: '/analytics'
        }
      ]
    }
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route)
    }
  }
}
</script>

<style scoped>
.home {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.dashboard-card {
  height: 180px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  text-align: center;
}
</style>
