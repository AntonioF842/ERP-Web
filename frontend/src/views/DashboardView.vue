<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Banner de Bienvenida -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">
          ¡Hola de nuevo, {{ authStore.user?.nombre_completo || 'Usuario' }}! 
        </h1>
        <p class="text-slate-500 text-sm mt-1">
          Resumen operativo y métricas clave del sistema.
        </p>
      </div>
      <div class="flex items-center gap-3 shrink-0">
        <router-link to="/ventas">
          <Button label="Nueva Venta" icon="pi pi-shopping-cart" size="small" />
        </router-link>
        <router-link to="/inventario">
          <Button label="Ver Inventario" icon="pi pi-box" size="small" severity="secondary" outlined />
        </router-link>
      </div>
    </div>

    <!-- Grid de Métricas (4 Columnas) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <MetricCard 
        title="Ingresos Totales" 
        :value="`$${Number(resumen.ingresos_totales || 0).toFixed(2)}`"
        subtitle="Ventas completadas"
        icon="pi pi-dollar"
        color-class="bg-emerald-50 text-emerald-600"
      />
      <MetricCard 
        title="Ventas Realizadas" 
        :value="resumen.total_ventas_realizadas || 0"
        subtitle="Transacciones registradas"
        icon="pi pi-shopping-bag"
        color-class="bg-blue-50 text-blue-600"
      />
      <MetricCard 
        title="Producto Estrella" 
        :value="topProductoDestacado.nombre || 'N/A'"
        subtitle="Mayor número de ventas"
        icon="pi pi-star-fill"
        color-class="bg-amber-50 text-amber-600"
      />
      <MetricCard 
        title="Alertas de Stock" 
        :value="stockBajo.length"
        subtitle="Requieren reabastecimiento"
        icon="pi pi-exclamation-triangle"
        color-class="bg-rose-50 text-rose-600"
      />
    </div>

    <!-- Rejilla Principal: Tabla Reabastecimiento + Atajos -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Tabla Stock Crítico (2 Columnas) -->
      <div class="lg:col-span-2 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-box text-rose-500 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Productos con Stock Crítico</h2>
          </div>
          <router-link to="/inventario" class="text-xs font-semibold text-blue-600 hover:text-blue-700">
            Gestionar Todo →
          </router-link>
        </div>

        <DataTable :value="stockBajo" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
          <template #empty>
            <div class="py-6 text-center text-slate-400">
              <i class="pi pi-check-circle text-3xl text-emerald-500 mb-2"></i>
              <p class="text-sm font-medium">El inventario se encuentra en niveles óptimos.</p>
            </div>
          </template>
          <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
          <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
          <Column field="stock_actual" header="Stock Actual">
            <template #body="slotProps">
              <Tag :value="slotProps.data.stock_actual" severity="danger" />
            </template>
          </Column>
          <Column field="stock_minimo" header="Stock Mínimo" class="text-slate-500"></Column>
        </DataTable>
      </div>

      <!-- Panel de Atajos Rápidos (1 Columna) -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div class="border-b border-slate-100 pb-3">
          <h2 class="font-bold text-slate-800 text-base">Accesos Rápidos</h2>
          <p class="text-xs text-slate-400">Atajos directos a las operaciones habituales</p>
        </div>

        <div class="space-y-3">
          <QuickAccessCard 
            to="/ventas" 
            title="Terminal POS" 
            description="Registrar nueva venta" 
            icon="pi pi-shopping-cart" 
          />
          <QuickAccessCard 
            to="/inventario" 
            title="Gestión de Productos" 
            description="Añadir o modificar catálogo" 
            icon="pi pi-tags" 
          />
          <QuickAccessCard 
            to="/reportes" 
            title="Reportes General" 
            description="Métricas y estadísticas del negocio" 
            icon="pi pi-chart-line" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../api/axios';
import MetricCard from '../components/MetricCard.vue';
import QuickAccessCard from '../components/QuickAccessCard.vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Button from 'primevue/button';

const authStore = useAuthStore();
const resumen = ref({ total_ventas_realizadas: 0, ingresos_totales: 0 });
const topProductos = ref([]);
const stockBajo = ref([]);
const loading = ref(false);

const topProductoDestacado = computed(() => {
  return topProductos.value.length > 0 ? topProductos.value[0] : { nombre: 'Sin ventas' };
});

const cargarDatosDashboard = async () => {
  loading.value = true;
  try {
    const [resumenRes, topRes, stockBajoRes] = await Promise.all([
      api.get('/reportes/resumen'),
      api.get('/reportes/top-productos'),
      api.get('/reportes/stock-bajo')
    ]);

    resumen.value = resumenRes.data;
    topProductos.value = topRes.data;
    stockBajo.value = stockBajoRes.data;
  } catch (error) {
    console.error('Error al cargar datos del dashboard:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  cargarDatosDashboard();
});
</script>