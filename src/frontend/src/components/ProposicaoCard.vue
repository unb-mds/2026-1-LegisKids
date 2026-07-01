<template>
  <article class="proposicao-card" @click="navegar" role="button" tabindex="0" @keydown.enter="navegar" @keydown.space.prevent="navegar">
    <div class="card-header">
      <span class="card-tag" :title="'Código: ' + (codigo || 'N/D')">{{ codigo || 'N/D' }}</span>
      <StatusBadge :status="status || 'Em tramitação'" />
      <span
        v-for="s in subtemasNormalizados"
        :key="s.nome"
        class="card-subtema"
        :style="{ background: corBadge(s.cor).background, color: corBadge(s.cor).color }"
      >{{ s.nome }}</span>
    </div>

    <h3 class="card-titulo">{{ titulo || 'Título não informado' }}</h3>

    <div class="card-meta">
      <span v-if="partido" class="meta-item">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
          <polyline points="9,22 9,12 15,12 15,22"/>
        </svg>
        {{ partido }}
      </span>
      <span v-if="data" class="meta-item">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        {{ dataFormatada }}
      </span>
    </div>

    <span class="card-link" aria-hidden="true">Ver detalhes →</span>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import StatusBadge from './StatusBadge.vue'
import { corBadge } from '@/utils/proposicao'

const props = defineProps({
  id: [String, Number],
  titulo: String,
  partido: String,
  data: String,
  status: String,
  subtemas: { type: Array, default: () => [] },
  siglaTipo: String,
  numero: [String, Number],
  ano: [String, Number]
})

const router = useRouter()

const subtemasNormalizados = computed(() =>
  (props.subtemas || []).map(s => (typeof s === 'string' ? { nome: s, cor: null } : { nome: s.nome, cor: s.cor }))
)

const codigo = computed(() => {
  if (props.siglaTipo && props.numero && props.ano) {
    return `${props.siglaTipo} ${props.numero}/${props.ano}`
  }
  return props.id
})

const dataFormatada = computed(() => {
  if (!props.data) return ''
  try {
    return new Date(props.data).toLocaleDateString('pt-BR')
  } catch {
    return props.data
  }
})

function navegar() {
  if (props.id) router.push({ name: 'detalhe', params: { id: props.id } })
}
</script>

<style scoped>
.proposicao-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  outline-offset: 2px;
}

.proposicao-card:hover,
.proposicao-card:focus-visible {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary);
}

.proposicao-card:focus-visible {
  outline: 2px solid var(--primary);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-tag {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-dark);
  background: #DBEAFE;
  padding: 3px 10px;
  border-radius: 999px;
  font-family: 'IBM Plex Mono', monospace;
}

.card-subtema {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
}

.card-titulo {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.card-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 12px;
  color: var(--text-caption);
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-link {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  align-self: flex-start;
  margin-top: 4px;
}
</style>
