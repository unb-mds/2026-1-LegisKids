<template>
  <nav class="navbar" role="navigation" aria-label="Navegação principal">
    <RouterLink to="/" class="navbar__logo" aria-label="LegisKids — ir para o início">
      <div class="logo-badge">
        <img class="logo-icon" src="@/assets/images/logo-legiskids.png" alt="LegisKids" />
      </div>
      <div class="logo-text">
        <span class="logo-subtitle">Monitoramento Legislativo</span>
      </div>
    </RouterLink>

    <div class="navbar__right">
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

        <RouterLink to="/configuracoes" class="nav-item navbar__action--mobile" active-class="active" @click="fecharMenu">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
          </svg>
          Configurações
        </RouterLink>

        <RouterLink to="/notificacoes" class="nav-item navbar__action--mobile" active-class="active" @click="fecharMenu">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M18 8a6 6 0 00-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 01-3.46 0"/>
          </svg>
          Notificações
        </RouterLink>
      </div>

      <div class="navbar__actions">
        <RouterLink
          to="/configuracoes"
          class="navbar__action"
          active-class="active"
          aria-label="Configurações"
          title="Configurações"
          @click="fecharMenu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
          </svg>
        </RouterLink>

        <RouterLink
          to="/notificacoes"
          class="navbar__action"
          active-class="active"
          aria-label="Notificações"
          title="Notificações"
          @click="fecharMenu"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M18 8a6 6 0 00-12 0c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 01-3.46 0"/>
          </svg>
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
    </div>
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

.logo-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: #fff;
  border-radius: 8px;
  padding: 4px 8px;
}

.logo-icon {
  display: block;
  height: 36px;
  width: auto;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.92);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.01em;
  margin-top: 2px;
}

.navbar__right {
  display: flex;
  align-items: center;
  gap: 16px;
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

.navbar__action--mobile {
  display: none;
}

.navbar__actions {
  display: flex;
  align-items: center;
  gap: 4px;
  padding-left: 12px;
  border-left: 1px solid rgba(255, 255, 255, 0.18);
}

.navbar__action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  transition: background var(--transition), color var(--transition);
  outline-offset: 2px;
}

.navbar__action:hover,
.navbar__action.active {
  background: rgba(255, 255, 255, 0.16);
  color: #fff;
}

.navbar__action:focus-visible {
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

  .navbar__right {
    gap: 8px;
  }

  .navbar__actions {
    display: none;
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

  .navbar__action--mobile {
    display: flex;
  }
}
</style>
