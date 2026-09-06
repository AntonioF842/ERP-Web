<template>
  <div class="space-y-6">
    <!-- Encabezado -->
    <div>
      <h1 class="text-2xl font-bold text-slate-800">Terminal de Ventas (POS)</h1>
      <p class="text-slate-500 text-sm">Selecciona productos, gestiona la orden y procesa la transacción</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Columna Izquierda: Búsqueda y Selección de Productos -->
      <div class="lg:col-span-2 space-y-4">
        <Card class="shadow-sm">
          <template #title>
            <span class="text-lg font-semibold text-slate-700">Catálogo de Productos</span>
          </template>
          <template #content>
            <DataTable 
              :value="productos" 
              :loading="loadingProductos" 
              paginator 
              :rows="5" 
              class="p-datatable-sm"
            >
              <template #empty> No hay productos disponibles en inventario. </template>
              <Column field="sku" header="SKU"></Column>
              <Column field="nombre" header="Producto"></Column>
              <Column field="precio_venta" header="Precio">
                <template #body="slotProps">
                  ${{ Number(slotProps.data.precio_venta || 0).toFixed(2) }}
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
              <Column header="Acción" style="width: 6rem">
                <template #body="slotProps">
                  <Button 
                    icon="pi pi-plus" 
                    severity="success" 
                    rounded 
                    text 
                    :disabled="slotProps.data.stock_actual <= 0"
                    @click="agregarAlCarrito(slotProps.data)" 
                  />
                </template>
              </Column>
            </DataTable>
          </template>
        </Card>
      </div>

      <!-- Columna Derecha: Resumen del Carrito y Detalle de Pago -->
      <div class="space-y-4">
        <Card class="shadow-sm border-t-4 border-blue-600">
          <template #title>
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold text-slate-700">Detalle de la Venta</span>
              <Button icon="pi pi-trash" severity="danger" text rounded @click="limpiarCarrito" :disabled="carrito.length === 0" />
            </div>
          </template>
          <template #content>
            <Message v-if="errorMessage" severity="error" class="mb-4" :closable="false">
              {{ errorMessage }}
            </Message>

            <!-- Lista de items en Carrito -->
            <div v-if="carrito.length > 0" class="divide-y divide-slate-200 mb-4 max-h-60 overflow-y-auto">
              <div v-for="(item, index) in carrito" :key="item.producto_id" class="py-2 flex justify-between items-center">
                <div class="flex-1 pr-2">
                  <p class="font-semibold text-sm text-slate-800">{{ item.nombre }}</p>
                  <p class="text-xs text-slate-500">${{ item.precio_unitario.toFixed(2) }} c/u</p>
                </div>
                <div class="flex items-center gap-2">
                  <InputNumber 
                    v-model="item.cantidad" 
                    :min="1" 
                    :max="item.stock_max" 
                    showButtons 
                    buttonLayout="horizontal" 
                    class="w-24 p-inputnumber-sm" 
                    @change="validarCantidad(item)"
                  />
                  <Button icon="pi pi-times" severity="danger" text rounded @click="removerDelCarrito(index)" />
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-slate-400">
              <i class="pi pi-shopping-cart text-4xl mb-2"></i>
              <p>El carrito está vacío</p>
            </div>

            <!-- Desglose de Totales -->
            <div class="border-t border-slate-200 pt-4 space-y-2 text-sm">
              <div class="flex justify-between text-slate-600">
                <span>Subtotal:</span>
                <span>${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>IVA (16%):</span>
                <span>${{ iva.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-lg font-bold text-slate-800 border-t border-slate-200 pt-2">
                <span>Total:</span>
                <span class="text-blue-600">${{ total.toFixed(2) }}</span>
              </div>
            </div>

            <Button 
              label="Procesar Venta" 
              icon="pi pi-check-circle" 
              class="w-full mt-6" 
              severity="primary" 
              :loading="procesando" 
              :disabled="carrito.length === 0" 
              @click="procesarVenta" 
            />
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../api/axios';
import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import InputNumber from 'primevue/inputnumber';
import Message from 'primevue/message';

const productos = ref([]);
const carrito = ref([]);
const loadingProductos = ref(false);
const procesando = ref(false);
const errorMessage = ref('');

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
      cantidad: item.cantidad,
      precio_unitario: Number(item.precio_unitario)
    }))
  };

  try {
    await api.post('/ventas', payload);
    limpiarCarrito();
    await cargarProductos(); // Refrescar el stock en la tabla tras la venta
  } catch (error) {
    if (error?.response?.status === 422) {
      const details = error.response.data?.detail;
      errorMessage.value = Array.isArray(details)
        ? details.map((d) => `${d.loc?.[d.loc.length - 1] || 'campo'}: ${d.msg}`).join(', ')
        : 'Datos con formato inválido.';
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