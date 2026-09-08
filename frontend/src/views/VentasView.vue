<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado y Selector de Pestaña -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Módulo de Ventas</h1>
        <p class="text-slate-500 text-sm mt-1">Terminal de punto de venta e historial de operaciones</p>
      </div>

      <!-- Selector de Pestaña -->
      <div class="flex items-center gap-2 bg-slate-100 p-1 rounded-xl">
        <button 
          @click="activeTab = 'pos'"
          :class="[
            'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2',
            activeTab === 'pos' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          <i class="pi pi-shopping-cart"></i>
          <span>Terminal POS</span>
        </button>
        <button 
          @click="activeTab = 'historial'; cargarHistorialVentas()"
          :class="[
            'px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-2',
            activeTab === 'historial' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
          ]"
        >
          <i class="pi pi-history"></i>
          <span>Historial de Ventas</span>
        </button>
      </div>
    </div>

    <!-- PESTAÑA 1: TERMINAL POS -->
    <div v-if="activeTab === 'pos'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      <!-- Columna Izquierda: Catálogo (2/3) -->
      <div class="lg:col-span-2 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div class="flex items-center gap-2">
            <i class="pi pi-shopping-bag text-slate-500 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Catálogo de Productos</h2>
          </div>
          <span class="p-input-icon-left w-full sm:w-64">
            <InputText v-model="filterText" placeholder="Buscar producto..." class="p-inputtext-sm w-full" />
          </span>
        </div>

        <DataTable 
          :value="productosFiltrados" 
          :loading="loadingProductos" 
          paginator 
          :rows="5" 
          class="p-datatable-sm"
          responsiveLayout="scroll"
        >
          <template #empty>
            <div class="py-8 text-center text-slate-400 text-sm">No hay productos disponibles en inventario.</div>
          </template>

          <Column field="sku" header="SKU" class="font-mono text-xs text-slate-500"></Column>
          <Column field="nombre" header="Producto" class="font-medium text-slate-800"></Column>
          <Column field="precio_venta" header="Precio">
            <template #body="slotProps">
              <span class="font-semibold text-slate-700">${{ Number(slotProps.data.precio_venta || 0).toFixed(2) }}</span>
            </template>
          </Column>
          <Column field="stock_actual" header="Stock Dispo.">
            <template #body="slotProps">
              <Tag 
                :value="slotProps.data.stock_actual" 
                :severity="slotProps.data.stock_actual > 0 ? 'success' : 'danger'" 
              />
            </template>
          </Column>
          <Column header="Acción" style="width: 5rem" class="text-center">
            <template #body="slotProps">
              <Button 
                icon="pi pi-plus" 
                severity="success" 
                rounded 
                size="small"
                :disabled="slotProps.data.stock_actual <= 0"
                @click="agregarAlCarrito(slotProps.data)" 
              />
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Columna Derecha: Detalle de Venta (1/3) -->
      <div class="bg-white rounded-2xl border border-slate-200 border-t-4 border-t-blue-600 shadow-sm p-6 space-y-4">
        <div class="flex justify-between items-center border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <i class="pi pi-shopping-cart text-blue-600 text-lg"></i>
            <h2 class="font-bold text-slate-800 text-base">Detalle de la Venta</h2>
          </div>
          <Button 
            icon="pi pi-trash" 
            severity="danger" 
            text 
            rounded 
            size="small"
            @click="limpiarCarrito" 
            :disabled="carrito.length === 0" 
          />
        </div>

        <Message v-if="errorMessage" severity="error" :closable="false">{{ errorMessage }}</Message>

        <div v-if="carrito.length > 0" class="divide-y divide-slate-100 max-h-64 overflow-y-auto pr-1 space-y-2">
          <div v-for="(item, index) in carrito" :key="item.producto_id" class="pt-2 flex justify-between items-center gap-2">
            <div class="flex-1 min-w-0">
              <p class="font-semibold text-sm text-slate-800 truncate">{{ item.nombre }}</p>
              <p class="text-xs text-slate-400">${{ item.precio_unitario.toFixed(2) }} c/u</p>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <InputNumber 
                v-model="item.cantidad" 
                :min="1" 
                :max="item.stock_max" 
                showButtons 
                buttonLayout="horizontal" 
                class="w-24 p-inputnumber-sm" 
                @change="validarCantidad(item)"
              />
              <Button icon="pi pi-times" severity="secondary" text rounded size="small" @click="removerDelCarrito(index)" />
            </div>
          </div>
        </div>

        <div v-else class="text-center py-10 text-slate-400">
          <i class="pi pi-shopping-cart text-3xl mb-2 text-slate-300"></i>
          <p class="text-sm font-medium">El carrito está vacío</p>
        </div>

        <div class="border-t border-slate-100 pt-4 space-y-2 text-sm">
          <div class="flex justify-between text-slate-500">
            <span>Subtotal:</span>
            <span class="font-medium">${{ subtotal.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-slate-500">
            <span>IVA (16%):</span>
            <span class="font-medium">${{ iva.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-lg font-bold text-slate-900 border-t border-slate-100 pt-3">
            <span>Total:</span>
            <span class="text-blue-600">${{ total.toFixed(2) }}</span>
          </div>
        </div>

        <Button 
          label="Procesar Venta" 
          icon="pi pi-check-circle" 
          class="w-full mt-4 p-button-primary" 
          :loading="procesando" 
          :disabled="carrito.length === 0" 
          @click="procesarVenta" 
        />
      </div>
    </div>

    <!-- PESTAÑA 2: HISTORIAL DE VENTAS -->
    <div v-else-if="activeTab === 'historial'" class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-100 pb-4">
        <div class="flex items-center gap-2">
          <i class="pi pi-list text-slate-500 text-lg"></i>
          <h2 class="font-bold text-slate-800 text-base">Registro General de Transacciones</h2>
        </div>
        <Button icon="pi pi-refresh" severity="secondary" outlined rounded size="small" @click="cargarHistorialVentas" />
      </div>

      <DataTable 
        :value="ventasHistorial" 
        :loading="loadingHistorial" 
        paginator 
        :rows="10" 
        class="p-datatable-sm"
        responsiveLayout="scroll"
      >
        <template #empty>
          <div class="py-8 text-center text-slate-400 text-sm">No se encontraron ventas registradas.</div>
        </template>

        <Column field="id" header="Folio Venta" sortable class="font-mono text-xs text-slate-500">
          <template #body="slotProps">#{{ slotProps.data.id }}</template>
        </Column>
        <Column field="fecha" header="Fecha y Hora" sortable>
          <template #body="slotProps">
            <span class="text-xs text-slate-600">{{ formatearFecha(slotProps.data.fecha) }}</span>
          </template>
        </Column>
        <Column field="total" header="Total" sortable>
          <template #body="slotProps">
            <span class="font-bold text-slate-800">${{ Number(slotProps.data.total).toFixed(2) }}</span>
          </template>
        </Column>
        <Column field="estado" header="Estado">
          <template #body="slotProps">
            <Tag 
              :value="slotProps.data.estado" 
              :severity="slotProps.data.estado === 'COMPLETADA' ? 'success' : 'danger'" 
            />
          </template>
        </Column>
        <Column header="Acciones" style="width: 8rem" class="text-center">
          <template #body="slotProps">
            <div class="flex items-center justify-center gap-1">
              <Button icon="pi pi-eye" severity="info" text rounded size="small" title="Ver Ticket / Detalle" @click="verDetalleVenta(slotProps.data)" />
              <Button 
                v-if="slotProps.data.estado === 'COMPLETADA'" 
                icon="pi pi-ban" 
                severity="danger" 
                text 
                rounded 
                size="small" 
                title="Cancelar Venta" 
                @click="confirmarCancelacion(slotProps.data)" 
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Modal Detalle / Ticket de Venta -->
    <Dialog 
      v-model:visible="ticketDialog" 
      header="Detalle de Transacción" 
      :modal="true" 
      class="p-fluid w-full max-w-md"
    >
      <!-- Contenedor con estilos CSS tradicionales (sin oklch) para html2pdf -->
      <div 
        id="ticket-imprimible" 
        style="background-color: #ffffff; color: #1e293b; font-family: sans-serif; padding: 20px; border-radius: 8px;"
      >
        <div style="text-align: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 12px;">
          <h2 style="font-weight: 800; font-size: 18px; margin: 0; text-transform: uppercase; color: #0f172a;">ERP System</h2>
          <p style="font-size: 12px; color: #64748b; margin: 4px 0 0 0;">Comprobante Digital de Venta</p>
          <p style="font-size: 12px; font-family: monospace; color: #94a3b8; margin: 4px 0 0 0;">Folio: #{{ ventaSeleccionada?.id }}</p>
          <p style="font-size: 11px; color: #94a3b8; margin: 2px 0 0 0;">{{ formatearFecha(ventaSeleccionada?.fecha) }}</p>
        </div>

        <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; margin-bottom: 12px;">
          <div 
            v-for="item in ventaSeleccionada?.detalles" 
            :key="item.id" 
            style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 12px;"
          >
            <div>
              <p style="font-weight: 600; margin: 0; color: #1e293b;">Producto ID #{{ item.producto_id }}</p>
              <p style="margin: 2px 0 0 0; color: #64748b; font-size: 11px;">{{ item.cantidad }} x ${{ item.precio_unitario.toFixed(2) }}</p>
            </div>
            <span style="font-weight: 700; color: #334155;">${{ item.subtotal.toFixed(2) }}</span>
          </div>
        </div>

        <div style="font-size: 12px;">
          <div style="display: flex; justify-content: space-between; color: #64748b; margin-bottom: 4px;">
            <span>Subtotal:</span>
            <span>${{ ventaSeleccionada?.subtotal.toFixed(2) }}</span>
          </div>
          <div style="display: flex; justify-content: space-between; color: #64748b; margin-bottom: 8px;">
            <span>IVA (16%):</span>
            <span>${{ ventaSeleccionada?.impuesto.toFixed(2) }}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 14px; color: #0f172a; border-top: 1px solid #e2e8f0; padding-top: 8px;">
            <span>Total Pagado:</span>
            <span style="color: #2563eb;">${{ ventaSeleccionada?.total.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-between gap-2 pt-2">
          <Button label="Cerrar" icon="pi pi-times" text severity="secondary" @click="ticketDialog = false" />
          <Button label="Descargar PDF" icon="pi pi-file-pdf" severity="primary" @click="descargarPDF" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../api/axios';
import html2pdf from 'html2pdf.js';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import Message from 'primevue/message';
import Dialog from 'primevue/dialog';

const activeTab = ref('pos');
const productos = ref([]);
const carrito = ref([]);
const ventasHistorial = ref([]);
const filterText = ref('');
const loadingProductos = ref(false);
const loadingHistorial = ref(false);
const procesando = ref(false);
const errorMessage = ref('');
const ticketDialog = ref(false);
const ventaSeleccionada = ref(null);

const productosFiltrados = computed(() => {
  if (!filterText.value.trim()) return productos.value;
  const term = filterText.value.toLowerCase();
  return productos.value.filter(
    p => p.nombre.toLowerCase().includes(term) || p.sku.toLowerCase().includes(term)
  );
});

const subtotal = computed(() => {
  return carrito.value.reduce((acc, item) => acc + item.precio_unitario * item.cantidad, 0);
});

const iva = computed(() => subtotal.value * 0.16);
const total = computed(() => subtotal.value + iva.value);

const cargarProductos = async () => {
  loadingProductos.value = true;
  try {
    const response = await api.get('/inventario/productos');
    productos.value = response.data;
  } catch (error) {
    console.error('Error al cargar inventario:', error);
  } finally {
    loadingProductos.value = false;
  }
};

const cargarHistorialVentas = async () => {
  loadingHistorial.value = true;
  try {
    const response = await api.get('/ventas');
    ventasHistorial.value = response.data;
  } catch (error) {
    console.error('Error al cargar historial de ventas:', error);
  } finally {
    loadingHistorial.value = false;
  }
};

const agregarAlCarrito = (producto) => {
  errorMessage.value = '';
  const existente = carrito.value.find((item) => item.producto_id === producto.id);
  if (existente) {
    if (existente.cantidad < producto.stock_actual) {
      existente.cantidad++;
    } else {
      errorMessage.value = `No hay más stock disponible de ${producto.nombre}`;
    }
  } else {
    carrito.value.push({
      producto_id: producto.id,
      nombre: producto.nombre,
      precio_unitario: Number(producto.precio_venta) || 0,
      cantidad: 1,
      stock_max: producto.stock_actual
    });
  }
};

const validarCantidad = (item) => {
  if (item.cantidad > item.stock_max) {
    item.cantidad = item.stock_max;
    errorMessage.value = `Stock máximo alcanzado para ${item.nombre}`;
  }
};

const removerDelCarrito = (index) => {
  carrito.value.splice(index, 1);
};

const limpiarCarrito = () => {
  carrito.value = [];
  errorMessage.value = '';
};

const procesarVenta = async () => {
  procesando.value = true;
  errorMessage.value = '';
  
  const payload = {
    detalles: carrito.value.map((item) => ({
      producto_id: item.producto_id,
      cantidad: Number(item.cantidad)
    }))
  };

  try {
    await api.post('/ventas', payload);
    limpiarCarrito();
    await cargarProductos();
  } catch (error) {
    if (error?.response?.status === 422) {
      const details = error.response.data?.detail;
      errorMessage.value = Array.isArray(details)
        ? details.map((d) => `${d.loc?.[d.loc.length - 1] || 'campo'}: ${d.msg}`).join(', ')
        : 'Formato de venta no válido.';
    } else {
      errorMessage.value = error?.response?.data?.detail || error?.message || 'Error al procesar la venta.';
    }
  } finally {
    procesando.value = false;
  }
};

const verDetalleVenta = (venta) => {
  ventaSeleccionada.value = venta;
  ticketDialog.value = true;
};

const confirmarCancelacion = async (venta) => {
  if (confirm(`¿Estás seguro de cancelar la Venta #${venta.id}? El stock será reingresado automáticamente al inventario.`)) {
    try {
      await api.patch(`/ventas/${venta.id}/cancelar`);
      await cargarHistorialVentas();
    } catch (error) {
      alert(error?.response?.data?.detail || 'Error al cancelar la venta.');
    }
  }
};

const descargarPDF = () => {
  const element = document.getElementById('ticket-imprimible');
  const opt = {
    margin: 0.5,
    filename: `ticket_venta_${ventaSeleccionada.value.id}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
};

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return '';
  return new Date(fechaStr).toLocaleString('es-MX', {
    dateStyle: 'short',
    timeStyle: 'short'
  });
};

onMounted(() => {
  cargarProductos();
});
</script>