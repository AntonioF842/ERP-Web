<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado y Filtros por Período -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Reportes & Business Intelligence</h1>
        <p class="text-slate-500 text-sm mt-1">Análisis de rendimiento, estados financieros y auditoría de inventario</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Selector de Período -->
        <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
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

        <Button label="Exportar PDF" icon="pi pi-file-pdf" severity="danger" size="small" @click="exportarPDF" />
        <Button label="CSV" icon="pi pi-download" severity="secondary" outlined size="small" @click="exportarCSV" />
      </div>
    </div>

    <!-- ÁREA IMPRIMIBLE PARA PDF (Estilos CSS tradicionales sin oklch) -->
    <div 
      id="reporte-imprimible" 
      style="background-color: #f8fafc; padding: 16px; border-radius: 12px; color: #1e293b; font-family: sans-serif;"
    >
      <!-- Indicadores Financieros (KPIs) -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #2563eb;">
          <p style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin: 0;">Ingresos Totales</p>
          <h3 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 0 0;">${{ Number(resumen.ingresos_totales || 0).toFixed(2) }}</h3>
        </div>

        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #10b981;">
          <p style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin: 0;">Ventas Completadas</p>
          <h3 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 0 0;">{{ resumen.total_ventas_realizadas || 0 }}</h3>
        </div>

        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #6366f1;">
          <p style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin: 0;">Ticket Promedio</p>
          <h3 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 0 0;">${{ ticketPromedio.toFixed(2) }}</h3>
        </div>

        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 4px solid #f43f5e;">
          <p style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin: 0;">Alertas de Stock</p>
          <h3 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 0 0;">{{ stockBajo.length }}</h3>
        </div>
      </div>

      <!-- Sección de Gráficos -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 24px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <h2 style="font-weight: 700; font-size: 16px; color: #1e293b; margin: 0 0 16px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
            Unidades Vendidas ({{ etiquetaPeriodo }})
          </h2>
          <div style="height: 240px;">
            <Chart v-if="topProductos.length > 0" type="bar" :data="chartDataBar" :options="chartOptionsBar" class="w-full h-full" />
            <p v-else style="text-align: center; color: #94a3b8; font-size: 14px; padding-top: 80px;">Sin ventas en este período.</p>
          </div>
        </div>

        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <h2 style="font-weight: 700; font-size: 16px; color: #1e293b; margin: 0 0 16px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
            Distribución de Ingresos
          </h2>
          <div style="height: 240px;">
            <Chart v-if="topProductos.length > 0" type="doughnut" :data="chartDataPie" :options="chartOptionsPie" class="w-full h-full" />
            <p v-else style="text-align: center; color: #94a3b8; font-size: 14px; padding-top: 80px;">Sin ingresos registrados.</p>
          </div>
        </div>
      </div>

      <!-- Auditoría de Stock (Movimientos Manuales/Ventas) -->
      <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 24px;">
        <h2 style="font-weight: 700; font-size: 16px; color: #1e293b; margin: 0 0 16px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
          Auditoría de Stock (Entradas / Salidas / Ajustes)
        </h2>
        <DataTable :value="movimientos" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
          <template #empty>
            <div style="text-align: center; color: #94a3b8; padding: 20px; font-size: 14px;">No se encontraron movimientos de stock en este período.</div>
          </template>
          <Column field="fecha" header="Fecha">
            <template #body="slotProps">
              <span style="font-size: 12px; color: #64748b;">{{ formatearFecha(slotProps.data.fecha) }}</span>
            </template>
          </Column>
          <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
          <Column field="producto_nombre" header="Producto" class="font-medium text-slate-800"></Column>
          <Column field="tipo_movimiento" header="Tipo">
            <template #body="slotProps">
              <Tag 
                :value="slotProps.data.tipo_movimiento" 
                :severity="slotProps.data.tipo_movimiento === 'ENTRADA' ? 'success' : slotProps.data.tipo_movimiento === 'SALIDA' ? 'danger' : 'warn'" 
              />
            </template>
          </Column>
          <Column field="cantidad" header="Cantidad" sortable></Column>
          <Column field="motivo" header="Motivo / Observación"></Column>
        </DataTable>
      </div>

      <!-- Tablas Inferiores -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <h2 style="font-weight: 700; font-size: 16px; color: #1e293b; margin: 0 0 16px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
            Top Productos Más Vendidos
          </h2>
          <DataTable :value="topProductos" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
            <template #empty>
              <div style="text-align: center; color: #94a3b8; padding: 20px; font-size: 14px;">Sin datos.</div>
            </template>
            <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
            <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
            <Column field="total_vendido" header="Vendidos" sortable></Column>
            <Column field="total_recaudado" header="Recaudado" sortable>
              <template #body="slotProps">
                <span style="font-weight: 600; color: #059669;">${{ Number(slotProps.data.total_recaudado || 0).toFixed(2) }}</span>
              </template>
            </Column>
          </DataTable>
        </div>

        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <h2 style="font-weight: 700; font-size: 16px; color: #1e293b; margin: 0 0 16px 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
            Productos con Stock Crítico
          </h2>
          <DataTable :value="stockBajo" :loading="loading" class="p-datatable-sm" responsiveLayout="scroll">
            <template #empty>
              <div style="text-align: center; color: #94a3b8; padding: 20px; font-size: 14px;">Niveles de stock óptimos.</div>
            </template>
            <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
            <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
            <Column field="stock_actual" header="Stock Actual">
              <template #body="slotProps">
                <Tag :value="slotProps.data.stock_actual" severity="danger" />
              </template>
            </Column>
            <Column field="stock_minimo" header="Stock Mínimo"></Column>
          </DataTable>
        </div>
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
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable'

