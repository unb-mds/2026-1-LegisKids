<template>
  <div id="layout">
    <Navbar />
    <main class="main-content">
      <RouterView />
    </main>
    <footer class="footer">
      <span>© 2026 Sistema de Monitoramento Legislativo — Proteção Infantil Digital</span>
      <nav class="footer-links">
        <a href="#">Sobre</a>
        <a href="#">Contato</a>
        <a href="#">Privacidade</a>
      </nav>
    </footer>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
#layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer {
  background: var(--primary);
  color: rgba(255, 255, 255, 0.8);
  padding: 20px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  margin-top: auto;
}

.footer-links {
  display: flex;
  gap: 22px;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  transition: color var(--transition);
}

.footer-links a:hover {
  color: #fff;
}

@media (max-width: 640px) {
  .footer {
    flex-direction: column;
    text-align: center;
    padding: 16px;
  }
}
</style>
