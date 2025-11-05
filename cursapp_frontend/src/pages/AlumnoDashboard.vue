<template>
  <div>
    <h1 class="text-3xl font-bold tracking-tight text-foreground md:text-4xl">
      Mi Aprendizaje
    </h1>

    <div v-if="learningStore.isLoading" class="mt-8 text-center text-muted-foreground">
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

    <div v-else class="mt-8 flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-card p-12 text-center">
      <h3 class="text-lg font-medium text-foreground">Aún no te has inscrito</h3>
      <p class="mt-2 text-sm text-muted-foreground">
        Parece que no tienes cursos activos. ¡Explora el catálogo para empezar!
      </p>
      <Button variant="outline" class="mt-4" as-child>
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
  // El store ya previene la recarga, esto es seguro
  learningStore.fetchMisCursos();
});
</script>