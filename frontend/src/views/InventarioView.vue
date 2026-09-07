<template>
  <div class="max-w-7xl mx-auto space-y-6">
    <!-- Encabezado de Sección -->
    <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Gestión de Inventario</h1>
        <p class="text-slate-500 text-sm mt-1">Administra los productos, precios y existencias en tiempo real</p>
      </div>
      <Button label="Nuevo Producto" icon="pi pi-plus" class="p-button-primary shrink-0" @click="openNewModal" />
    </div>

    <!-- Indicadores Rápidos -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Productos</p>
          <h3 class="text-2xl font-extrabold text-slate-800 mt-1">{{ productos.length }}</h3>
        </div>
        <div class="p-3.5 bg-blue-50 text-blue-600 rounded-xl">
          <i class="pi pi-box text-xl"></i>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Stock en Alerta</p>
          <h3 class="text-2xl font-extrabold text-slate-800 mt-1">{{ productosCriticos }}</h3>
        </div>
        <div class="p-3.5 bg-rose-50 text-rose-600 rounded-xl">
          <i class="pi pi-exclamation-triangle text-xl"></i>
        </div>
      </div>

      <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Valor Estimado</p>
          <h3 class="text-2xl font-extrabold text-slate-800 mt-1">${{ valorTotalInventario.toFixed(2) }}</h3>
        </div>
        <div class="p-3.5 bg-emerald-50 text-emerald-600 rounded-xl">
          <i class="pi pi-dollar text-xl"></i>
        </div>
      </div>
    </div>

    <!-- Tabla Principal de Productos -->
    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div class="flex items-center gap-2">
          <i class="pi pi-list text-slate-500 text-lg"></i>
          <h2 class="font-bold text-slate-800 text-base">Catálogo de Productos</h2>
        </div>
        <div class="flex items-center gap-3">
          <span class="p-input-icon-left w-full sm:w-64">
            <InputText v-model="filterText" placeholder="Buscar por SKU o Nombre..." class="p-inputtext-sm w-full" />
          </span>
          <Button icon="pi pi-refresh" severity="secondary" outlined rounded size="small" @click="cargarProductos" />
        </div>
      </div>

      <DataTable 
        :value="productosFiltrados" 
        :loading="loading" 
        paginator 
        :rows="8" 
        dataKey="id"
        class="p-datatable-sm"
        responsiveLayout="scroll"
      >
        <template #empty>
          <div class="py-8 text-center text-slate-400 text-sm">
            No se encontraron productos registrados en el inventario.
          </div>
        </template>

        <Column field="sku" header="SKU" sortable class="font-mono text-xs text-slate-500"></Column>
        <Column field="nombre" header="Nombre" sortable class="font-medium text-slate-800"></Column>
        <Column field="precio_venta" header="Precio Venta" sortable>
          <template #body="slotProps">
            <span class="font-semibold text-slate-700">${{ Number(slotProps.data.precio_venta || 0).toFixed(2) }}</span>
          </template>
        </Column>
        <Column field="costo_compra" header="Costo Compra" sortable>
          <template #body="slotProps">
            <span class="text-slate-500">${{ Number(slotProps.data.costo_compra || 0).toFixed(2) }}</span>
          </template>
        </Column>
        <Column field="stock_actual" header="Stock" sortable>
          <template #body="slotProps">
            <Tag 
              :value="slotProps.data.stock_actual" 
              :severity="slotProps.data.stock_actual <= slotProps.data.stock_minimo ? 'danger' : 'success'" 
            />
          </template>
        </Column>
        <Column header="Acciones" style="width: 6rem" class="text-center">
          <template #body="slotProps">
            <Button icon="pi pi-pencil" severity="secondary" text rounded size="small" @click="editProducto(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Modal Formulario (Crear / Editar) -->
    <Dialog 
      v-model:visible="productDialog" 
      :header="isEdit ? 'Editar Producto' : 'Nuevo Producto'" 
      :modal="true" 
      class="p-fluid w-full max-w-lg"
    >
      <div class="flex flex-col gap-4 mt-2">
        <Message v-if="errorMessage" severity="error" :closable="false">
          {{ errorMessage }}
        </Message>

        <div class="flex flex-col gap-1.5">
          <label for="sku" class="font-semibold text-slate-700 text-sm">SKU / Código Único</label>
          <InputText id="sku" v-model.trim="productoForm.sku" required autofocus placeholder="Ej: PROD-001" />
        </div>

        <div class="flex flex-col gap-1.5">
          <label for="nombre" class="font-semibold text-slate-700 text-sm">Nombre del Producto</label>
          <InputText id="nombre" v-model.trim="productoForm.nombre" required placeholder="Nombre descriptivo" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-1.5">
            <label for="precio_venta" class="font-semibold text-slate-700 text-sm">Precio Venta ($)</label>
            <InputNumber id="precio_venta" v-model="productoForm.precio_venta" mode="currency" currency="USD" locale="en-US" :min="0" />
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="costo_compra" class="font-semibold text-slate-700 text-sm">Costo Compra ($)</label>
            <InputNumber id="costo_compra" v-model="productoForm.costo_compra" mode="currency" currency="USD" locale="en-US" :min="0" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="flex flex-col gap-1.5">
            <label for="stock_actual" class="font-semibold text-slate-700 text-sm">Stock Inicial</label>
            <InputNumber id="stock_actual" v-model="productoForm.stock_actual" :min="0" />
          </div>

          <div class="flex flex-col gap-1.5">
            <label for="stock_minimo" class="font-semibold text-slate-700 text-sm">Stock Mínimo (Alerta)</label>
            <InputNumber id="stock_minimo" v-model="productoForm.stock_minimo" :min="0" />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2 pt-2">
          <Button label="Cancelar" icon="pi pi-times" text severity="secondary" @click="hideDialog" />
          <Button label="Guardar" icon="pi pi-check" :loading="saving" @click="saveProducto" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../api/axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Message from 'primevue/message';

