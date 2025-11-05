import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient';
import type { CursoList } from '@/types/cursos.types';

export const useCatalogStore = defineStore('catalog', {
    state: () => ({
        cursos: [] as CursoList[],
        isLoading: false,
    }),
    actions: {
        /**
         * Obtiene la lista pública de cursos del catálogo.
         */
        async fetchCursos() {
            if (this.cursos.length > 0) return; // Evitar recargas
            
            this.isLoading = true;
            try {
                const { data } = await apiClient.get('cursos/catalogo/');

                this.cursos = data.results;
            } catch (error) {
                console.error("Error al cargar el catálogo:", error);
            } finally {
                this.isLoading = false;
            }
        }
    }
});