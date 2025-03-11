<template>
  <div id="app">
    <header class="header">
      <h1>HR招聘系统</h1>
    </header>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      backendStatus: null
    }
  },
  mounted() {
    this.checkBackend()
  },
  methods: {
    async checkBackend() {
      try {
        const response = await fetch('http://localhost:8001/')
        const data = await response.json()
        this.backendStatus = data.message || JSON.stringify(data)
      } catch (error) {
        this.backendStatus = `后端服务连接失败: ${error.message}`
      }
    }
  }
}
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
.header {
  background-color: #4CAF50;
  color: white;
  padding: 20px;
  text-align: center;
}
.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 10px 0;
  cursor: pointer;
  border-radius: 4px;
}
</style>
