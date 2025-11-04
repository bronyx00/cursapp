import { defineStore } from "pinia";
import apiClient from "@/services/apiClient";
import type { MiCursoInscrito } from "@/types/cursos.types";

export const useLearningStore = defineStore('learning', {
    state: () => ({
        misCursos: [] as MiCursoInscrito[],
        isLoading: false,
    }),
    actions: {
        /** Obtiene los cursos en los que el alumno está inscrito y pagado. */
        async fetchMisCursos() {
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
        }
    }
});