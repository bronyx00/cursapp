import { defineStore } from "pinia";
import apiClient from "@/services/apiClient";
import type { MiCursoInscrito, CursoList } from "@/types/cursos.types";

export interface ProgresoReciente {
    id: number;
    leccion: { id: number; titulo: string; };
    modulo: { id: number; titulo: string; };
    curso: CursoList;
    ultima_vista: string;
}

export const useLearningStore = defineStore('learning', {
    state: () => ({
        misCursos: [] as MiCursoInscrito[],
        cursoReciente: null as ProgresoReciente | null,
        isLoading: false,
        isLoadingReciente: true,
    }),
    actions: {
        async fetchMisCursos() {
        /** Obtiene los cursos en los que el alumno está inscrito y pagado. */    
            // No recargar si ya los tenemos
            if (this.misCursos.length > 0) return;

            this.isLoading = true;
            try {
                // Llama al endpoint del backend
                const { data } = await apiClient.get('/evaluacion/mi-aprendizaje/');

                this.misCursos = data.results;
            } catch (error) {
                console.error("Error al cargar 'Mi Aprendizaje':", error);
            } finally {
                this.isLoading = false;
            }
        },

        async fetchCursoReciente() {
            if (this.cursoReciente) return; // No recargar
            this.isLoadingReciente = true;
            try {
                // Llama al endpoint de ultima vista
                const { data } = await apiClient.get('/evaluacion/mi-progreso/continuar/');
                this.cursoReciente = data;
            } catch (error) {
                // 404 si el usuario no ha visto nada
                if ((error as any).response?.status !== 404) {
                    console.error("Error al cargar 'Progreso Reciente':", error);
                }
            } finally {
                this.isLoadingReciente = false;
            }
        }
    }
});