<template>
  <nav class="navbar" role="navigation" aria-label="Navegação principal">
    <RouterLink to="/" class="navbar__logo" aria-label="LegisKids — ir para o início">
      <div class="logo-icon">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
          <rect width="32" height="32" rx="6" fill="white" fill-opacity="0.15"/>
          <path d="M16 4L6 9v8c0 5.5 4.3 10.7 10 12 5.7-1.3 10-6.5 10-12V9L16 4z" fill="white" fill-opacity="0.9"/>
          <path d="M13 16l2 2 4-4" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="logo-text">
        <span class="logo-title">LegisKids</span>
        <span class="logo-subtitle">Monitoramento Legislativo</span>
      </div>
    </RouterLink>

    <div class="navbar__menu" :class="{ 'navbar__menu--open': menuAberto }" role="menubar">
      <RouterLink to="/" class="nav-item" active-class="active" exact @click="fecharMenu">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
          <polyline points="9,22 9,12 15,12 15,22"/>
        </svg>
        Dashboard
      </RouterLink>

      <RouterLink to="/busca" class="nav-item" active-class="active" @click="fecharMenu">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        Busca
      </RouterLink>
    </div>

    <button
      class="navbar__hamburger"
      :aria-expanded="menuAberto"
      aria-label="Abrir menu de navegação"
      @click="toggleMenu"
    >
      <svg v-if="!menuAberto" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
      <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const menuAberto = ref(false)

function toggleMenu() {
  menuAberto.value = !menuAberto.value
}

function fecharMenu() {
  menuAberto.value = false
}
</script>

<style scoped>
.navbar {
  height: 72px;
  background: var(--primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  gap: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.18);
}

.navbar__logo {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  text-decoration: none;
}

.logo-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.logo-title {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
  font-weight: 400;
  margin-top: 2px;
}

.navbar__menu {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 7px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 14px;
  border-radius: 6px;
  transition: background var(--transition), color var(--transition);
  outline-offset: 2px;
}

.nav-item:hover,
.nav-item.active {
  background: rgba(255, 255, 255, 0.16);
  color: #fff;
}

.nav-item:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.8);
}

.navbar__hamburger {
  display: none;
  background: rgba(255, 255, 255, 0.14);
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  padding: 8px;
  align-items: center;
  justify-content: center;
  transition: background var(--transition);
}

.navbar__hamburger:hover {
  background: rgba(255, 255, 255, 0.26);
}

.navbar__hamburger:focus-visible {
  outline: 2px solid rgba(255, 255, 255, 0.8);
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 16px;
    height: 60px;
    flex-wrap: wrap;
    height: auto;
    min-height: 60px;
    align-items: center;
  }

  .logo-subtitle {
    display: none;
  }

  .navbar__hamburger {
    display: flex;
  }

  .navbar__menu {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
    padding: 8px 0 12px;
  }

  .navbar__menu--open {
    display: flex;
  }

  .nav-item {
    padding: 10px 12px;
  }
}
</style>
