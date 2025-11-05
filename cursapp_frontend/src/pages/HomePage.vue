<template>
    <div class="container mx-auto px-4 py-8 md:py-16">

        <section class="text-center max-w-3xl mx-auto">
            <span class="text-base font-semibold text-accent">Tu futuro. Ahora.</span>

            <h1 class="mt-4 text-4xl md:text-6xl font-bold tracking-tighter text-foreground">
                Aprende habilidades reales, rápido.
            </h1>
            <p class="mt-6 text-lg text-muted-foreground max-w-xl mx-auto">
                CursApp es la plataforma para jóvenes que buscan dominar las tecnologías más demandadas. Sin rellenos, solo habilidades prácticas.
            </p>

            <Button size="lg" class="mt-8">
                Explirar Cursos
            </Button>
        </section>

        <section class="mt-16 md:mt-24">
            <h2 class="text-2xl md:text-3xl font-bold tracking-tight text-foreground">
                Nuestros Cursos
            </h2>

            <div v-if="catalogStore.isLoading" class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <p class="text-muted-foreground">Cargando cursos...</p>
            </div>

            <div v-else-if="catalogStore.cursos.length > 0" class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                <CourseCard
                    v-for="curso in catalogStore.cursos"
                    :key="curso.id"
                    :curso="curso"
                    :progreso="'0'"
                    :show-progress="false"
                    :show-price="true"
                />
            </div>

            <div v-else class="mt-8 text-center text-muted-foreground">
                <p>No se encontraron cursos en este momento.</p>
            </div>
        </section>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useCatalogStore } from '@/store/catalog.store';
import Button from '@/components/ui/button/Button.vue'
import CourseCard from '@/components/shared/CourseCard.vue';

const catalogStore = useCatalogStore();

onMounted(() => {
    catalogStore.fetchCursos();
});
</script>