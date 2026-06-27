import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/busca',
      name: 'busca',
      component: () => import('@/views/BuscaView.vue')
    },
    {
      path: '/proposicao/:id',
      name: 'detalhe',
      component: () => import('@/views/DetalheView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/'
    }
  ]
})

export default router
