<template>
  <div>
    <h2 class="text-2xl font-bold tracking-tight text-foreground">
      Mi Aprendizaje
    </h2>

    <Tabs default-value="en-progreso" class="w-full mt-4">
      <TabsList class="grid w-full grid-cols-2">
        <TabsTrigger value="en-progreso">En Progreso</TabsTrigger>
        <TabsTrigger value="completados">Completados</TabsTrigger>
      </TabsList>
      
      <TabsContent value="en-progreso">
        <div v-if="learningStore.isLoading" class="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          <CourseCardSkeleton />
          <CourseCardSkeleton />
        </div>
        <div v-else-if="cursosEnProgreso.length > 0" class="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          <CourseCard
            v-for="item in cursosEnProgreso"
            :key="item.id"
            :curso="item.curso"
            :progreso="item.porcentaje_progreso"
            :show-progress="true"
          />
        </div>
        <div v-else class="mt-8 flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-card p-12 text-center">
          <h3 class="text-lg font-medium text-foreground">No tienes cursos en progreso</h3>
          <p class="mt-2 text-sm text-muted-foreground">
            Parece que ya completaste todo. ¡Explora el catálogo para un nuevo reto!
          </p>
          <Button variant="outline" class="mt-4" as-child>
            <RouterLink to="/">Explorar Cursos</RouterLink>
          </Button>
        </div>
      </TabsContent>

      <TabsContent value="completados">
        <div v-if="learningStore.isLoading" class="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          <CourseCardSkeleton />
        </div>
        <div v-else-if="cursosCompletados.length > 0" class="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
          <CourseCard
            v-for="item in cursosCompletados"
            :key="item.id"
            :curso="item.curso"
            :progreso="item.porcentaje_progreso"
            :show-progress="true"
          />
        </div>
        <div v-else class="mt-8 flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-border bg-card p-12 text-center">
          <h3 class="text-lg font-medium text-foreground">Aún no has completado cursos</h3>
          <p class="mt-2 text-sm text-muted-foreground">
            ¡Termina tu primer curso para verlo aquí!
          </p>
        </div>
      </TabsContent>
    </Tabs>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useLearningStore } from '@/store/learning.store';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import CourseCard from '@/components/shared/CourseCard.vue';
import CourseCardSkeleton from '@/components/shared/CourseCardSkeleton.vue';
import { Button } from '@/components/ui/button';
import { RouterLink } from 'vue-router';

const learningStore = useLearningStore();

const cursosEnProgreso = computed(() => {
  return learningStore.misCursos.filter(c => !c.completado);
});
const cursosCompletados = computed(() => {
  return learningStore.misCursos.filter(c => c.completado);
});
</script>