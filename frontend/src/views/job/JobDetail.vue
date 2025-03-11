<template>
  <div class="job-detail">
    <h2>职位详情</h2>
    <p>职位详情页面正在开发中...</p>
  </div>
</template>

<script>
export default {
  name: 'JobDetail',
  data() {
    return {
      jobId: this.$route.params.id
    }
  },
  mounted() {
    console.log('加载职位ID:', this.jobId)
  }
}
</script>

<style scoped>
.job-detail {
  padding: 20px;
}
</style>
