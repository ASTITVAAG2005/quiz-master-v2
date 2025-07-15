<template>
  <div class="card mt-3">
    <div class="card-header bg-info text-dark fw-bold">
      Manage Questions
      <button class="btn btn-sm btn-light float-end" @click="showAddQuestionModal = true">+ Add Question</button>
    </div>
    <div class="card-body">
      <template v-if="quizzes.length">
        <div v-for="quiz in quizzes" :key="quiz.id">
          <p>
            <strong>{{ quiz.chapter?.subject?.Subjectname }} → {{ quiz.chapter?.Chaptername }}</strong> -
            {{ formatDate(quiz.date) }}
          </p>
          <ul class="list-group">
            <li v-for="q in questions.filter(q => q.quiz_id === quiz.id)" :key="q.id" class="list-group-item">
              {{ q.question }}
              <button class="btn btn-warning btn-sm float-end mx-1" @click="startEdit(q)">Edit</button>
              <button class="btn btn-danger btn-sm float-end" @click="deleteQuestion(q.id)">Delete</button>
            </li>
          </ul>
        </div>
      </template>
      <p v-else>No questions available.</p>
    </div>

    <!-- Add Question Modal -->
    <div class="modal fade" :class="{ show: showAddQuestionModal }" style="display: block;" v-if="showAddQuestionModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Question</h5>
            <button type="button" class="btn-close" @click="showAddQuestionModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addQuestion">
              <div class="mb-3">
                <label class="form-label">Select Quiz</label>
                <select class="form-control" v-model="newQuestion.quiz_id" required>
                  <option v-for="quiz in quizzes" :value="quiz.id" :key="quiz.id">
                    {{ quiz.chapter?.Chaptername }} - {{ formatDate(quiz.date) }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Question</label>
                <input v-model="newQuestion.question" type="text" class="form-control" required />
              </div>
              <div v-for="n in 4" :key="n" class="mb-3">
                <label class="form-label">Option {{ n }}</label>
                <input v-model="newQuestion[`option${n}`]" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select class="form-control" v-model="newQuestion.correct_option" required>
                  <option v-for="n in 4" :key="n" :value="n">Option {{ n }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Add Question</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Question Modal -->
    <div class="modal fade" :class="{ show: showEditQuestionModal }" style="display: block;" v-if="showEditQuestionModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Question</h5>
            <button type="button" class="btn-close" @click="showEditQuestionModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateQuestion">
              <div class="mb-3">
                <label class="form-label">Question</label>
                <input v-model="editedQuestion.question" type="text" class="form-control" required />
              </div>
              <div v-for="n in 4" :key="n" class="mb-3">
                <label class="form-label">Option {{ n }}</label>
                <input v-model="editedQuestion[`option${n}`]" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select class="form-control" v-model="editedQuestion.correct_option" required>
                  <option v-for="n in 4" :key="n" :value="n">Option {{ n }}</option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import dayjs from 'dayjs'

export default {
  name: 'QuestionsSection',
  props: ['quizzes'],
  data() {
    return {
      questions: [],
      loading: false,
      error: '',
      showAddQuestionModal: false,
      showEditQuestionModal: false,
      newQuestion: {
        quiz_id: '',
        question: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        correct_option: ''
      },
      editedQuestion: null
    }
  },
  mounted() {
    this.fetchQuestions()
  },
  methods: {
    formatDate(date) {
      return dayjs(date).format('DD-MM-YYYY')
    },

    fetchQuestions() {
      const token = localStorage.getItem('access_token')
      this.loading = true
      axios.get('http://localhost:5000/api/admin/questions', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(res => {
        this.questions = res.data
      })
      .catch(err => {
        this.error = 'Failed to fetch questions'
        console.error('Error fetching questions:', err)
      })
      .finally(() => {
        this.loading = false
      })
    },

    addQuestion() {
      const token = localStorage.getItem('access_token')
      axios.post('http://localhost:5000/api/admin/questions', this.newQuestion, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        this.fetchQuestions()
        this.newQuestion = {
          quiz_id: '',
          question: '',
          option1: '',
          option2: '',
          option3: '',
          option4: '',
          correct_option: ''
        }
        this.showAddQuestionModal = false
      })
      .catch(err => {
        this.error = 'Failed to add question'
        console.error('Error adding question:', err)
      })
    },

    deleteQuestion(id) {
      const token = localStorage.getItem('access_token')
      axios.delete(`http://localhost:5000/api/admin/questions/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        this.fetchQuestions()
      })
      .catch(err => {
        this.error = 'Failed to delete question'
        console.error('Error deleting question:', err)
      })
    },

    startEdit(question) {
      this.editedQuestion = { ...question }
      this.showEditQuestionModal = true
    },

    updateQuestion() {
      const token = localStorage.getItem('access_token')
      axios.put(`http://localhost:5000/api/admin/questions/${this.editedQuestion.id}`, this.editedQuestion, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        this.fetchQuestions()
        this.showEditQuestionModal = false
        this.editedQuestion = null
      })
      .catch(err => {
        this.error = 'Failed to update question'
        console.error('Error updating question:', err)
      })
    }
  }
}
</script>
