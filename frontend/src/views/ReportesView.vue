<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Reportes & Analíticas</h1>
        <p class="text-slate-500 text-sm mt-1">Resumen ejecutivo, productos más vendidos y alertas de stock</p>
      </div>
      <Button icon="pi pi-refresh" label="Actualizar" severity="secondary" text @click="cargarReportes" />
    </div>

    <!-- Indicadores Financieros (KPIs) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 border-l-4 border-l-blue-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Ingresos Totales</p>
          <h3 class="text-3xl font-black text-slate-800 mt-2">
            ${{ Number(resumen.ingresos_totales || 0).toFixed(2) }}
          </h3>
        </div>
        <div class="p-4 bg-blue-50 text-blue-600 rounded-xl">
          <i class="pi pi-dollar text-2xl"></i>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 border-l-4 border-l-emerald-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-500">Ventas Completadas</p>
          <h3 class="text-3xl font-black text-slate-800 mt-2">
            {{ resumen.total_ventas_realizadas || 0 }}
          </h3>
        </div>
        <div class="p-4 bg-emerald-50 text-emerald-600 rounded-xl">
          <i class="pi pi-shopping-bag text-2xl"></i>
        </div>
      </div>
    </div>

    <!-- Tablas de Información -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Tabla: Top Productos Más Vendidos -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-100">
          <i class="pi pi-star-fill text-amber-500 text-lg"></i>
          <h2 class="font-bold text-slate-800 text-base">Top Productos Más Vendidos</h2>
        </div>
        
        <DataTable :value="topProductos" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
          <template #empty>
            <div class="py-6 text-center text-slate-400 text-sm">No hay ventas completadas registradas.</div>
          </template>
          <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
          <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
          <Column field="total_vendido" header="Vendidos" sortable></Column>
          <Column field="total_recaudado" header="Recaudado" sortable>
            <template #body="slotProps">
              ${{ Number(slotProps.data.total_recaudado || 0).toFixed(2) }}
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Tabla: Alertas de Stock Bajo -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-100">
          <i class="pi pi-exclamation-triangle text-rose-500 text-lg"></i>
          <h2 class="font-bold text-slate-800 text-base">Alertas de Stock Bajo</h2>
        </div>

        <DataTable :value="stockBajo" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
          <template #empty>
            <div class="py-6 text-center text-slate-400 text-sm">Todos los productos están con nivel aceptable de stock.</div>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Button from 'primevue/button';

const resumen = ref({ total_ventas_realizadas: 0, ingresos_totales: 0 });
const topProductos = ref([]);
const stockBajo = ref([]);
const loading = ref(false);

const cargarReportes = async () => {
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
    console.error('Error al cargar reportes:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  cargarReportes();
});
</script>