const periodoSeleccionado = ref('mes');
const resumen = ref({ total_ventas_realizadas: 0, ingresos_totales: 0 });
const topProductos = ref([]);
const stockBajo = ref([]);
const movimientos = ref([]);
const loading = ref(false);

const periodos = [
  { label: 'Día', value: 'dia' },
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
  datasets: [{ label: 'Unidades Vendidas', backgroundColor: '#2563eb', borderRadius: 8, data: topProductos.value.map(p => p.total_vendido) }]
}));

const chartOptionsBar = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } };

const chartDataPie = computed(() => ({
  labels: topProductos.value.map(p => p.nombre),
  datasets: [{ data: topProductos.value.map(p => p.total_recaudado), backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'] }]
}));

const chartOptionsPie = { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } };

const cambiarPeriodo = (nuevoPeriodo) => {
  periodoSeleccionado.value = nuevoPeriodo;
  cargarReportes();
};

const cargarReportes = async () => {
  loading.value = true;
  try {
    const [resumenRes, topRes, stockBajoRes, movRes] = await Promise.all([
      api.get(`/reportes/resumen?periodo=${periodoSeleccionado.value}`),
      api.get(`/reportes/top-productos?periodo=${periodoSeleccionado.value}`),
      api.get('/reportes/stock-bajo'),
      api.get(`/reportes/movimientos?periodo=${periodoSeleccionado.value}`)
    ]);

    resumen.value = resumenRes.data;
    topProductos.value = topRes.data;
    stockBajo.value = stockBajoRes.data;
    movimientos.value = movRes.data;
  } catch (error) {
    console.error('Error al cargar reportes:', error);
  } finally {
    loading.value = false;
  }
};

const exportarPDF = () => {
  const doc = new jsPDF();

  // 1. Encabezado Principal
  doc.setFillColor(30, 41, 59); // Slate-800
  doc.rect(0, 0, 210, 28, 'F');
  
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.text('ERP System - Reporte Ejecutivo BI', 14, 18);
  
  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.text(`Período: ${etiquetaPeriodo.value.toUpperCase()} | Generado: ${new Date().toLocaleDateString('es-MX')}`, 130, 18);

  // 2. Tarjetas de Resumen Financiero (KPIs)
  doc.setTextColor(30, 41, 59);
  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.text('Resumen Financiero', 14, 38);

  // Cajas KPI
  const kpis = [
    { label: 'Ingresos Totales', val: `$${Number(resumen.value.ingresos_totales || 0).toFixed(2)}` },
    { label: 'Ventas Completadas', val: `${resumen.value.total_ventas_realizadas || 0}` },
    { label: 'Ticket Promedio', val: `$${ticketPromedio.value.toFixed(2)}` },
    { label: 'Alertas de Stock', val: `${stockBajo.value.length}` }
  ];

  kpis.forEach((kpi, idx) => {
    const x = 14 + (idx * 46);
    doc.setFillColor(248, 250, 252);
    doc.setDrawColor(226, 232, 240);
    doc.roundedRect(x, 42, 42, 20, 2, 2, 'FD');

    doc.setFontSize(7);
    doc.setTextColor(100, 116, 139);
    doc.text(kpi.label.toUpperCase(), x + 4, 48);

    doc.setFontSize(11);
    doc.setTextColor(15, 23, 42);
    doc.setFont('helvetica', 'bold');
    doc.text(kpi.val, x + 4, 58);
  });

  let currentY = 70;

  // 3. Tabla: Top Productos Más Vendidos
  doc.setFontSize(10);
  doc.setTextColor(30, 41, 59);
  doc.text('Top Productos Más Vendidos', 14, currentY);

  autoTable(doc, {
    startY: currentY + 4,
    head: [['SKU', 'Producto', 'Unidades Vendidas', 'Total Recaudado']],
    body: topProductos.value.map(p => [
      p.sku,
      p.nombre,
      p.total_vendido,
      `$${Number(p.total_recaudado || 0).toFixed(2)}`
    ]),
    theme: 'grid',
    headStyles: { fillColor: [37, 99, 235], textColor: 255, fontStyle: 'bold' },
    styles: { fontSize: 8, cellPadding: 2.5 }
  });

  currentY = doc.lastAutoTable.finalY + 10;

  // 4. Tabla: Auditoría de Movimientos de Stock
  doc.setFontSize(10);
  doc.setTextColor(30, 41, 59);
  doc.text('Auditoría de Stock (Entradas / Salidas / Ajustes)', 14, currentY);

  autoTable(doc, {
    startY: currentY + 4,
    head: [['Fecha', 'SKU', 'Producto', 'Tipo', 'Cantidad', 'Motivo / Observación']],
    body: movimientos.value.map(m => [
      formatearFecha(m.fecha),
      m.sku,
      m.producto_nombre,
      m.tipo_movimiento,
      m.cantidad,
      m.motivo || 'N/A'
    ]),
    theme: 'striped',
    headStyles: { fillColor: [71, 85, 105], textColor: 255, fontStyle: 'bold' },
    styles: { fontSize: 8, cellPadding: 2.5 }
  });

  currentY = doc.lastAutoTable.finalY + 10;

  // 5. Tabla: Alertas de Stock Bajo (Si aplica)
  if (stockBajo.value.length > 0) {
    if (currentY > 230) {
      doc.addPage();
      currentY = 20;
    }

    doc.setFontSize(10);
    doc.setTextColor(225, 29, 72); // Rose-600
    doc.text('Productos con Nivel Crítico de Stock', 14, currentY);

    autoTable(doc, {
      startY: currentY + 4,
      head: [['SKU', 'Producto', 'Stock Actual', 'Stock Mínimo']],
      body: stockBajo.value.map(sb => [
        sb.sku,
        sb.nombre,
        sb.stock_actual,
        sb.stock_minimo
      ]),
      theme: 'grid',
      headStyles: { fillColor: [225, 29, 72], textColor: 255, fontStyle: 'bold' },
      styles: { fontSize: 8, cellPadding: 2.5 }
    });
  }

  // Guardar archivo PDF estructurado
  doc.save(`reporte_ejecutivo_${periodoSeleccionado.value}_${new Date().toISOString().slice(0, 10)}.pdf`);
};


const exportarCSV = () => {
  if (topProductos.value.length === 0) return;
  let csvContent = "data:text/csv;charset=utf-8,SKU,Producto,Total Vendido,Total Recaudado ($)\n";
  topProductos.value.forEach(p => { csvContent += `${p.sku},${p.nombre},${p.total_vendido},${p.total_recaudado}\n`; });
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `reporte_${periodoSeleccionado.value}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return '';
  return new Date(fechaStr).toLocaleString('es-MX', { dateStyle: 'short', timeStyle: 'short' });
};

onMounted(() => {
  cargarReportes();
});
</script>