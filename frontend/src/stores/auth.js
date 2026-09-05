import { defineStore } from 'pinia'
import api from '../api/axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
    actions: {
        async login(email, password) {
            const params = new URLSearchParams();
            params.append( 'username', email );
            params.append( 'password', password );

            const response = await api.post('/usuarios/login', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            this.token = response.data.access_token;
            localStorage.setItem('token', this.token);
            await this.fetchProfile();
        },
        async fetchProfile() {
            if (!this.token) return;
            try {
                const response = await api.get('/usuarios/me');
                this.user = response.data;
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        }
    }
})