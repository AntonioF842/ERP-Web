<template>
  <div class="space-y-6">
    <!-- Encabezado de Sección -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Gestión de Inventario</h1>
        <p class="text-slate-500 text-sm">Administra los productos y existencias de la empresa</p>
      </div>
      <Button label="Nuevo Producto" icon="pi pi-plus" class="p-button-primary" @click="openNewModal" />
    </div>

    <!-- Tabla de Productos -->
    <Card class="shadow-sm">
      <template #content>
        <DataTable 
          :value="productos" 
          :loading="loading" 
          paginator 
          :rows="10" 
          dataKey="id"
          class="p-datatable-sm"
        >
          <template #header>
            <div class="flex justify-between items-center">
              <span class="text-lg font-semibold text-slate-700">Listado de Productos</span>
              <Button icon="pi pi-refresh" text rounded @click="cargarProductos" />
            </div>
          </template>

          <template #empty> No se encontraron productos registrados. </template>

          <Column field="sku" header="SKU" sortable></Column>
          <Column field="nombre" header="Nombre" sortable></Column>
          <Column field="precio" header="Precio" sortable>
            <template #body="slotProps">
              ${{ Number(slotProps.data.precio).toFixed(2) }}
            </template>
          </Column>
          <Column field="stock" header="Stock" sortable>
            <template #body="slotProps">
              <Tag 
                :value="slotProps.data.stock" 
                :severity="slotProps.data.stock <= slotProps.data.stock_minimo ? 'danger' : 'success'" 
              />
            </template>
          </Column>
          <Column header="Acciones" style="width: 10rem">
            <template #body="slotProps">
              <div class="flex gap-2">
                <Button icon="pi pi-pencil" severity="warn" text rounded @click="editProducto(slotProps.data)" />
              </div>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>

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

        <div class="flex flex-col gap-2">
          <label for="sku" class="font-semibold text-slate-700">SKU / Código</label>
          <InputText id="sku" v-model.trim="productoForm.sku" required autofocus />
        </div>

        <div class="flex flex-col gap-2">
          <label for="nombre" class="font-semibold text-slate-700">Nombre del Producto</label>
          <InputText id="nombre" v-model.trim="productoForm.nombre" required />
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-2">
                <label for="precio_venta" class="font-semibold text-slate-700">Precio Venta ($)</label>
                <InputNumber id="precio_venta" v-model="productoForm.precio_venta" mode="currency" currency="USD" locale="en-US" :min="0" />
            </div>

            <div class="flex flex-col gap-2">
                <label for="costo_compra" class="font-semibold text-slate-700">Costo Compra ($)</label>
                <InputNumber id="costo_compra" v-model="productoForm.costo_compra" mode="currency" currency="USD" locale="en-US" :min="0" />
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-2">
                <label for="stock_actual" class="font-semibold text-slate-700">Stock Inicial</label>
                <InputNumber id="stock_actual" v-model="productoForm.stock_actual" :min="0" />
            </div>

            <div class="flex flex-col gap-2">
                <label for="stock_minimo" class="font-semibold text-slate-700">Stock Mínimo</label>
                <InputNumber id="stock_minimo" v-model="productoForm.stock_minimo" :min="0" />
            </div>
        </div>
      </div>

      <template #footer>
        <Button label="Cancelar" icon="pi pi-times" text @click="hideDialog" />
        <Button label="Guardar" icon="pi pi-check" :loading="saving" @click="saveProducto" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/axios';
import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Message from 'primevue/message';

const productos = ref([]);
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
  productoForm.value = { sku: '', nombre: '', precio: 0, stock: 0, stock_minimo: 5 };
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