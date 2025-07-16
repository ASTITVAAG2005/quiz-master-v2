<template>
  <div class="modal fade" tabindex="-1" ref="searchModal">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">Search Results for "{{ query }}"</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>

        <div class="modal-body">
          <template v-if="hasResults">
            <div v-if="results.subjects?.length">
              <h5>Subjects</h5>
              <ul class="list-group mb-3">
                <li v-for="s in results.subjects" :key="s.id" class="list-group-item">
                  {{ s.name }}
                </li>
              </ul>
            </div>

            <div v-if="results.chapters?.length">
              <h5>Chapters</h5>
              <ul class="list-group mb-3">
                <li v-for="c in results.chapters" :key="c.id" class="list-group-item">
                  {{ c.name }}
                </li>
              </ul>
            </div>

            <div v-if="results.quizzes?.length">
              <h5>Quizzes</h5>
              <ul class="list-group mb-3">
                <li v-for="q in results.quizzes" :key="q.id" class="list-group-item">
                  {{ q.title }} (Total Questions: {{ q.total_questions }})
                </li>
              </ul>
            </div>

            <div v-if="results.questions?.length">
              <h5>Questions</h5>
              <ul class="list-group mb-3">
                <li v-for="q in results.questions" :key="q.id" class="list-group-item">
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
</template>

<script>
import { Modal } from 'bootstrap'

export default {
  props: {
    query: String,
    results: Object
  },
  computed: {
    hasResults() {
      return ['subjects', 'chapters', 'quizzes', 'questions'].some(
        key => Array.isArray(this.results?.[key]) && this.results[key].length > 0
      );
    }
  },
  methods: {
    showModal() {
      const modalInstance = new Modal(this.$refs.searchModal);
      modalInstance.show();
    }
  }
}
</script>

<style scoped>
.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

/* ⏩ Speed up the fade animation */
.modal.fade .modal-dialog {
  transition: transform 0.15s ease-out !important;
}

.modal.fade.show {
  transition: opacity 0.15s linear !important;
}
</style>
