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
      path: '/configuracoes',
      name: 'configuracoes',
      component: () => import('@/views/ConfiguracoesView.vue')
    },
    {
      path: '/notificacoes',
      name: 'notificacoes',
      component: () => import('@/views/NotificacoesView.vue')
    },
    {
      path: '/sobre',
      name: 'sobre',
      component: () => import('@/views/SobreView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/'
    }
  ]
})

export default router
