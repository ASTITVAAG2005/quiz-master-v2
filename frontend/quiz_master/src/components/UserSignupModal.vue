<template>
  <div class="custom-modal-backdrop">
    <div class="custom-modal-dialog">
      <div class="custom-modal-content">
        <div class="modal-header">
          <h5 class="modal-title">User Signup</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="signupUser">
            <div class="mb-3" v-for="(label, key) in fields" :key="key">
              <label class="form-label">{{ label }}</label>
              <input
                :type="key === 'email' ? 'email' : key === 'dob' ? 'date' : key === 'password' ? 'password' : 'text'"
                class="form-control"
                v-model="form[key]"
                required
              />
            </div>
            <button type="submit" class="btn btn-success w-100">Sign Up</button>
          </form>
          <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
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
      form: {
        username: '',
        email: '',
        password: '',
        fullname: '',
        qualification: '',
        dob: ''
      },
      error: '',
      success: '',
      fields: {
        username: 'Username',
        email: 'Email',
        password: 'Password',
        fullname: 'Full Name',
        qualification: 'Qualification',
        dob: 'Date of Birth'
      }
    };
  },
  methods: {
    async signupUser() {
      try {
        const res = await axios.post('http://localhost:5000/api/usersignup', this.form);
        if (res.status === 201 || res.status === 200) {
          this.success = 'Signup successful! You can now log in.';
          this.error = '';
          this.form = {
            username: '',
            email: '',
            password: '',
            fullname: '',
            qualification: '',
            dob: ''
          };
            setTimeout(() => {
      this.$emit('close');
    }, 1000);
        } else {
          this.error = 'Signup failed. Please try again.';
          this.success = '';
        }
      } catch (err) {
        this.error = err.response?.data?.msg || 'Signup failed. Try again.';
        this.success = '';
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
  max-width: 450px;
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
