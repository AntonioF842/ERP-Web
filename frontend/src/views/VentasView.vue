<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h1 class="text-2xl font-bold text-slate-900">Terminal de Ventas (POS)</h1>
      <p class="text-slate-500 text-sm mt-1">Selecciona productos, gestiona la orden y procesa la transacción</p>
    </div>

    <!-- Rejilla Principal: 2 columnas en pantallas grandes (2/3 Catálogo + 1/3 Carrito) -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
      
      <!-- Columna Izquierda: Catálogo (lg:col-span-2) -->
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
            <div class="py-8 text-center text-slate-400 text-sm">
              No hay productos disponibles en inventario.
            </div>
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

      <!-- Columna Derecha: Detalle de Venta / Carrito (1/3) -->
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

        <Message v-if="errorMessage" severity="error" :closable="false">
          {{ errorMessage }}
        </Message>

        <!-- Productos en Carrito -->
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

        <!-- Totales -->
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../api/axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import Message from 'primevue/message';

const productos = ref([]);
const carrito = ref([]);
const filterText = ref('');
const loadingProductos = ref(false);
const procesando = ref(false);
const errorMessage = ref('');

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
      cantidad: Number(item.cantidad),
      precio_unitario: Number(item.precio_unitario)
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

onMounted(() => {
  cargarProductos();
});
</script>