const productos = ref([]);
const filterText = ref('');
const loading = ref(false);
const saving = ref(false);
const productDialog = ref(false);
const isEdit = ref(false);
const selectedId = ref(null);
const errorMessage = ref('');

const productoForm = ref({
  sku: '',
  nombre: '',
  descripcion: '',
  precio_venta: 0,
  costo_compra: 0,
  stock_actual: 0,
  stock_minimo: 5
});

const productosFiltrados = computed(() => {
  if (!filterText.value.trim()) return productos.value;
  const term = filterText.value.toLowerCase();
  return productos.value.filter(
    p => p.nombre.toLowerCase().includes(term) || p.sku.toLowerCase().includes(term)
  );
});

const productosCriticos = computed(() => {
  return productos.value.filter(p => p.stock_actual <= p.stock_minimo).length;
});

const valorTotalInventario = computed(() => {
  return productos.value.reduce((acc, p) => acc + (p.precio_venta * p.stock_actual), 0);
});

const cargarProductos = async () => {
  loading.value = true;
  try {
    const response = await api.get('/inventario/productos');
    productos.value = response.data;
  } catch (error) {
    console.error('Error al cargar productos:', error);
  } finally {
    loading.value = false;
  }
};

const openNewModal = () => {
  isEdit.value = false;
  selectedId.value = null;
  errorMessage.value = '';
  productoForm.value = { sku: '', nombre: '', descripcion: '', precio_venta: 0, costo_compra: 0, stock_actual: 0, stock_minimo: 5 };
  productDialog.value = true;
};

const editProducto = (producto) => {
  isEdit.value = true;
  selectedId.value = producto.id;
  errorMessage.value = '';
  productoForm.value = { ...producto };
  productDialog.value = true;
};

const hideDialog = () => {
  productDialog.value = false;
};

const saveProducto = async () => {
  saving.value = true;
  errorMessage.value = '';
  
  const payload = {
    sku: productoForm.value.sku,
    nombre: productoForm.value.nombre,
    descripcion: productoForm.value.descripcion || '',
    precio_venta: Number(productoForm.value.precio_venta) || 0,
    costo_compra: Number(productoForm.value.costo_compra) || 0,
    stock_actual: Number(productoForm.value.stock_actual) || 0,
    stock_minimo: Number(productoForm.value.stock_minimo) || 0
  };

  try {
    if (isEdit.value) {
      await api.put(`/inventario/productos/${selectedId.value}`, payload);
    } else {
      await api.post('/inventario/productos', payload);
    }
    productDialog.value = false;
    await cargarProductos();
  } catch (error) {
    if (error?.response?.status === 422) {
      const details = error.response.data?.detail;
      errorMessage.value = Array.isArray(details)
        ? details.map(d => `${d.loc?.[d.loc.length - 1] || 'campo'}: ${d.msg}`).join(', ')
        : 'Datos con formato inválido.';
    } else {
      errorMessage.value = error?.response?.data?.detail || error?.message || 'Error al guardar el producto.';
    }
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  cargarProductos();
});
</script>