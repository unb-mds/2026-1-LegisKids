<template>
  <div class="filter-bar">
    <div class="filter-controls">
      <div class="filter-field">
        <label for="filter-termo" class="filter-label">Palavra-chave</label>
        <div class="search-wrapper">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            id="filter-termo"
            v-model="local.termo"
            type="search"
            class="filter-input search-input"
            placeholder="Buscar proposições..."
            autocomplete="off"
            @keydown.enter="emitir"
          />
        </div>
      </div>

      <div class="filter-field">
        <label for="filter-subtema" class="filter-label">Subtema</label>
        <select id="filter-subtema" v-model="local.subtema" class="filter-select" @change="emitir">
          <option value="">Todos</option>
          <option v-for="t in temas" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>

      <div class="filter-field">
        <label for="filter-partido" class="filter-label">Partido</label>
        <input id="filter-partido" v-model="local.partido" type="text" class="filter-input" placeholder="Ex: PT, PL..." @blur="emitir" />
      </div>

      <div class="filter-field">
        <label for="filter-parlamentar" class="filter-label">Parlamentar</label>
        <input id="filter-parlamentar" v-model="local.parlamentar" type="text" class="filter-input" placeholder="Nome do parlamentar" @blur="emitir" />
      </div>

      <div class="filter-field">
        <label for="filter-data-inicio" class="filter-label">Data início</label>
        <input id="filter-data-inicio" v-model="local.dataInicio" type="date" class="filter-input" @change="emitir" />
      </div>

      <div class="filter-field">
        <label for="filter-data-fim" class="filter-label">Data fim</label>
        <input id="filter-data-fim" v-model="local.dataFim" type="date" class="filter-input" @change="emitir" />
      </div>
    </div>

    <div class="filter-actions">
      <button class="btn btn-primary" @click="emitir">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        Buscar
      </button>
      <button class="btn btn-outline" @click="limpar">Limpar filtros</button>
    </div>

    <div v-if="filtrosAtivos.length" class="filter-tags" role="list" aria-label="Filtros ativos">
      <span
        v-for="f in filtrosAtivos"
        :key="f.key"
        class="filter-tag"
        role="listitem"
      >
        {{ f.label }}: {{ f.valor }}
        <button
          class="filter-tag__remove"
          :aria-label="`Remover filtro ${f.label}`"
          @click="removerFiltro(f.key)"
        >×</button>
      </span>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue'
import { fetchTemas } from '@/services/temas'

const emit = defineEmits(['filter-changed'])

const local = reactive({
  termo: '',
  subtema: '',
  partido: '',
  parlamentar: '',
  dataInicio: '',
  dataFim: ''
})

const temas = reactive([])

onMounted(async () => {
  try {
    const data = await fetchTemas()
    temas.push(...(Array.isArray(data) ? data : data.temas ?? []))
  } catch {
    // temas indisponíveis — campo permanece vazio
  }
})

const LABELS = {
  termo: 'Palavra-chave',
  subtema: 'Subtema',
  partido: 'Partido',
  parlamentar: 'Parlamentar',
  dataInicio: 'Data início',
  dataFim: 'Data fim'
}

const filtrosAtivos = computed(() =>
  Object.entries(local)
    .filter(([, v]) => v)
    .map(([k, v]) => ({ key: k, label: LABELS[k], valor: v }))
)

function emitir() {
  emit('filter-changed', { ...local })
}

function limpar() {
  Object.keys(local).forEach(k => { local[k] = '' })
  emit('filter-changed', { ...local })
}

function removerFiltro(key) {
  local[key] = ''
  emitir()
}
</script>

<style scoped>
.filter-bar {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter-controls {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.filter-input {
  width: 100%;
  height: 40px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  padding: 0 12px;
  font-size: 14px;
  font-family: inherit;
  color: var(--text-primary);
  outline: none;
  transition: border-color var(--transition), box-shadow var(--transition);
}

.search-input {
  padding-left: 36px;
}

.filter-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.filter-select {
  width: 100%;
  height: 40px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
  padding: 0 12px;
  font-size: 14px;
  font-family: inherit;
  color: var(--text-primary);
  cursor: pointer;
  outline: none;
  transition: border-color var(--transition);
}

.filter-select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #DBEAFE;
  color: var(--primary-dark);
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 13px;
  font-weight: 500;
}

.filter-tag__remove {
  background: none;
  border: none;
  color: var(--primary-dark);
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0;
  display: flex;
  align-items: center;
  opacity: 0.7;
  transition: opacity var(--transition);
}

.filter-tag__remove:hover {
  opacity: 1;
}
</style>
