import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient';
import type { CursoList } from '@/types/cursos.types';

export const useRecommendationStore = defineStore('recommendation', {
    state: () => ({
        cursosRecomendados: [] as CursoList[],
        isLoading: false,
    }),
    actions: {
        async fetchRecomendaciones() {
            // No recarga si ya tenemos
            if (this.cursosRecomendados.length > 0) return;

            this.isLoading = true;
            try {
                // Llama al endpoint de recomendaciones
                const { data } = await apiClient.get('/recomendacion/cursos/');
                this.cursosRecomendados = data.results;
            } catch (error) {
                console.error("Error al cargar Recomendaciones:", error);
            } finally {
                this.isLoading = false;
            }
        }
    }
});