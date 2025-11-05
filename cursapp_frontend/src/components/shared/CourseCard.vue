<template>
  <RouterLink :to="`/cursos/${curso.slug}`" class="group block h-full rounded-xl overflow-hidden shadow-sm border border-border bg-card transition-all duration-300 hover:shadow-lg hover:border-primary/50">
    <Card class="flex h-full flex-col p-0 border-0 shadow-none rounded-none">
      
      <CardHeader class="p-0">
        <div class="aspect-video w-full overflow-hidden">
          <img
            v-if="curso.portada"
            :src="curso.portada"
            :alt="curso.titulo"
            class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div v-else class="h-full w-full bg-secondary flex items-center justify-center">
             <BookMarked class="h-12 w-12 text-muted-foreground/50" />
          </div>
        </div>
      </CardHeader>

      <CardContent class="p-4 flex-1">
        <h3 class="font-semibold text-lg leading-tight text-foreground line-clamp-1">
          {{ curso.titulo }}
        </h3>
        <p class="mt-1 text-sm text-muted-foreground line-clamp-1">
          {{ curso.instructor_nombre }}
        </p>

        <p class="mt-3 text-sm text-muted-foreground/80 line-clamp-4">
          {{ curso.descripcion }}
        </p>
        </CardContent>

      <CardFooter class="p-4 pt-0">
        <div v-if="showProgress" class="w-full">
          <div class="mb-0 flex w-full justify-between text-xs text-muted-foreground">
            <span>Progreso</span>
            <span>{{ Number(progreso).toFixed(0) }}%</span>
          </div>
          <Progress
            :model-value="Number(progreso)"
            class="h-2 w-full"
          />
        </div>

        <div v-else-if="showPrice" class="w-full">
          <CoursePrice
            :precio-usd="curso.precio_usd"
            :precio-ves="curso.precio_ves"
          />
        </div>
      </CardFooter>
    </Card>
  </RouterLink>
</template>

<script setup lang="ts">
import type { CursoList } from '@/types/cursos.types';
import { RouterLink } from 'vue-router';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { BookMarked } from 'lucide-vue-next';
import CoursePrice from './CoursePrice.vue';

defineProps<{
    curso: CursoList;
    progreso: string | string;
    showProgress?: boolean;
    showPrice?: boolean;
}>();
</script>