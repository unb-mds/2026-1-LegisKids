<template>
  <span class="status-badge" :class="classe" role="status">{{ status }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const classe = computed(() => {
  const s = props.status?.toLowerCase() ?? ''
  if (s.includes('aprovado') || s.includes('sancionado')) return 'status--aprovado'
  if (s.includes('urgente') || s.includes('crítico')) return 'status--urgente'
  if (s.includes('arquivado') || s.includes('retirado')) return 'status--arquivado'
  return 'status--tramitacao'
})
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status--aprovado {
  background: var(--success-bg);
  color: var(--success-text);
}

.status--urgente {
  background: var(--danger-bg);
  color: var(--danger-text);
}

.status--arquivado {
  background: #F1F5F9;
  color: var(--text-secondary);
}

.status--tramitacao {
  background: #DBEAFE;
  color: var(--primary-dark);
}
</style>
