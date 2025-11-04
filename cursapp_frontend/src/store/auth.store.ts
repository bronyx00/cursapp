import { defineStore } from "pinia";
import apiClient from "@/services/apiClient";
import type { UserProfile } from "@/types/user.types";
import router from '@/router'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
        user: null as UserProfile | null, 
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        esAlumno: (state) => state.user?.rol === 3,
        esInstructor: (state) => state.user?.rol === 2,
    },

    actions: {
        async login(credentials: { username: string, password: string }) {
            try {
                // API de Login
                const { data } = await apiClient.post('/auth/login/', credentials);

                this.accessToken = data.access;
                this.refreshToken = data.refresh;
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                // Después de loguear, pide el perfil del usuario
                await this.fetchProfile();
            } catch (error) {
                console.error('Error de login:', error);
                throw error;
            }
        },

        async fetchProfile() {
            if (!this.accessToken) return;
            try {
                // API de perfil
                const { data } = await apiClient.get('/auth/perfil/');
                this.user = data;
            } catch (error) {
                console.error('Error fetching profile:', error);
                this.logout(); // Si el token es inválido, desloguea
            }
        },

        logout() {
            this.accessToken = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            router.push('/login');
        },
    },
});