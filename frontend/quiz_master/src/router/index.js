import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import ViewUsers from '@/components/admin/ViewUsers.vue'  
import AdminSummaryPage from '@/components/admin/AdminSummaryPage.vue'
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
