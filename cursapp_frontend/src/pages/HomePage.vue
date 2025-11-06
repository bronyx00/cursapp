<template>
  <div class="bg-background text-foreground">
    
    <section class="relative container mx-auto flex min-h-[calc(100vh-4rem)] items-center overflow-hidden px-4 py-24 md:min-h-0 md:py-40 ">

      <div class="relative z-10 mx-auto max-w-3xl text-center">
        <span class="text-base font-semibold text-muted-foreground">
          Donde el aprendizaje se vuelve tangible.
        </span>
        
        <h1 class="mt-4 font-bold tracking-tighter text-accent"
            style="font-size: clamp(3.5rem, 10vw, 6rem); line-height: 1.1;">
          MÁS QUE CURSOS,
          <br />
          <span class="inline-block px-4 text-primary-foreground bg-primary -rotate-1">
            RESULTADOS
          </span>
        </h1>
        
        <p class="mt-8 text-lg text-muted-foreground md:text-xl max-w-xl mx-auto">
          Programas prácticos diseñados para crear. El único lugar donde cada lección termina en un proyecto real.
        </p>

        <div class="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Button size="lg" class="w-full sm:w-auto" as-child>
            <RouterLink to="/register?rol=alumno">Soy Alumno</RouterLink>
          </Button>
          <Button size="lg" variant="outline" class="w-full sm:w-auto" as-child>
            <RouterLink to="/register?rol=instructor">Soy Instructor</RouterLink>
          </Button>
        </div>
      </div>
    </section>

    <FeaturedCategories />

    <section class="bg-secondary/40 py-16 md:py-24">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
          Cursos Populares
        </h2>

        <div v-if="catalogStore.isLoading" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <CourseCardSkeleton v-for="i in 4" :key="i" />
        </div>

        <div v-else-if="catalogStore.cursos.length > 0" class="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <CourseCard
            v-for="curso in catalogStore.cursos"
            :key="curso.id"
            :curso="curso"
            :progreso="'0'" 
            :show-progress="false"
            :show-price="true"
          />
        </div>

        <div v-else class="mt-10 text-center text-muted-foreground">
          <p>No se encontraron cursos en este momento.</p>
        </div>
      </div>
    </section>

    <section class="container mx-auto px-4 py-24 md:py-32">
      <div class="mx-auto max-w-3xl text-center">
        <h2 class="text-4xl font-bold tracking-tighter text-foreground md:text-5xl">
          Conviértete en Instructor
        </h2>
        <p class="mt-6 text-lg text-muted-foreground md:text-xl">
          Comparte tu conocimiento con miles de estudiantes y genera ingresos. Te proveemos las herramientas para crear cursos de clase mundial.
        </p>
        <Button size="lg" class="mt-10">
          Empieza a enseñar hoy
        </Button>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router'; 
import { useCatalogStore } from '@/store/catalog.store';
import Button from '@/components/ui/button/Button.vue'
import CourseCard from '@/components/shared/CourseCard.vue';
import FeaturedCategories from '@/components/home/FeaturedCategories.vue';
import CourseCardSkeleton from '@/components/shared/CourseCardSkeleton.vue';
import { Hand, ThumbsUp } from 'lucide-vue-next'; 

const catalogStore = useCatalogStore();

onMounted(() => {
    catalogStore.fetchCursos();
});
</script>