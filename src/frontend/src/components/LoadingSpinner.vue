<template>
  <div class="spinner-wrapper" role="status" aria-label="Carregando...">
    <div class="spinner" aria-hidden="true"></div>
    <span class="spinner-text">Carregando...</span>
  </div>
</template>

<style scoped>
.spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-text {
  font-size: 14px;
  color: var(--text-secondary);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
