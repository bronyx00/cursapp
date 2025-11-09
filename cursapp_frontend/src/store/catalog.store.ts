import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient';
import type { CursoList, Categoria } from '@/types/cursos.types';

export const useCatalogStore = defineStore('catalog', {
    state: () => ({
        popularCourses: [] as CursoList[],
        newCourses: [] as CursoList[],
        cursos: [] as CursoList[],
        categorias: [] as Categoria[],
        isLoading: false,
        isLoadingCategorias: false,
    }),
    actions: {
        async fetchPopularCourses() {
            /**
             * Obtiene los cursos más populares (ordenado por reseñas).
             */
            if (this.popularCourses.length > 0) return; // Evitar recargas

            this.isLoading = true;
            try {
                const { data } = await apiClient.get('cursos/catalogo/', {
                    params: { ordering: '-total_resenas' }
                });
                this.popularCourses = data.results;
            } catch (error) {
                console.error("Error al cargar cursos populares:", error);
            } finally {
                this.isLoading = false;
            }
        },
        async fetchNewCourses() {
            /**
             * Obtiene los cursos más nuevos (ordenados por fecha).
             */
            if (this.newCourses.length > 0) return; // Evitar recargas

            this.isLoading = true;
            try {
                const { data } = await apiClient.get('cursos/catalogo/', {
                    params: { ordering: '-fecha_creacion' }
                });
                this.newCourses = data.results;
            } catch (error) {
                console.error("Error al cargar cursos nuevos:", error);
            } finally {
                this.isLoading = false
            }
        },
        async fetchCursos() {
            /**
             * Obtiene la lista pública de cursos del catálogo.
             */
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
        },
        async fetchCategorias() {
            /**
             * Obtiene la lista pública de géneros de cursos del catálogo.
             */
            if (this.categorias.length > 0) return;
            this.isLoadingCategorias = true;
            try {
                const { data } = await apiClient.get('/cursos/categorias/');
                this.categorias = data.results;
            } catch (error) {
                console.error("Error al cargar categorías:", error);
            } finally {
                this.isLoadingCategorias = false;
            }
        }
    }
});