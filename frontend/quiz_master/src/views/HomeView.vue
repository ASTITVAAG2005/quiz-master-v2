<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">Quiz Master</a>
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" :class="{ show: navbarOpen }">
          <button class="btn btn-danger mx-2" @click="showAdminModal = true">Admin Login</button>
          <button class="btn btn-primary mx-2" @click="showUserModal = true">User Login</button>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <div class="container text-center mt-5">
      <!-- Welcome Text -->
      <h1>Welcome to Quiz Master</h1>
      <h6>Dare to challenge your mind? Step in and find out!</h6>

      <!-- Image -->
      <div class="d-flex justify-content-center">
        <img src="@/assets/Student_exam_cartoon2.jpg" alt="Student Exam Cartoon" class="img-fluid mt-3" />
      </div>

      <!-- Signup -->
      <div class="mt-5">
        <p style="font-size: 1.2rem; font-weight: bold; color: #333;">
          New here? No worries! <br />Create an account and start your journey :)
        </p>
        <button class="btn btn-success" @click="showSignupModal = true">Sign Up as a User</button>
      </div>

      <!-- Modals -->
      <AdminLoginModal v-if="showAdminModal" @close="showAdminModal = false" />
      <UserLoginModal v-if="showUserModal" @close="showUserModal = false" />
      <UserSignupModal v-if="showSignupModal" @close="showSignupModal = false" />
    </div>
  </div>
</template>

<script>
import AdminLoginModal from '@/components/AdminLoginModal.vue';
import UserLoginModal from '@/components/UserLoginModal.vue';
import UserSignupModal from '@/components/UserSignupModal.vue';

export default {
  name: 'HomeView',
  components: {
    AdminLoginModal,
    UserLoginModal,
    UserSignupModal
  },
  data() {
    return {
      navbarOpen: false,
      showAdminModal: false,
      showUserModal: false,
      showSignupModal: false
    };
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen;
    }
  }
};
</script>

<style scoped>
/* Optional: Remove body margin if present globally */
body {
  margin: 0;
}
</style>
