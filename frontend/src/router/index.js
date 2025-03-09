import { createRouter, createWebHistory } from 'vue-router'
import UsersListing from '@/views/UsersListing.vue'

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/users', name: 'users', component: UsersListing }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router