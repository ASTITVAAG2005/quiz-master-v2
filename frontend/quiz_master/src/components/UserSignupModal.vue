<template>
  <div class="modal-backdrop">
    <div class="modal-dialog-centered modal">
      <div class="modal-content">
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
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
