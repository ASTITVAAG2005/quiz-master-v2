<template>
  <div class="card mt-3">
    <div class="card-header bg-info text-dark fw-bold">
      Manage Quizzes
      <button class="btn btn-sm btn-light float-end" @click="openAddModal">+ Add Quiz</button>
    </div>
    <div class="card-body">
      <ul v-if="quizzes.length" class="list-group">
        <li v-for="quiz in quizzes" :key="quiz.id" class="list-group-item">
          <strong>{{ getChapterName(quiz.chapter_id) }}</strong> - Date: {{ formatDate(quiz.date) }} | Duration: {{ quiz.time_duration }}
          <button class="btn btn-warning btn-sm float-end mx-1" @click="openEditModal(quiz)">Edit</button>
          <button class="btn btn-danger btn-sm float-end" @click="deleteQuiz(quiz.id)">Delete</button>
        </li>
      </ul>
      <p v-else>No quizzes available.</p>
    </div>

    <!-- Add/Edit Quiz Modal -->
    <div class="modal fade" :class="{ show: showQuizModal }" style="display: block;" v-if="showQuizModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Quiz' : 'Add Quiz' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateQuiz() : addQuiz()">
              <div class="mb-3">
                <label class="form-label">Select Chapter</label>
                <select class="form-control" v-model="quizForm.chapter_id" required>
                  <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
                    {{ chapter.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Date of Quiz</label>
                <input type="date" class="form-control" v-model="quizForm.date" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Time Duration (HH:MM)</label>
                <input type="text" class="form-control" v-model="quizForm.time_duration" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Remarks</label>
                <textarea class="form-control" v-model="quizForm.remarks"></textarea>
              </div>
              <button type="submit" class="btn btn-info">{{ isEditMode ? 'Update' : 'Add' }} Quiz</button>
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
  name: 'QuizzesSection',
  props: ['chapters'],
  data() {
    return {
      quizzes: [],
      quizForm: {
        id: null,
        chapter_id: '',
        date: '',
        time_duration: '',
        remarks: ''
      },
      showQuizModal: false,
      isEditMode: false,
      error: ''
    }
  },
  mounted() {
    this.fetchQuizzes()
  },
  methods: {
    formatDate(date) {
      return dayjs(date).format('DD-MM-YYYY')
    },
    getChapterName(id) {
      const chapter = this.chapters.find(ch => ch.id === id)
      return chapter ? chapter.name : 'Unknown Chapter'
    },
    fetchQuizzes() {
      const token = localStorage.getItem('access_token')
      axios.get('http://localhost:5000/api/admin/quizzes', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(res => {
        this.quizzes = res.data
      }).catch(err => {
        this.error = 'Failed to fetch quizzes'
        console.error(err)
      })
    },
    openAddModal() {
      this.isEditMode = false
      this.quizForm = { id: null, chapter_id: '', date: '', time_duration: '', remarks: '' }
      this.showQuizModal = true
    },
    openEditModal(quiz) {
      this.isEditMode = true
      this.quizForm = { ...quiz }
      this.showQuizModal = true
    },
    closeModal() {
      this.showQuizModal = false
    },
    addQuiz() {
      const token = localStorage.getItem('access_token')
      axios.post('http://localhost:5000/api/admin/quizzes', this.quizForm, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(() => {
        this.fetchQuizzes()
        this.closeModal()
      }).catch(err => {
        this.error = 'Failed to add quiz'
        console.error(err)
      })
    },
    updateQuiz() {
      const token = localStorage.getItem('access_token')
      axios.put(`http://localhost:5000/api/admin/quizzes/${this.quizForm.id}`, this.quizForm, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(() => {
        this.fetchQuizzes()
        this.closeModal()
      }).catch(err => {
        this.error = 'Failed to update quiz'
        console.error(err)
      })
    },
    deleteQuiz(id) {
      const token = localStorage.getItem('access_token')
      axios.delete(`http://localhost:5000/api/admin/quizzes/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      }).then(() => {
        this.fetchQuizzes()
      }).catch(err => {
        this.error = 'Failed to delete quiz'
        console.error(err)
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
