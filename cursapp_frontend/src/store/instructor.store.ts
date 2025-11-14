import { defineStore } from "pinia";
import apiClient from "@/services/apiClient";
import type { CursoList } from '@/types/cursos.types';

// Tipo para la data de la API
export interface InstructorStats {
    total_inscripciones: number;
    total_resenas: number;
    ganancias_totales_usd: string;
    ganancias_pendientes_usd: string;
    ganancias_pagadas_usd: string;
}

export const useInstructorStore = defineStore('instructor', {
    state: () => ({
        stats: null as InstructorStats | null,
        misCursos: [] as CursoList[],
        isLoading: false,
        isLoadingCursos: false,
    }),
    actions: {
        async fetchDashboardStats() {
            if (this.stats) return; // No recargar

            this.isLoading = true;
            try {
                const { data } = await apiClient.get('/evaluacion/instructor/dashboard/');
                this.stats = data;
            } catch (error) {
                console.error("Error al cargar stats de instructor:", error);
            } finally {
                this.isLoading = false;
            }
        },

        async fetchMisCursos() {
            if (this.misCursos.length > 0) return;
            this.isLoadingCursos = true;
            try {
                const { data } = await apiClient.get('/cursos/catalogo/');
                this.misCursos = data.results;
            } catch (error) {
                console.error("Error al cargar cursos de instructor:", error);
            } finally {
                this.isLoadingCursos = true;
            }
        }
    }
});