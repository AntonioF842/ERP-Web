<template>
  <div class="space-y-6">
    <!-- Encabezado -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Reportes & Analíticas</h1>
        <p class="text-slate-500 text-sm">Resumen ejecutivo, productos más vendidos y alertas de stock</p>
      </div>
      <Button icon="pi pi-refresh" label="Actualizar" severity="secondary" text @click="cargarReportes" />
    </div>

    <!-- Indicadores Financieros (KPIs) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card class="shadow-sm border-l-4 border-blue-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-sm font-semibold text-slate-500">Ingresos Totales</p>
              <h3 class="text-3xl font-bold text-slate-800 mt-1">
                ${{ Number(resumen.ingresos_totales || 0).toFixed(2) }}
              </h3>
            </div>
            <div class="p-4 bg-blue-100 rounded-full text-blue-600">
              <i class="pi pi-dollar text-3xl"></i>
            </div>
          </div>
        </template>
      </Card>

      <Card class="shadow-sm border-l-4 border-green-500">
        <template #content>
          <div class="flex justify-between items-center">
            <div>
              <p class="text-sm font-semibold text-slate-500">Ventas Completadas</p>
              <h3 class="text-3xl font-bold text-slate-800 mt-1">
                {{ resumen.total_ventas_realizadas || 0 }}
              </h3>
            </div>
            <div class="p-4 bg-green-100 rounded-full text-green-600">
              <i class="pi pi-shopping-bag text-3xl"></i>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Tablas de Información -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Tabla: Top Productos Más Vendidos -->
      <Card class="shadow-sm">
        <template #title>
          <div class="flex items-center gap-2 text-lg font-semibold text-slate-700">
            <i class="pi pi-star-fill text-yellow-500"></i>
            <span>Top Productos Más Vendidos</span>
          </div>
        </template>
        <template #content>
          <DataTable :value="topProductos" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
            <template #empty> No hay ventas completadas registradas. </template>
            <Column field="sku" header="SKU"></Column>
            <Column field="nombre" header="Producto"></Column>
            <Column field="total_vendido" header="Vendidos" sortable></Column>
            <Column field="total_recaudado" header="Recaudado" sortable>
              <template #body="slotProps">
                ${{ Number(slotProps.data.total_recaudado || 0).toFixed(2) }}
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>

      <!-- Tabla: Alertas de Stock Bajo -->
      <Card class="shadow-sm">
        <template #title>
          <div class="flex items-center gap-2 text-lg font-semibold text-slate-700">
            <i class="pi pi-exclamation-triangle text-red-500"></i>
            <span>Alertas de Stock Bajo</span>
          </div>
        </template>
        <template #content>
          <DataTable :value="stockBajo" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
            <template #empty> Todos los productos están con nivel aceptable de stock. </template>
            <Column field="sku" header="SKU"></Column>
            <Column field="nombre" header="Producto"></Column>
            <Column field="stock_actual" header="Stock Actual">
              <template #body="slotProps">
                <Tag :value="slotProps.data.stock_actual" severity="danger" />
              </template>
            </Column>
            <Column field="stock_minimo" header="Stock Mínimo"></Column>
          </DataTable>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import Card from 'primevue/card';
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