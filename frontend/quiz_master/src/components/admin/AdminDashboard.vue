<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="container mt-3">
          <form @submit.prevent="search" class="d-flex justify-content-center">
            <div class="input-group" style="width: 300px;">
              <input type="text" class="form-control form-control-sm" v-model="query" placeholder="Search subjects, quizzes, or questions..." />
              <button class="btn btn-sm btn-primary" type="submit">🔍</button>
            </div>
          </form>
        </div>

        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <button class="btn btn-info me-3" @click="goToSummary">Summary</button>
          <button class="btn btn-info me-3" @click="goToUsers">View Users</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <h2>Welcome, Admin</h2>

      <SubjectsSection :subjects="subjects" @refresh="fetchData" />
      <ChaptersSection :chapters="chapters" :subjects="subjects" @refresh="fetchData" />
      <QuizzesSection :quizzes="quizzes" :chapters="chapters" @refresh="fetchData" />
      <QuestionsSection :quizzes="quizzes" @refresh="fetchData" />
      <SearchResults
  ref="searchResults"
  v-if="query"
  :query="query"
  :results="searchResults"
/>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SubjectsSection from '@/components/admin/SubjectsSection.vue'
import ChaptersSection from '@/components/admin/ChaptersSection.vue'
import QuizzesSection from '@/components/admin/QuizzesSection.vue'
import QuestionsSection from '@/components/admin/QuestionsSection.vue'
import SearchResults from '@/components/admin/SearchResults.vue'

export default {
  name: 'AdminDashboard',
  components: {
    SubjectsSection,
    ChaptersSection,
    QuizzesSection,
    QuestionsSection,
    SearchResults
  },
  data() {
    return {
      subjects: [],
      chapters: [],
      quizzes: [],
      query: '',
      searchResults: {},
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      const token = localStorage.getItem('access_token')
      this.loading = true
      this.error = null

      Promise.all([
        axios.get('http://localhost:5000/api/admin/subjects', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/admin/chapters', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/api/admin/quizzes', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])
        .then(([subjectsRes, chaptersRes, quizzesRes]) => {
          this.subjects = subjectsRes.data
          this.chapters = chaptersRes.data
          this.quizzes = quizzesRes.data
        })
        .catch(error => {
          console.error('Error fetching dashboard data:', error)
          this.error = 'Failed to load admin data.'
        })
        .finally(() => {
          this.loading = false
        })
    },
    search() {
  const token = localStorage.getItem('access_token');
  const cleanQuery = this.query.trim();
  if (!cleanQuery) return;

  axios
    .get(`http://localhost:5000/api/admin/search?q=${encodeURIComponent(cleanQuery)}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      this.searchResults = {
        subjects: res.data.subjects || [],
        chapters: res.data.chapters || [],
        quizzes: res.data.quizzes || [],
        questions: res.data.questions || []
      };

      // Show the modal
      this.$nextTick(() => {
    this.$refs.searchResults?.showModal();
  });
    })
    .catch(error => {
      console.error('Error during search:', error);
      this.error = 'Search failed.';
    });
},
    goToSummary() {
      this.$router.push('/admin/summary')
    },
    goToUsers() {
      this.$router.push('/admin/view-users')
    },
    logout() {
      const token = localStorage.getItem('access_token')
      axios
        .post('http://localhost:5000/api/logout', {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          localStorage.removeItem('access_token')
          this.$router.push('/')
        })
        .catch(error => {
          console.error('Logout failed:', error)
        })
    }
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-dialog {
  margin-top: 10%;
}
</style>