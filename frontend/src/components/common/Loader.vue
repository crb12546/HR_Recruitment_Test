<template>
  <div class="loader-container" v-if="loading">
    <div class="loader-content">
      <el-icon class="loader-icon"><Loading /></el-icon>
      <p class="loader-text">{{ text }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Loader',
  props: {
    loading: {
      type: Boolean,
      default: true
    },
    text: {
      type: String,
      default: '加载中...'
    }
  }
};
</script>

<style scoped>
.loader-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1000;
}

.loader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loader-icon {
  font-size: 32px;
  color: #409EFF;
  animation: rotate 1.5s linear infinite;
}

.loader-text {
  margin-top: 10px;
  color: #606266;
  font-size: 14px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
