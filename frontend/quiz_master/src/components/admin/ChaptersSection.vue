<template>
  <div class="card mt-3">
    <div class="card-header bg-info text-dark fw-bold">
      Manage Chapters
      <button class="btn btn-sm btn-light float-end" @click="showAddModal = true">+ Add Chapter</button>
    </div>

    <div class="card-body">
      <ul v-if="chapters.length" class="list-group">
        <li v-for="chapter in chapters" :key="chapter.id" class="list-group-item">
          <strong>{{ getSubjectName(chapter.subject_id) }}</strong> → {{ chapter.name }} - {{ chapter.description }}
          <button class="btn btn-warning btn-sm float-end mx-1" @click="openEditModal(chapter)">Edit</button>
          <button class="btn btn-danger btn-sm float-end" @click="deleteChapter(chapter.id)">Delete</button>
        </li>
      </ul>
      <p v-else>No chapters available.</p>
    </div>

    <!-- Add Chapter Modal -->
    <div class="modal fade" :class="{ show: showAddModal }" style="display: block" v-if="showAddModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Chapter</h5>
            <button type="button" class="btn-close" @click="showAddModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addChapter">
              <div class="mb-3">
                <label class="form-label">Select Subject</label>
                <select class="form-control" v-model="newChapter.subject_id" required>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter Name</label>
                <input v-model="newChapter.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="newChapter.description" class="form-control" required></textarea>
              </div>
              <button type="submit" class="btn btn-warning">Add Chapter</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Chapter Modal -->
    <div class="modal fade" :class="{ show: showEditModal }" style="display: block" v-if="showEditModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Chapter</h5>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateChapter">
              <div class="mb-3">
                <label class="form-label">Select Subject</label>
                <select class="form-control" v-model="editedChapter.subject_id" required>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter Name</label>
                <input v-model="editedChapter.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="editedChapter.description" class="form-control" required></textarea>
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
  name: 'ChaptersSection',
  props: ['subjects'],
  data() {
    return {
      chapters: [],
      loading: false,
      error: '',
      showAddModal: false,
      showEditModal: false,
      newChapter: {
        subject_id: '',
        name: '',
        description: ''
      },
      editedChapter: {
        id: null,
        subject_id: '',
        name: '',
        description: ''
      }
    }
  },
  mounted() {
    this.fetchChapters()
  },
  methods: {
    getSubjectName(subjectId) {
      const subj = this.subjects.find(s => s.id === subjectId)
      return subj ? subj.name : 'Unknown Subject'
    },

    fetchChapters() {
      const token = localStorage.getItem("access_token")
      this.loading = true
  axios.get("https://quiz-master-v2-giuh.onrender.com/api/admin/chapters", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        this.chapters = res.data
      })
      .catch(err => {
        this.error = 'Failed to fetch chapters'
        console.error("Error fetching chapters:", err.response?.data || err)
      })
      .finally(() => {
        this.loading = false
      })
    },

    addChapter() {
      const token = localStorage.getItem("access_token")
  axios.post("https://quiz-master-v2-giuh.onrender.com/api/admin/chapters", this.newChapter, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchChapters()
        this.$emit('refresh') 
        this.newChapter = { subject_id: '', name: '', description: '' }
        this.showAddModal = false
      })
      .catch(err => {
        this.error = 'Failed to add chapter'
        console.error("Error adding chapter:", err.response?.data || err)
      })
    },

    openEditModal(chapter) {
      this.editedChapter = { ...chapter } // Clone the object
      this.showEditModal = true
    },

    updateChapter() {
      const token = localStorage.getItem("access_token")
      
  axios.put(`https://quiz-master-v2-giuh.onrender.com/api/admin/chapters/${this.editedChapter.id}`, {
        name: this.editedChapter.name,
        subject_id: this.editedChapter.subject_id,
        description: this.editedChapter.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchChapters()
        this.showEditModal = false
        this.editedChapter = { id: null, subject_id: '', name: '', description: '' }
        this.$emit('refresh')
      })
      .catch(err => {
        this.error = 'Failed to update chapter'
        console.error("Error updating chapter:", err.response?.data || err)
      })
    },

    deleteChapter(id) {
      const token = localStorage.getItem("access_token")
  axios.delete(`https://quiz-master-v2-giuh.onrender.com/api/admin/chapters/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        this.fetchChapters()
        this.$emit('refresh') 
      })
      .catch(err => {
        this.error = 'Failed to delete chapter'
        console.error("Error deleting chapter:", err.response?.data || err)
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
