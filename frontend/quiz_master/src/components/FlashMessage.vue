<!-- components/common/FlashMessage.vue -->
<template>
  <div class="flash-container" v-if="visible">
    <div :class="['flash-message', type]">
      <strong>{{ message }}</strong>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    type: {
      type: String,
      default: 'success' // 'success', 'error', 'warning', etc.
    }
  },
  data() {
    return {
      visible: true
    };
  },
  mounted() {
    setTimeout(() => {
      this.visible = false;
    }, 3000); // Auto-hide after 3s
  }
};
</script>

<style scoped>
.flash-container {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  justify-content: center;
  width: 100%;
}

.flash-message {
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 15px;
  text-align: center;
  animation: slideIn 0.5s ease-out forwards, fadeOut 1s ease-in-out forwards 2.5s;
}

.flash-message.success {
  background-color: #28a745;
}
.flash-message.error {
  background-color: #dc3545;
}
.flash-message.warning {
  background-color: #ffc107;
  color: black;
}

@keyframes slideIn {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeOut {
  to {
    opacity: 0;
  }
}
</style>
