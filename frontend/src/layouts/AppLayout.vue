<template>
  <div class="flex h-screen bg-slate-50 overflow-hidden">
    <!-- Sidebar / Menú Lateral -->
    <aside class="w-64 bg-slate-900 text-slate-100 flex flex-col justify-between shadow-xl">
      <div>
        <!-- Logo ERP -->
        <div class="p-5 flex items-center gap-3 border-b border-slate-800">
          <i class="pi pi-box text-blue-400 text-2xl"></i>
          <span class="font-bold text-xl tracking-wide">ERP System</span>
        </div>

        <!-- Links de Navegación -->
        <nav class="p-4 flex flex-col gap-1">
          <router-link 
            to="/dashboard" 
            class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
            active-class="bg-blue-600 text-white hover:bg-blue-600"
          >
            <i class="pi pi-chart-bar text-lg"></i>
            <span class="font-medium">Dashboard</span>
          </router-link>

          <router-link 
            to="/inventario" 
            class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
            active-class="bg-blue-600 text-white hover:bg-blue-600"
          >
            <i class="pi pi-tags text-lg"></i>
            <span class="font-medium">Inventario</span>
          </router-link>

          <router-link 
            to="/ventas" 
            class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
            active-class="bg-blue-600 text-white hover:bg-blue-600"
          >
            <i class="pi pi-shopping-cart text-lg"></i>
            <span class="font-medium">Ventas</span>
          </router-link>

          <router-link 
            to="/reportes" 
            class="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
            active-class="bg-blue-600 text-white hover:bg-blue-600"
          >
            <i class="pi pi-file text-lg"></i>
            <span class="font-medium">Reportes</span>
          </router-link>
        </nav>
      </div>

      <!-- Footer del Sidebar con info de usuario -->
      <div class="p-4 border-t border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-3 overflow-hidden">
          <Avatar icon="pi pi-user" class="bg-blue-600 text-white" shape="circle" />
          <div class="truncate">
            <p class="text-sm font-semibold truncate">{{ authStore.user?.nombre_completo || 'Usuario' }}</p>
            <p class="text-xs text-slate-400 capitalize truncate">{{ authStore.user?.rol || 'Rol' }}</p>
          </div>
        </div>
        <Button 
          icon="pi pi-sign-out" 
          severity="danger" 
          text 
          rounded 
          aria-label="Cerrar Sesión" 
          @click="handleLogout"
        />
      </div>
    </aside>

    <!-- Área Principal de Contenido -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header Superior -->
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm">
        <h2 class="text-xl font-bold text-slate-800">
          {{ $route.name ? $route.name.toUpperCase() : 'ERP' }}
        </h2>
        <div class="flex items-center gap-3">
          <span class="text-sm text-slate-500">{{ authStore.user?.email }}</span>
        </div>
      </header>

      <!-- Vistas Hijas -->
      <main class="flex-1 overflow-y-auto p-6 bg-slate-100">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>