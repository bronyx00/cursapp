<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-xl">Recomendado para ti</CardTitle>
    </CardHeader>
    <CardContent class="flex flex-col gap-4">
      <div v-if="recommendationStore.isLoading" class="flex flex-col gap-4">
        <div v-for="i in 2" :key="i" class="flex items-center gap-3">
          <div class="h-16 w-16 flex-shrink-0 rounded-lg bg-muted animate-pulse"></div>
          <div class="flex-1">
            <div class="h-4 w-full rounded-md bg-muted"></div>
            <div class="mt-2 h-4 w-1/2 rounded-md bg-muted"></div>
          </div>
        </div>
      </div>

      <div 
        v-for="curso in recommendationStore.cursosRecomendados.slice(0, 3)" 
        :key="curso.id" 
        class="flex items-center gap-3"
      >
        <img 
          v-if="curso.portada" 
          :src="curso.portada" 
          :alt="curso.titulo"
          class="h-16 w-16 flex-shrink-0 rounded-lg object-cover"
        />
        <div v-else class="flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-lg bg-muted">
          <BookMarked class="h-6 w-6 text-muted-foreground" />
        </div>
        <div class="flex-1">
          <RouterLink :to="`/cursos/${curso.slug}`" class="font-semibold leading-tight line-clamp-2 hover:underline">
            {{ curso.titulo }}
          </RouterLink>
          <p class="text-sm text-muted-foreground">{{ curso.instructor_nombre }}</p>
        </div>
      </div>

      <div v-if="!recommendationStore.isLoading && recommendationStore.cursosRecomendados.length === 0" class="text-sm text-muted-foreground">
        Aún no tenemos recomendaciones. ¡Sigue aprendiendo!
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useRecommendationStore } from '@/store/recommendation.store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BookMarked } from 'lucide-vue-next';
import { RouterLink } from 'vue-router';

const recommendationStore = useRecommendationStore();
</script>