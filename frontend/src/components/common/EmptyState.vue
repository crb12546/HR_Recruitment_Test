<template>
  <div class="empty-state">
    <div class="empty-image">
      <slot name="image">
        <el-empty :image="image" :image-size="imageSize" :description="description" />
      </slot>
    </div>
    <div class="empty-actions" v-if="$slots.default">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyState',
  props: {
    image: {
      type: String,
      default: ''
    },
    imageSize: {
      type: Number,
      default: 100
    },
    description: {
      type: String,
      default: '暂无数据'
    }
  }
};
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.empty-image {
  margin-bottom: 20px;
}

.empty-actions {
  margin-top: 20px;
}
</style>
