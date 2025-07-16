<template>
  <div class="custom-modal-backdrop">
    <div class="custom-modal-dialog">
      <div class="custom-modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Admin Login</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="loginAdmin">
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input v-model="username" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-danger w-100">Login</button>
          </form>
          <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  methods: {
    async loginAdmin() {
      try {
        const res = await axios.post('http://localhost:5000/api/adminlogin', {
          username: this.username,
          password: this.password
        });
        if (res.status === 200) {
          localStorage.setItem('access_token', res.data.token);
          this.$router.push('/admin-dashboard');
        }
      } catch (err) {
        this.error = err.response?.data?.msg || 'Login failed';
      }
    }
  }
};
</script>

<style scoped>
.custom-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-modal-dialog {
  max-width: 400px;
  width: 100%;
}

.custom-modal-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  width: 100%;
}
</style>
