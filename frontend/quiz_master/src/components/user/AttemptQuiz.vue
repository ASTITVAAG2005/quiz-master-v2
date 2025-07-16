<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Quiz Master</a>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="container mt-4">
      <h2 class="text-center">Quiz: {{ quiz.chapter }}</h2>

      <div class="alert alert-warning text-center">
        ⏳ Time Left: <span>{{ formattedTime }}</span>
      </div>

      <form @submit.prevent="submitQuiz">
        <div v-for="(q, index) in quiz.questions" :key="q.id" class="card my-3">
          <div class="card-body">
            <h5>Q{{ index + 1 }}: {{ q.statement }}</h5>
            <div v-for="option in q.options" :key="option" class="form-check">
              <input
                class="form-check-input"
                type="radio"
                :name="`answer-${q.id}`"
                :value="option"
                v-model="userAnswers[q.id]"
                required
              />
              <label class="form-check-label">{{ option }}</label>
            </div>
          </div>
        </div>

        <button type="submit" class="btn btn-success w-100">Submit Quiz</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AttemptQuiz',
  data() {
    return {
      quiz: {
        chapter: '',
        questions: [],
        duration: '00:00',
      },
      userAnswers: {},
      timer: 0,
      timerInterval: null,
    }
  },
  computed: {
    formattedTime() {
      const h = Math.floor(this.timer / 3600).toString().padStart(2, '0')
      const m = Math.floor((this.timer % 3600) / 60).toString().padStart(2, '0')
      const s = (this.timer % 60).toString().padStart(2, '0')
      return `${h}:${m}:${s}`
    }
  },
  mounted() {
    this.loadQuiz()
  },
  methods: {
    loadQuiz() {
      const token = localStorage.getItem('access_token')
      const quizId = this.$route.params.quiz_id

      axios.get(`http://localhost:5000/api/user/quiz/${quizId}/start`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => {
        const q = res.data.quiz
        this.quiz = {
          chapter: q.title || `Quiz ${quizId}`,
          duration: q.duration || '00:30',
          questions: q.questions.map(q => ({
            id: q.id,
            statement: q.statement,
            options: q.options
          }))
        }
        this.initTimer(quizId, this.quiz.duration)
      }).catch(err => {
        console.error('Failed to start quiz:', err)
        alert('Could not start quiz.')
        this.$router.push('/user-dashboard')
      })
    },
    initTimer(quizId, duration) {
      const [h, m] = duration.split(':').map(Number)
      const total = h * 3600 + m * 60
      const stored = sessionStorage.getItem(`quiz_timer_${quizId}`)
      this.timer = stored ? parseInt(stored) : total

      this.timerInterval = setInterval(() => {
        if (this.timer > 0) {
          this.timer--
          sessionStorage.setItem(`quiz_timer_${quizId}`, this.timer)
        } else {
          clearInterval(this.timerInterval)
          this.submitQuiz()
        }
      }, 1000)
    },
    submitQuiz() {
      const quizId = this.$route.params.quiz_id
      const token = localStorage.getItem('access_token')

      axios.post(`http://localhost:5000/api/user/quiz/${quizId}/submit`, {
        answers: this.userAnswers
      }, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => {
        clearInterval(this.timerInterval)
        sessionStorage.removeItem(`quiz_timer_${quizId}`)
        alert(`Quiz Submitted! Your Score: ${res.data.score.toFixed(2)}%`)
        this.$router.push('/user/quiz-scores')
      }).catch(() => {
        alert('Failed to submit quiz.')
      })
    },
    logout() {
      const token = localStorage.getItem('access_token')
      axios.post('http://localhost:5000/api/logout', {}, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(() => {
        localStorage.removeItem('access_token')
        this.$router.push('/')
      })
    }
  },
  beforeUnmount() {
    clearInterval(this.timerInterval)
  }
}
</script>

<style scoped>
.card {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
