<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Quiz Master</a>
        <button class="btn btn-primary ms-auto" @click="goBack">Back to Dashboard</button>
      </div>
    </nav>

    <!-- Summary Content -->
    <div class="container mt-4">
      <h2 class="text-center">Your Performance Summary</h2>

      <div class="container mt-4">
        <h5>Your Performance Over Time</h5>
        <img
          v-if="chart"
          class="img-fluid"
          :src="`http://localhost:5000${chart}`"
          alt="Performance Chart"
        />
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserSummaryPage',
  data() {
    return {
      chart: '',
      error: ''
    }
  },
  mounted() {
    this.fetchSummary()
  },
  methods: {
    fetchSummary() {
      const token = localStorage.getItem('access_token')
      axios
        .get('http://localhost:5000/api/user/summary', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          this.chart = response.data.chart // "/static/user_performance_chart.png"
        })
        .catch(err => {
          console.error('Error loading user summary:', err)
          this.error = 'Failed to load performance chart.'
        })
    },
    goBack() {
      this.$router.push('/user-dashboard')
    }
  }
}
</script>

<style scoped>
img {
  border: 1px solid #ccc;
  padding: 10px;
  background-color: #fff;
  max-width: 100%;
}
</style>
