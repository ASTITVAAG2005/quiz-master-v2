<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h4>Registered Users</h4>
      <router-link to="/admin-dashboard" class="btn btn-primary">Back to Dashboard</router-link>
    </div>

    <form @submit.prevent="searchUsers" class="mb-3 d-flex justify-content-center">
      <div class="input-group" style="max-width: 400px;">
        <input type="text" class="form-control form-control-sm" v-model="query" placeholder="Search users..." />
        <button class="btn btn-sm btn-primary" type="submit">🔍</button>
      </div>
    </form>

    <!-- <div v-if="query" class="mb-3">
      <h5>Search Results for "{{ query }}"</h5>
      <p v-if="filteredUsers.length === 0" class="text-muted">No results found.</p>
    </div> -->

    <div class="card">
      <div class="card-header bg-success text-white">Users</div>
      <div class="card-body">
        <div v-if="filteredUsers.length" class="table-responsive">
          <table class="table table-hover">
            <thead class="table-dark">
              <tr>
                <th>Username</th>
                <th>Full Name</th>
                <th>Email</th>
                <th>Qualification</th>
                <th>DOB</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.fullname }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.qualification }}</td>
                <td>{{ formatDate(user.dob) }}</td>
                <td>{{ user.role }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">No users to display.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import dayjs from 'dayjs'

export default {
  name: 'ViewUsers',
  data() {
    return {
      users: [],
      query: '',
      loading: false,
      error: ''
    }
  },
  computed: {
    filteredUsers() {
      if (!this.query) return this.users
      const q = this.query.toLowerCase()
      return this.users.filter(
        u =>
          u.username.toLowerCase().includes(q) ||
          u.email.toLowerCase().includes(q) ||
          (u.fullname && u.fullname.toLowerCase().includes(q))
      )
    }
  },
  mounted() {
    this.fetchUsers()
  },
  methods: {
    formatDate(dateStr) {
      return dateStr ? dayjs(dateStr).format('DD-MM-YYYY') : 'N/A'
    },
    fetchUsers() {
      const token = localStorage.getItem('access_token')
      this.loading = true
      axios
        .get('http://localhost:5000/api/admin/users', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(res => {
          this.users = res.data.users
        })
        .catch(err => {
          console.error('Failed to fetch users:', err)
          this.error = 'Error loading user data'
        })
        .finally(() => {
          this.loading = false
        })
    },
    searchUsers() {
      // Filtering is done client-side via computed property
    }
  }
}
</script>

<style scoped>
.table-responsive {
  max-height: 500px;
  overflow-y: auto;
}
</style>
