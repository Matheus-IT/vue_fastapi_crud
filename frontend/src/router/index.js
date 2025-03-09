import { createRouter, createWebHistory } from 'vue-router'
import UsersListing from '@/views/UsersListing.vue'
import UserDetail from '@/views/UserDetail.vue'

const routes = [
    { path: '/', redirect: '/users' },
    { path: '/users', name: 'users', component: UsersListing },
    { path: '/users/:user_id', name: 'user-detail', component: UserDetail }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router