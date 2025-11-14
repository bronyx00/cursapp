<template>
  <Card class="bg-primary/5 text-primary-foreground border-primary/20">
    <CardHeader>
      <CardTitle class="text-2xl font-bold text-primary">
        Continuar Aprendiendo
      </CardTitle>
    </CardHeader>
    
    <CardContent v-if="learningStore.isLoadingReciente">
      <div class="h-8 w-3/4 animate-pulse rounded-md bg-muted"></div>
      <div class="mt-2 h-4 w-1/2 animate-pulse rounded-md bg-muted"></div>
    </CardContent>

    <template v-if="learningStore.cursoReciente">
      <CardContent class="pt-0">
        <h3 class="text-xl font-semibold text-foreground">
          {{ learningStore.cursoReciente.leccion.titulo }}
        </h3>
        <p class="text-muted-foreground">
          {{ learningStore.cursoReciente.curso.titulo }}
        </p>
      </CardContent>
      <CardFooter>
        <Button class="bg-primary hover:bg-primary/90" as-child>
          <RouterLink :to="`/aprender/${learningStore.cursoReciente.curso.slug}/leccion/${learningStore.cursoReciente.leccion.id}`">
            <Play class="mr-2 h-4 w-4" />
            Ir a la lección
          </RouterLink>
        </Button>
      </CardFooter>
    </template>

    <CardContent v-if="!learningStore.isLoadingReciente && !learningStore.cursoReciente">
      <p class="text-muted-foreground">
        ¡Empieza tu primera lección! Elige uno de tus cursos para comenzar.
      </p>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useLearningStore } from '@/store/learning.store';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RouterLink } from 'vue-router';
import { Play } from 'lucide-vue-next';

const learningStore = useLearningStore();
</script>