<template>
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
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Button } from '@/components/ui/button';
</script>