<template>
  <div v-if="query">
    <h4>Search Results for "{{ query }}"</h4>

    <div v-if="results.users?.length">
      <h5>Users</h5>
      <ul class="list-group mb-3">
        <li class="list-group-item" v-for="user in results.users" :key="user.UserID">
          <strong>{{ user.Username }}</strong> ({{ user.Email }})
        </li>
      </ul>
    </div>

    <div v-if="results.subjects?.length">
      <h5>Subjects</h5>
      <ul class="list-group mb-3">
        <li class="list-group-item" v-for="subject in results.subjects" :key="subject.SubjectID">
          {{ subject.Subjectname }}
        </li>
      </ul>
    </div>

    <div v-if="results.quizzes?.length">
      <h5>Quizzes</h5>
      <ul class="list-group mb-3">
        <li class="list-group-item" v-for="quiz in results.quizzes" :key="quiz.QuizID">
          Quiz ID: {{ quiz.QuizID }} - Chapter: {{ quiz.chapter.Chaptername }}
        </li>
      </ul>
    </div>

    <div v-if="results.questions?.length">
      <h5>Questions</h5>
      <ul class="list-group mb-3">
        <li class="list-group-item" v-for="q in results.questions" :key="q.QuestionID">
          {{ q.Question_statement }}
        </li>
      </ul>
    </div>

    <p v-if="noResults" class="text-muted">No results found for "{{ query }}".</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SearchResults',
  props: ['query'],
  data() {
    return {
      results: {
        users: [],
        subjects: [],
        quizzes: [],
        questions: [],
        chapters: []
      },
      loading: false,
      error: ''
    }
  },
  computed: {
    noResults() {
      return !this.results.users?.length &&
             !this.results.subjects?.length &&
             !this.results.quizzes?.length &&
             !this.results.questions?.length &&
             !this.results.chapters?.length
    }
  },
  mounted() {
    if (this.query?.trim()) {
      this.search()
    }
  },
  watch: {
    query(newQuery, oldQuery) {
      if (newQuery && newQuery !== oldQuery) {
        this.search()
      }
    }
  },
  methods: {
    search() {
      const token = localStorage.getItem("access_token")
      this.loading = true
      axios.get(`http://localhost:5000/api/admin/dashboard?query=${this.query}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(res => {
        this.results = {
          users: res.data.users || [],
          subjects: res.data.subjects || [],
          quizzes: res.data.quizzes || [],
          questions: res.data.questions || [],
          chapters: res.data.chapters || []
        }
      })
      .catch(err => {
        this.error = "Failed to fetch search results"
        console.error("Search error:", err)
      })
      .finally(() => {
        this.loading = false
      })
    }
  }
}
</script>

