<template>
  <div class="card mt-3">
    <div class="card-header bg-info text-dark fw-bold">
      Manage Subjects
      <button class="btn btn-sm btn-light float-end" @click="showAddSubjectModal = true">+ Add Subject</button>
    </div>
    <div class="card-body">
      <ul v-if="subjects.length" class="list-group">
        <li v-for="subject in subjects" :key="subject.id" class="list-group-item">
          <strong>{{ subject.name }}</strong> - {{ subject.description }}
          <button class="btn btn-warning btn-sm float-end mx-1" @click="openEditModal(subject)">Edit</button>
          <button class="btn btn-danger btn-sm float-end" @click="deleteSubject(subject.id)">Delete</button>
        </li>
      </ul>
      <p v-else>No subjects available.</p>
    </div>

    <!-- Add Subject Modal -->
    <div class="modal fade" :class="{ show: showAddSubjectModal }" style="display: block;" v-if="showAddSubjectModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Subject</h5>
            <button type="button" class="btn-close" @click="showAddSubjectModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSubject">
              <div class="mb-3">
                <label class="form-label">Subject Name</label>
                <input v-model="newSubject.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="newSubject.description" class="form-control" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Add Subject</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Subject Modal -->
    <div class="modal fade" :class="{ show: showEditSubjectModal }" style="display: block;" v-if="showEditSubjectModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Subject</h5>
            <button type="button" class="btn-close" @click="showEditSubjectModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateSubject">
              <div class="mb-3">
                <label class="form-label">Subject Name</label>
                <input v-model="editedSubject.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="editedSubject.description" class="form-control" required></textarea>
              </div>
              <button type="submit" class="btn btn-success">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubjectsSection',
  data() {
    return {
      subjects: [],
      showAddSubjectModal: false,
      showEditSubjectModal: false,
      newSubject: {
        name: '',
        description: ''
      },
      editedSubject: {
        id: null,
        name: '',
        description: ''
      },
      loading: false,
      error: ''
    }
  },
  mounted() {
    this.fetchSubjects()
  },
  methods: {
    fetchSubjects() {
      const token = localStorage.getItem("access_token")
      this.loading = true
      axios.get('http://localhost:5000/api/admin/subjects', {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        this.subjects = res.data.subjects || res.data
      })
      .catch(err => {
        this.error = 'Failed to fetch subjects'
        console.error('Error fetching subjects:', err.response?.data || err)
      })
      .finally(() => { this.loading = false })
    },

    addSubject() {
      const token = localStorage.getItem("access_token")
      axios.post('http://localhost:5000/api/admin/subjects', this.newSubject, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchSubjects()
        this.$emit('refresh') 
        this.showAddSubjectModal = false
        this.newSubject = { name: '', description: '' }
      })
      .catch(err => {
        this.error = 'Failed to add subject'
        console.error('Error adding subject:', err.response?.data || err)
      })
    },

    openEditModal(subject) {
      this.editedSubject = { ...subject }
      this.showEditSubjectModal = true
    },

    updateSubject() {
      const token = localStorage.getItem("access_token")
      axios.put(`http://localhost:5000/api/admin/subjects/${this.editedSubject.id}`, {
        name: this.editedSubject.name,
        description: this.editedSubject.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchSubjects()
        this.$emit('refresh') 
        this.showEditSubjectModal = false
        this.editedSubject = { id: null, name: '', description: '' }
      })
      .catch(err => {
        this.error = 'Failed to update subject'
        console.error('Error updating subject:', err.response?.data || err)
      })
    },

    deleteSubject(id) {
      const token = localStorage.getItem("access_token")
      axios.delete(`http://localhost:5000/api/admin/subjects/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchSubjects()
        this.$emit('refresh')
      })
      .catch(err => {
        this.error = 'Failed to delete subject'
        console.error('Delete error:', err.response?.data || err)
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
