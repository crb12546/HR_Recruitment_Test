<template>
  <div v-if="show" class="error-message" :class="{ 'is-fixed': fixed }">
    <el-alert
      :title="title"
      :description="message"
      :type="type"
      :closable="closable"
      show-icon
      @close="handleClose"
    />
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '错误'
    },
    message: {
      type: String,
      default: '发生了一个错误，请稍后重试'
    },
    type: {
      type: String,
      default: 'error',
      validator: (value) => ['success', 'warning', 'info', 'error'].includes(value)
    },
    fixed: {
      type: Boolean,
      default: false
    },
    closable: {
      type: Boolean,
      default: true
    },
    duration: {
      type: Number,
      default: 0 // 0表示不自动关闭
    }
  },
  data() {
    return {
      timer: null
    };
  },
  methods: {
    handleClose() {
      this.$emit('close');
    }
  },
  watch: {
    show(newVal) {
      if (newVal && this.duration > 0) {
        // 清除之前的定时器
        if (this.timer) {
          clearTimeout(this.timer);
        }
        
        // 设置新的定时器
        this.timer = setTimeout(() => {
          this.$emit('close');
        }, this.duration);
      }
    }
  },
  beforeUnmount() {
    // 组件销毁前清除定时器
    if (this.timer) {
      clearTimeout(this.timer);
    }
  }
};
</script>

<style scoped>
.error-message {
  margin-bottom: 15px;
}

.error-message.is-fixed {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2000;
  min-width: 300px;
  max-width: 80%;
}
</style>
