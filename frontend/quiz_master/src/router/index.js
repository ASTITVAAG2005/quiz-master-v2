import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import ViewUsers from '@/components/admin/ViewUsers.vue'  
import AdminSummaryPage from '@/components/admin/AdminSummaryPage.vue'

import UserDashboard from '@/components/user/UserDashboard.vue'
import UserSummaryPage from '@/components/user/UserSummaryPage.vue'
import UserQuizScore from '@/components/user/UserQuizScore.vue'
import AttemptQuiz from '@/components/user/AttemptQuiz.vue'  

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/admin/view-users',       
    name: 'ViewUsers',
    component: ViewUsers
  },
  {
    path: '/admin/summary',
    name: 'AdminSummary',
    component: AdminSummaryPage
  },
  {
    path: '/user-dashboard',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/user/summary',
    name: 'UserSummary',
    component: UserSummaryPage
  },
  {
    path: '/user/quiz-scores',
    name: 'UserQuizScore',
    component: UserQuizScore
  },
  {
    path: '/quiz/start/:quiz_id',         
    name: 'AttemptQuiz',
    component: AttemptQuiz
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
