<template>
    <div>
        <h1 class="text-2xl font-bold md:text-3xl">Mi Aprendizaje</h1>

        <div v-if="learningStore.isLoading" class="mt-8 text-center text-secondary-foreground/70">
            <p>Cargando tus cursos...</p>
        </div>

        <div
            v-else-if="learningStore.misCursos.length > 0"
            class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
            <CourseCard
                v-for="item in learningStore.misCursos"
                :key="item.id"
                :curso="item.curso"
                :progreso="item.porcentaje_progreso"
            />
        </div>

        <div v-else class="mt-8 rounded-lg border border-dashed border-border p-12 text-center text-secondary-foreground/70">
            <h3 class="text-lg font-medium">Aún no te has inscrito</h3>
            <p class="mt-2 text-sm">
                Parece que no tienes cursos activos. ¡Explora nuestro catálogo para empezar a aprender!
            </p>
            <Button variant="outline" class="mt-4">
                <RouterLink to="/">Explorar Cursos</RouterLink>
            </Button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useLearningStore } from '@/store/learning.store';
import CourseCard from '@/components/shared/CourseCard.vue';
import Button from '@/components/ui/button/Button.vue';
import { RouterLink } from 'vue-router';

const learningStore = useLearningStore();

onMounted(() => {
    learningStore.fetchMisCursos();
});
</script>