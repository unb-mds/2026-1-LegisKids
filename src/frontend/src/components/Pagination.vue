<template>
  <div class="pagination" role="navigation" aria-label="Paginação">
    <div class="pagination__info">
      <label for="per-page-select" class="sr-only">Itens por página</label>
      <select
        id="per-page-select"
        class="per-page-select"
        :value="itemsPerPage"
        @change="$emit('per-page-changed', Number($event.target.value))"
        aria-label="Itens por página"
      >
        <option :value="10">10 por página</option>
        <option :value="25">25 por página</option>
        <option :value="50">50 por página</option>
      </select>
      <span class="pagination__total" aria-live="polite">
        {{ inicio }}–{{ fim }} de {{ totalItems }} resultado{{ totalItems !== 1 ? 's' : '' }}
      </span>
    </div>

    <div class="pagination__controls">
      <button
        class="page-btn"
        :disabled="currentPage <= 1"
        aria-label="Página anterior"
        @click="$emit('page-changed', currentPage - 1)"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <polyline points="15,18 9,12 15,6"/>
        </svg>
      </button>

      <button
        v-for="p in paginas"
        :key="p"
        class="page-btn"
        :class="{ 'page-btn--active': p === currentPage }"
        :disabled="p === currentPage"
        :aria-current="p === currentPage ? 'page' : undefined"
        :aria-label="`Página ${p}`"
        @click="$emit('page-changed', p)"
      >
        {{ p }}
      </button>

      <button
        class="page-btn"
        :disabled="currentPage >= totalPages"
        aria-label="Próxima página"
        @click="$emit('page-changed', currentPage + 1)"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
          <polyline points="9,18 15,12 9,6"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalItems: { type: Number, required: true },
  itemsPerPage: { type: Number, default: 10 },
  currentPage: { type: Number, default: 1 }
})

defineEmits(['page-changed', 'per-page-changed'])

const totalPages = computed(() => Math.max(1, Math.ceil(props.totalItems / props.itemsPerPage)))

const inicio = computed(() => Math.min((props.currentPage - 1) * props.itemsPerPage + 1, props.totalItems))
const fim = computed(() => Math.min(props.currentPage * props.itemsPerPage, props.totalItems))

const paginas = computed(() => {
  const total = totalPages.value
  const current = props.currentPage
  const delta = 2
  const range = []

  for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
    range.push(i)
  }
  if (range[0] > 1) range.unshift(1)
  if (range[range.length - 1] < total) range.push(total)
  return range
})
</script>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding: 12px 0;
}

.pagination__info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.per-page-select {
  height: 36px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--card);
  padding: 0 10px;
  font-size: 13px;
  font-family: inherit;
  color: var(--text-primary);
  cursor: pointer;
  outline: none;
}

.per-page-select:focus {
  border-color: var(--primary);
}

.pagination__total {
  font-size: 13px;
  color: var(--text-secondary);
}

.pagination__controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--card);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  font-family: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  transition: background var(--transition), border-color var(--transition), color var(--transition);
  outline-offset: 2px;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.page-btn:focus-visible {
  outline: 2px solid var(--primary);
}

.page-btn--active {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  cursor: default;
}

.page-btn:disabled:not(.page-btn--active) {
  opacity: 0.4;
  cursor: not-allowed;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
