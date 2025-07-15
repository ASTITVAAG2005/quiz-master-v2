<template>
  <div>
    <!-- Navbar -->
 <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <!-- Left Side: Brand -->
    <a class="navbar-brand me-auto" href="#">
  Welcome {{ user?.fullname || 'User' }}, to Quiz Master
</a>
    <!-- Center: Search Bar -->
    <div class="mx-auto" style="width: 300px;">
      <form @submit.prevent="search" class="d-flex">
        <div class="input-group input-group-sm">
          <input type="text" class="form-control" v-model="query" placeholder="Search subjects or quizzes..." />
          <button class="btn btn-primary" type="submit">🔍</button>
        </div>
      </form>
    </div>

    <!-- Right Side: Buttons -->
    <div class="d-flex ms-auto">
      <button class="btn btn-info me-2 btn-sm" @click="goToSummary">📊 Summary</button>
      <button class="btn btn-warning me-2 btn-sm" @click="goToScores">View Scores</button>
      <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
    </div>
  </div>
</nav>


        <!-- Search Results Modal -->
    <div v-if="showSearchModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">

        <div class="modal-header">
            <h5 class="modal-title">Search Results for "{{ query }}"</h5>
            <button type="button" class="btn-close" @click="showSearchModal = false"></button>
        </div>

        <div class="modal-body">
            <template v-if="hasSearchResults">
            <div v-if="searchResults.subjects.length">
                <h5>Subjects</h5>
                <ul class="list-group mb-3">
                <li v-for="s in searchResults.subjects" :key="s.id" class="list-group-item">
                    {{ s.name }}
                </li>
                </ul>
            </div>

            <div v-if="searchResults.chapters.length">
                <h5>Chapters</h5>
                <ul class="list-group mb-3">
                <li v-for="c in searchResults.chapters" :key="c.id" class="list-group-item">
                    {{ c.name }}
                </li>
                </ul>
            </div>

            <div v-if="searchResults.quizzes.length">
                <h5>Quizzes</h5>
                <ul class="list-group mb-3">
                <li v-for="q in searchResults.quizzes" :key="q.id" class="list-group-item">
                    {{ q.title }} (Total Questions: {{ q.total_questions }})
                </li>
                </ul>
            </div>

            <div v-if="searchResults.questions.length">
                <h5>Questions</h5>
                <ul class="list-group mb-3">
                <li v-for="q in searchResults.questions" :key="q.id" class="list-group-item">
                    {{ q.question }}
                </li>
                </ul>
            </div>
            </template>

            <p v-else class="text-muted">No results found for "{{ query }}".</p>
        </div>
        </div>
    </div>
    </div>


    <!-- Quizzes -->
    <div class="container mt-4">
      <h5>Upcoming Quizzes</h5>
      <div v-if="quizzes.length">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Subject</th>
              <th>Chapter</th>
              <th>No. of Questions</th>
              <th>Scheduled Date</th>
              <th>Duration(HH:MM)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.quiz.id">
              <td>{{ quiz.quiz.id }}</td>
              <td>{{ quiz.subject.name }}</td>
              <td>{{ quiz.chapter.name }}</td>
              <td>{{ quiz.quiz.total_questions }}</td>
              <td>{{ formatDate(quiz.quiz.date) }}</td>
              <td>{{ quiz.quiz.duration }}</td>
              <td>
                <button class="btn btn-info btn-sm" @click="openModal(quiz.quiz.id)">View</button>
                <span v-if="quiz.is_expired" class="badge bg-danger">Deadline passed</span>
                <button v-else class="btn btn-success btn-sm" @click="startQuiz(quiz.quiz.id)">Start</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Modal -->
        <div v-if="selectedQuiz" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Quiz Details</h5>
                <button type="button" class="btn-close" @click="selectedQuiz = null"></button>
            </div>
            <div class="modal-body">
                <p><strong>ID:</strong> {{ selectedQuiz.quiz.id }}</p>
                <p><strong>Subject:</strong> {{ selectedQuiz.subject.name }}</p>
                <p><strong>Chapter:</strong> {{ selectedQuiz.chapter.name }}</p>
                <p><strong>No. of Questions:</strong> {{ selectedQuiz.quiz.total_questions }}</p>
                <p><strong>Scheduled Date:</strong> {{ formatDate(selectedQuiz.quiz.date) }}</p>
                <p><strong>Duration (HH:MM) :</strong> {{ selectedQuiz.quiz.duration }}</p>
                <p v-if="selectedQuiz.is_expired" class="text-danger"><strong>⚠ This quiz is no longer available.</strong></p>
            </div>
            </div>
        </div>
        </div>


      </div>
      <p v-else>No upcoming quizzes available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data() {
    return {
      query: '',
      subjects: [],
      quizzes: [],
      selectedQuiz: null,
      error: null,
      user: null, 
      searchResults: {
        subjects: [],
        chapters: [],
        quizzes: [],
        questions: []
      },
      showSearchModal: false
    }
  },
  mounted() {
    this.fetchUserData()
  },
  computed: {
    hasSearchResults() {
      const r = this.searchResults
      return r.subjects.length || r.chapters.length || r.quizzes.length || r.questions.length
    }
  },
  methods: {
    fetchUserData() {
      const token = localStorage.getItem('access_token')
      axios.get('http://localhost:5000/api/user/dashboard', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => {
        this.user = res.data.user
        this.subjects = res.data.subjects
        this.quizzes = res.data.upcoming_quizzes
      }).catch(err => {
        console.error('Error loading user dashboard:', err)
        this.error = 'Failed to load user data.'
      })
    },
    search() {
      const token = localStorage.getItem('access_token')
      if (!this.query.trim()) return

      axios.get(`http://localhost:5000/api/admin/search?q=${encodeURIComponent(this.query)}`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => {
        this.searchResults = res.data
        this.showSearchModal = true
      }).catch(err => {
        console.error('Search error:', err)
        this.error = 'Failed to search.'
      })
    },
    goToSummary() {
      this.$router.push('/user/summary')
    },
    goToScores() {
      this.$router.push('/user/quiz-scores')
    },
    logout() {
      const token = localStorage.getItem('access_token')
      axios.post('http://localhost:5000/api/logout', {}, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(() => {
        localStorage.removeItem('access_token')
        this.$router.push('/')
      })
    },
    openModal(quizId) {
      this.selectedQuiz = this.quizzes.find(q => q.quiz.id === quizId)
    },
    startQuiz(quizId) {
      this.$router.push(`/quiz/start/${quizId}`) 
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-GB') // 'dd-mm-yyyy'
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
