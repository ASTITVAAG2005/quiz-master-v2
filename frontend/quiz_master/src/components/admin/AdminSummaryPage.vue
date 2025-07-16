<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Quiz Master</a>
        <button class="btn btn-primary ms-auto" @click="goBack">Back to Dashboard</button>
      </div>
    </nav>

    <div class="container mt-4">
      <h2 class="text-center">Admin Summary</h2>

      <div class="container mt-4">
        <h5>Quiz Statistics</h5>
        <img
          v-if="charts.length"
          class="img-fluid"
          :src="`http://localhost:5000${charts[1]}`"
          alt="Quiz Statistics Chart"
        />
      </div>

      <div class="container mt-4">
        <h5>User Quiz Participation</h5>
        <img
          v-if="charts.length"
          class="img-fluid"
          :src="`http://localhost:5000${charts[0]}`"
          alt="User Participation Chart"
        />
      </div>

      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminSummaryPage',
  data() {
    return {
      charts: [],
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
        .get('http://localhost:5000/api/admin/summary', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          this.charts = response.data.charts // Keep `/static/...` paths
        })
        .catch(err => {
          console.error('Error loading summary:', err)
          this.error = 'Failed to load summary charts.'
        })
    },
    goBack() {
      this.$router.push('/admin-dashboard')
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
