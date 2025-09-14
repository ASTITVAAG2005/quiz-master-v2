<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container d-flex justify-content-between align-items-center">
        <a class="navbar-brand" href="#">Quiz Master</a>

        <!-- Right side buttons -->
        <div class="d-flex align-items-center gap-2">
          <button class="btn btn-success" @click="exportScores">Export as CSV</button>
          <button class="btn btn-primary" @click="goBack">Back to Dashboard</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <h5>Your Past Quiz Scores</h5>

      <div v-if="scores.length">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Quiz</th>
              <th>Chapter</th>
              <th>Subject</th>
              <th>Date and Time</th>
              <th>Score</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="score in scores" :key="score.score_id">
              <td>{{ score.quiz_id }}</td>
              <td>{{ score.chapter_name }}</td>
              <td>{{ score.subject_name }}</td>
              <td>{{ score.timestamp }}</td>
              <td>{{ score.total_score.toFixed(2) }}%</td>
              <td>
                <button class="btn btn-info btn-sm" @click="openAnswersModal(score)">View Answers</button>
                <span v-if="score.retake_allowed">
                  <button class="btn btn-warning btn-sm" @click="retakeQuiz(score.quiz_id)">Retake Quiz</button>
                </span>
                <span v-else class="text-success">Passed</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No quiz attempts found.</p>
    </div>

    <!-- Modal for viewing answers -->
    <div v-if="selectedScore" class="modal fade show d-block" style="background-color: rgba(0,0,0,0.5);" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Answers - {{ selectedScore.quiz_id }}</h5>
            <button type="button" class="btn-close" @click="selectedScore = null"></button>
          </div>
          <div class="modal-body">
            <div v-for="question in selectedScore.questions" :key="question.id" class="mb-3">
              <p><strong>Q:</strong> {{ question.statement }}</p>

              <p :style="{ color: question.user_answer === question.correct_answer ? 'green' : 'red' }">
                <strong>Your Answer:</strong> {{ question.user_answer || 'Not Answered' }}
              </p>

              <p><strong>Correct Answer:</strong> {{ question.correct_answer }}</p>
              <hr />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserQuizScore',
  data() {
    return {
      scores: [],
      selectedScore: null,
      error: ''
    }
  },
  mounted() {
    this.fetchScores()
  },
  methods: {
    fetchScores() {
      const token = localStorage.getItem('access_token')
  axios.get('https://quiz-master-v2-giuh.onrender.com/api/user/scores', {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        this.scores = res.data.scores
      })
      .catch(err => {
        console.error('Failed to fetch scores:', err)
        this.error = 'Error loading scores.'
      })
    },
    exportScores() {
    const token = localStorage.getItem('access_token')
  axios.get('https://quiz-master-v2-giuh.onrender.com/api/user/export-scores', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      const filename = res.data.filename
  const downloadUrl = `https://quiz-master-v2-giuh.onrender.com/static/exports/${filename}`
      window.open(downloadUrl, '_blank')
    })
    .catch(err => {
      console.error('Export failed:', err)
    })
  },
    openAnswersModal(score) {
      this.selectedScore = score
    },
    retakeQuiz(quizId) {
      this.$router.push(`/quiz/start/${quizId}`)
    },
    goBack() {
      this.$router.push('/user-dashboard')
    }
  }
}
</script>

<style scoped>
.modal-dialog {
  margin-top: 10%;
}
</style>
