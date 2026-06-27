import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useBuscaStore = defineStore('busca', () => {
  const termo = ref('')
  const filtros = reactive({
    parlamentar: '',
    partido: '',
    dataInicio: '',
    dataFim: '',
    subtema: ''
  })
  const pagina = ref(1)
  const porPagina = ref(10)

  function limparFiltros() {
    termo.value = ''
    filtros.parlamentar = ''
    filtros.partido = ''
    filtros.dataInicio = ''
    filtros.dataFim = ''
    filtros.subtema = ''
    pagina.value = 1
  }

  return { termo, filtros, pagina, porPagina, limparFiltros }
})
