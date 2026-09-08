<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado y Filtros por Período -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Reportes & Business Intelligence</h1>
        <p class="text-slate-500 text-sm mt-1">Análisis de rendimiento por intervalo de tiempo</p>
      </div>

      <!-- Selector de Período -->
      <div class="flex items-center gap-2 bg-slate-100 p-1 rounded-xl">
        <button 
          v-for="opcion in periodos" 
          :key="opcion.value"
          @click="cambiarPeriodo(opcion.value)"
          :class="[
            'px-3 py-1.5 text-xs font-semibold rounded-lg transition-all',
            periodoSeleccionado === opcion.value 
              ? 'bg-white text-blue-600 shadow-sm' 
              : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          {{ opcion.label }}
        </button>
      </div>
    </div>

    <!-- Indicadores Financieros (KPIs) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <div class="bg-white p-5 rounded-2xl border border-slate-200 border-l-4 border-l-blue-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Ingresos Totales</p>
          <h3 class="text-2xl font-black text-slate-800 mt-1">${{ Number(resumen.ingresos_totales || 0).toFixed(2) }}</h3>
        </div>
        <div class="p-3.5 bg-blue-50 text-blue-600 rounded-xl">
          <i class="pi pi-dollar text-xl"></i>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200 border-l-4 border-l-emerald-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Ventas Completadas</p>
          <h3 class="text-2xl font-black text-slate-800 mt-1">{{ resumen.total_ventas_realizadas || 0 }}</h3>
        </div>
        <div class="p-3.5 bg-emerald-50 text-emerald-600 rounded-xl">
          <i class="pi pi-shopping-bag text-xl"></i>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200 border-l-4 border-l-indigo-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Ticket Promedio</p>
          <h3 class="text-2xl font-black text-slate-800 mt-1">${{ ticketPromedio.toFixed(2) }}</h3>
        </div>
        <div class="p-3.5 bg-indigo-50 text-indigo-600 rounded-xl">
          <i class="pi pi-calculator text-xl"></i>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200 border-l-4 border-l-rose-500 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Alertas de Stock</p>
          <h3 class="text-2xl font-black text-slate-800 mt-1">{{ stockBajo.length }}</h3>
        </div>
        <div class="p-3.5 bg-rose-50 text-rose-600 rounded-xl">
          <i class="pi pi-exclamation-triangle text-xl"></i>
        </div>
      </div>
    </div>

    <!-- Sección de Gráficos -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-chart-bar text-blue-600 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Unidades Vendidas ({{ etiquetaPeriodo }})</h2>
          </div>
        </div>
        <div class="h-64 flex items-center justify-center">
          <Chart v-if="topProductos.length > 0" type="bar" :data="chartDataBar" :options="chartOptionsBar" class="w-full h-full" />
          <p v-else class="text-sm text-slate-400">No hay transacciones registradas en este período.</p>
        </div>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-chart-pie text-emerald-600 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Distribución de Ingresos</h2>
          </div>
        </div>
        <div class="h-64 flex items-center justify-center">
          <Chart v-if="topProductos.length > 0" type="doughnut" :data="chartDataPie" :options="chartOptionsPie" class="w-full h-full" />
          <p v-else class="text-sm text-slate-400">Sin datos de recaudación en este período.</p>
        </div>
      </div>
    </div>

    <!-- Tablas de Información Detallada -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-star-fill text-amber-500 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Top Productos ({{ etiquetaPeriodo }})</h2>
          </div>
          <Button label="CSV" icon="pi pi-download" severity="secondary" text size="small" @click="exportarCSV" />
        </div>
        
        <DataTable :value="topProductos" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
          <template #empty>
            <div class="py-6 text-center text-slate-400 text-sm">No hay ventas registradas en este rango.</div>
          </template>
          <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
          <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
          <Column field="total_vendido" header="Vendidos" sortable></Column>
          <Column field="total_recaudado" header="Recaudado" sortable>
            <template #body="slotProps">
              <span class="font-semibold text-emerald-600">${{ Number(slotProps.data.total_recaudado || 0).toFixed(2) }}</span>
            </template>
          </Column>
        </DataTable>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-exclamation-triangle text-rose-500 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Alertas de Stock Bajo</h2>
          </div>
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
import { ref, computed, onMounted } from 'vue';
import api from '../api/axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import Chart from 'primevue/chart';

const periodoSeleccionado = ref('mes');
const resumen = ref({ total_ventas_realizadas: 0, ingresos_totales: 0 });
const topProductos = ref([]);
const stockBajo = ref([]);
const loading = ref(false);

const periodos = [
  { label: 'Semana', value: 'semana' },
  { label: 'Mes', value: 'mes' },
  { label: 'Año', value: 'anio' },
  { label: 'Todo', value: 'todos' }
];

const etiquetaPeriodo = computed(() => {
  const p = periodos.find(item => item.value === periodoSeleccionado.value);
  return p ? p.label : '';
});

const ticketPromedio = computed(() => {
  if (!resumen.value.total_ventas_realizadas) return 0;
  return resumen.value.ingresos_totales / resumen.value.total_ventas_realizadas;
});

const chartDataBar = computed(() => ({
  labels: topProductos.value.map(p => p.nombre),
  datasets: [
    {
      label: 'Unidades Vendidas',
      backgroundColor: '#2563eb',
      borderRadius: 8,
      data: topProductos.value.map(p => p.total_vendido)
    }
  ]
}));

const chartOptionsBar = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
    x: { grid: { display: false } }
  }
};

const chartDataPie = computed(() => ({
  labels: topProductos.value.map(p => p.nombre),
  datasets: [
    {
      data: topProductos.value.map(p => p.total_recaudado),
      backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    }
  ]
}));

const chartOptionsPie = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
};

const cambiarPeriodo = (nuevoPeriodo) => {
  periodoSeleccionado.value = nuevoPeriodo;
  cargarReportes();
};

const cargarReportes = async () => {
  loading.value = true;
  try {
    const [resumenRes, topRes, stockBajoRes] = await Promise.all([
      api.get(`/reportes/resumen?periodo=${periodoSeleccionado.value}`),
      api.get(`/reportes/top-productos?periodo=${periodoSeleccionado.value}`),
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

const exportarCSV = () => {
  if (topProductos.value.length === 0) return;
  
  let csvContent = "data:text/csv;charset=utf-8,SKU,Producto,Total Vendido,Total Recaudado ($)\n";
  topProductos.value.forEach(p => {
    csvContent += `${p.sku},${p.nombre},${p.total_vendido},${p.total_recaudado}\n`;
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `reporte_${periodoSeleccionado.value}_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

onMounted(() => {
  cargarReportes();
});
</script>