<template>
  <div class="busca">
    <div class="container">

      <header class="busca-header">
        <h1 class="busca-title">Busca de Proposições</h1>
        <p class="busca-desc">Pesquise e filtre proposições legislativas por tema, parlamentar, partido ou período.</p>
      </header>

      <FilterBar @filter-changed="onFiltroMudou" />

      <div class="busca-resultados">
        <LoadingSpinner v-if="store.loading" />

        <template v-else-if="store.error">
          <div class="erro-banner" role="alert">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ store.error }}
          </div>
        </template>

        <template v-else>
          <div class="resultados-header">
            <span class="resultados-count" aria-live="polite">
              <template v-if="buscaFeita">
                {{ store.total }} resultado{{ store.total !== 1 ? 's' : '' }} encontrado{{ store.total !== 1 ? 's' : '' }}
              </template>
            </span>
          </div>

          <div v-if="buscaFeita && store.lista.length === 0" class="empty-state" role="status">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <p>Nenhuma proposição encontrada com os filtros aplicados.</p>
            <p>Tente outros termos ou limpe os filtros.</p>
          </div>

          <div v-else class="proposicoes-lista" role="list" aria-label="Lista de proposições">
            <div v-for="p in store.lista" :key="p.id" role="listitem">
              <ProposicaoCard
                :id="p.id"
                :titulo="p.titulo || p.ementa"
                :autor="p.autor || p.nome_autor"
                :partido="p.partido || p.sigla_partido"
                :data="p.data || p.data_apresentacao"
                :status="p.status"
                :subtema="p.subtema || p.categoria"
              />
            </div>
          </div>

          <Pagination
            v-if="buscaFeita && store.total > 0"
            :total-items="store.total"
            :items-per-page="buscaStore.porPagina"
            :current-page="buscaStore.pagina"
            @page-changed="onPaginaMudou"
            @per-page-changed="onPorPaginaMudou"
          />
        </template>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProposicoesStore } from '@/stores/proposicoes'
import { useBuscaStore } from '@/stores/busca'
import FilterBar from '@/components/FilterBar.vue'
import ProposicaoCard from '@/components/ProposicaoCard.vue'
import Pagination from '@/components/Pagination.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const store = useProposicoesStore()
const buscaStore = useBuscaStore()
const buscaFeita = ref(false)

async function onFiltroMudou(filtros) {
  Object.assign(buscaStore.filtros, filtros)
  if (filtros.termo !== undefined) buscaStore.termo = filtros.termo
  buscaStore.pagina = 1
  buscaFeita.value = true
  await store.carregar(
    { ...buscaStore.filtros, termo: buscaStore.termo },
    buscaStore.pagina,
    buscaStore.porPagina
  )
}

async function onPaginaMudou(pagina) {
  buscaStore.pagina = pagina
  await store.carregar(
    { ...buscaStore.filtros, termo: buscaStore.termo },
    pagina,
    buscaStore.porPagina
  )
}

async function onPorPaginaMudou(porPagina) {
  buscaStore.porPagina = porPagina
  buscaStore.pagina = 1
  await store.carregar(
    { ...buscaStore.filtros, termo: buscaStore.termo },
    1,
    porPagina
  )
}
</script>

<style scoped>
.busca {
  padding: 28px 20px;
}

.busca-header {
  margin-bottom: var(--gap);
}

.busca-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.busca-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.busca-resultados {
  margin-top: var(--gap);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.resultados-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.resultados-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.proposicoes-lista {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  padding: 48px 20px;
  color: var(--text-secondary);
  font-size: 14px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.erro-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--warning-bg);
  border-left: 4px solid var(--warning-border);
  border-radius: var(--radius);
  padding: 14px 18px;
  font-size: 14px;
  color: var(--warning-text);
}
</style>
