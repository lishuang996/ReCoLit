import { createRouter, createWebHistory } from 'vue-router'
import TempView from '../components/TempView.vue'
import RegisterView from '../components/RegisterView.vue'

const routes = [
  {
    path: '/', 
    name: 'Temp',
    component: TempView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  }
]

const router = createRouter({
  history: createWebHistory(), 
  routes 
})

export default router
