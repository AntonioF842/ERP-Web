<template>
  <div class="space-y-6">
    <!-- Bienvenida / Encabezado -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">
          ¡Hola de nuevo, {{ authStore.user?.nombre_completo || 'Usuario' }}! 
        </h1>
        <p class="text-slate-500 text-sm mt-1">
          Aquí tienes un resumen general de la actividad y estado del ERP hoy.
        </p>
      </div>
      <div class="flex gap-3">
        <router-link to="/ventas">
          <Button label="Nueva Venta" icon="pi pi-shopping-cart" severity="primary" size="small" />
        </router-link>
        <router-link to="/inventario">
          <Button label="Ver Inventario" icon="pi pi-box" severity="secondary" size="small" outlined />
        </router-link>
      </div>
    </div>

    <!-- Tarjetas de Métricas Clave -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card class="shadow-sm border-l-4 border-blue-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Ingresos Totales</p>
              <h3 class="text-2xl font-bold text-slate-800 mt-1">
                ${{ Number(resumen.ingresos_totales || 0).toFixed(2) }}
              </h3>
            </div>
            <div class="p-3 bg-blue-100 rounded-lg text-blue-600">
              <i class="pi pi-dollar text-xl"></i>
            </div>
          </div>
        </template>
      </Card>

      <Card class="shadow-sm border-l-4 border-green-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Ventas Realizadas</p>
              <h3 class="text-2xl font-bold text-slate-800 mt-1">
                {{ resumen.total_ventas_realizadas || 0 }}
              </h3>
            </div>
            <div class="p-3 bg-green-100 rounded-lg text-green-600">
              <i class="pi pi-shopping-bag text-xl"></i>
            </div>
          </div>
        </template>
      </Card>

      <Card class="shadow-sm border-l-4 border-purple-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Top Producto</p>
              <h3 class="text-lg font-bold text-slate-800 mt-1 truncate max-w-[120px]" :title="topProductoDestacado.nombre">
                {{ topProductoDestacado.nombre || 'N/A' }}
              </h3>
            </div>
            <div class="p-3 bg-purple-100 rounded-lg text-purple-600">
              <i class="pi pi-star-fill text-xl"></i>
            </div>
          </div>
        </template>
      </Card>

      <Card class="shadow-sm border-l-4 border-red-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Alertas de Stock</p>
              <h3 class="text-2xl font-bold text-slate-800 mt-1">
                {{ stockBajo.length }}
              </h3>
            </div>
            <div class="p-3 bg-red-100 rounded-lg text-red-600">
              <i class="pi pi-exclamation-circle text-xl"></i>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Sección Inferior: Alertas Prioritarias y Accesos -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Tabla Resumen: Alertas de Stock Bajo -->
      <Card class="lg:col-span-2 shadow-sm">
        <template #title>
          <div class="flex justify-between items-center text-base font-bold text-slate-800">
            <span class="flex items-center gap-2">
              <i class="pi pi-exclamation-triangle text-red-500"></i>
              Productos Requieren Reabastecimiento
            </span>
            <router-link to="/inventario" class="text-xs text-blue-600 hover:underline">Gestionar</router-link>
          </div>
        </template>
        <template #content>
          <DataTable :value="stockBajo" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
            <template #empty>
              <div class="py-4 text-center text-slate-400">
                <i class="pi pi-check-circle text-2xl text-green-500 mb-1"></i>
                <p>El inventario no presenta productos en nivel crítico.</p>
              </div>
            </template>
            <Column field="sku" header="SKU"></Column>
            <Column field="nombre" header="Producto"></Column>
            <Column field="stock_actual" header="Stock Dispo.">
              <template #body="slotProps">
                <Tag :value="slotProps.data.stock_actual" severity="danger" />
              </template>
            </Column>
            <Column field="stock_minimo" header="Stock Mínimo"></Column>
          </DataTable>
        </template>
      </Card>

      <!-- Panel Lateral de Atajos -->
      <Card class="shadow-sm">
        <template #title>
          <span class="text-base font-bold text-slate-800">Accesos Rápidos</span>
        </template>
        <template #content>
          <div class="flex flex-col gap-3">
            <router-link to="/ventas" class="p-3 rounded-lg border border-slate-200 hover:border-blue-500 hover:bg-blue-50/50 transition-all flex items-center justify-between group">
              <div class="flex items-center gap-3">
                <i class="pi pi-shopping-cart text-blue-600 text-lg"></i>
                <div>
                  <p class="font-semibold text-slate-800 text-sm">Ir a Terminal POS</p>
                  <p class="text-xs text-slate-500">Registrar una nueva transacción</p>
                </div>
              </div>
              <i class="pi pi-chevron-right text-slate-400 group-hover:text-blue-600"></i>
            </router-link>

            <router-link to="/inventario" class="p-3 rounded-lg border border-slate-200 hover:border-blue-500 hover:bg-blue-50/50 transition-all flex items-center justify-between group">
              <div class="flex items-center gap-3">
                <i class="pi pi-box text-blue-600 text-lg"></i>
                <div>
                  <p class="font-semibold text-slate-800 text-sm">Crear Producto</p>
                  <p class="text-xs text-slate-500">Añadir items al catálogo</p>
                </div>
              </div>
              <i class="pi pi-chevron-right text-slate-400 group-hover:text-blue-600"></i>
            </router-link>

            <router-link to="/reportes" class="p-3 rounded-lg border border-slate-200 hover:border-blue-500 hover:bg-blue-50/50 transition-all flex items-center justify-between group">
              <div class="flex items-center gap-3">
                <i class="pi pi-chart-bar text-blue-600 text-lg"></i>
                <div>
                  <p class="font-semibold text-slate-800 text-sm">Reportes Detallados</p>
                  <p class="text-xs text-slate-500">Analítica avanzada del negocio</p>
                </div>
              </div>
              <i class="pi pi-chevron-right text-slate-400 group-hover:text-blue-600"></i>
            </router-link>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../api/axios';
import Card from 'primevue/card';
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