import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchProposicoes as apiFetchProposicoes } from '@/services/proposicoes'

export const useProposicoesStore = defineStore('proposicoes', () => {
  const lista = ref([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref(null)

  async function carregar(filtros = {}, pagina = 1, porPagina = 10) {
    loading.value = true
    error.value = null
    try {
      const data = await apiFetchProposicoes(filtros, pagina, porPagina)
      lista.value = data.items ?? data
      total.value = data.total ?? data.length
    } catch (e) {
      error.value = e.message || 'Erro ao carregar proposições'
    } finally {
      loading.value = false
    }
  }

  function resetar() {
    lista.value = []
    total.value = 0
    loading.value = false
    error.value = null
  }

  return { lista, total, loading, error, carregar, resetar }
})
