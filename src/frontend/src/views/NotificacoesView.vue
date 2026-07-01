<template>
  <div class="placeholder-page">
    <div class="container">
      <header class="placeholder-header">
        <h1 class="placeholder-title">Notificações</h1>
        <p class="placeholder-desc">Alertas sobre proposições e temas acompanhados.</p>
      </header>

      <div class="empty-state" role="status">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M18 8a6 6 0 00-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>
          <path d="M13.73 21a2 2 0 01-3.46 0"/>
        </svg>
        <p>Notificações em construção.</p>
        <p>Essa funcionalidade está prevista para uma próxima etapa do projeto.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.placeholder-page {
  padding: 28px 20px;
}

.placeholder-header {
  margin-bottom: var(--gap);
}

.placeholder-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.placeholder-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
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
  box-shadow: var(--shadow);
}
</style>
