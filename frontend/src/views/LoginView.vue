<template>
    <div class="flex items-center justify-center min-h-screen bg-slate-100">
        <Card class="w-full max-w-md shadow-lg">
            <template #title>
                <div class="text-center font-bold text-2xl text-slate-800">
                    Acceso al ERP
                </div>
            </template>
            <template #subtitle>
                <div class="text-center text-slate-500 mb-4">
                    Ingrese sus credenciales de usuario
                </div>
            </template>
            <template #content>
                <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
                    <Message v-if="errorMessage" severity="error" :closable="false">
                        {{ errorMessage }}
                    </Message>

                    <div class="flex flex-col gap-2">
                        <label for="email" class="font-semibold text-slate-700">Correo Electrónico</label> 
                        <InputText id="email" v-model="email" type="email" placeholder="usuario@erp.com" required />
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="password" class="font-semibold text-slate-700">Contraseña</label>
                        <InputText id="password" v-model="password" type="password" placeholder="••••••••" required />
                    </div>

                    <Button type="submit" label="Iniciar Sesión" icon="pi pi-sign-in" :loading="loading" class="mt-2" />                   
                </form>
            </template>
        </Card>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import  Card  from 'primevue/card';
import  InputText  from 'primevue/inputtext';
import  Button  from 'primevue/button';
import  Message  from 'primevue/message';

const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMessage = ref('');

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
    loading.value = true;
    errorMessage.value = '';
    try {
        await authStore.login(email.value, password.value);
        router.push('/dashboard');
    } catch (error) {
        errorMessage.value = error.response?.data?.detail || 'Error de conexión con el servidor';
    } finally {
        loading.value = false;
    }
};
</script>