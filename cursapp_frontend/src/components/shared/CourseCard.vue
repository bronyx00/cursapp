<template>
    <RouterLink :to="`/cursos/${curso.slug}`">
        <Card class="flex h-full flex-col overflow-hidden transition-all duration-200 ease-in-out hover:shadow-lg hover:shadow-primary/10">

            <CardHeader class="p-0">
                <div class="aspect-video w-full bg-secondary">
                    <img
                        v-if="curso.portada"
                        :src="curso.portada"
                        :alt="curso.titulo"
                        class="h-full w-full object-cover"
                    />
                </div>
            </CardHeader>

            <CardContent class="flex-1 p-4">
                <h3 class="font-semibold leading-tight text-foreground">
                    {{ curso.titulo }}
                </h3>
                <p class="mt-1 text-sm text-secondary-foreground/70">
                    {{ curso.instructor_nombre }}
                </p>
            </CardContent>

            <CardFooter class="flex flex-col items-start p-4 pt-0">
                <div class="mb-1 flex w-full justify-between text-xs text-secondary-foreground/70">
                    <span>Progreso</span>
                    <span>{{ Number(progreso).toFixed(0) }}</span>
                </div>
                <Progress
                    :model-value="Number(progreso)"
                    class="h-2 w-full"
                    indicator-class="bg-accent"
                />
            </CardFooter>
        </Card>
    </RouterLink>
</template>

<script setup lang="ts">
import type { CursoList } from '@/types/cursos.types';
import { RouterLink } from 'vue-router';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress';

defineProps<{
    curso: CursoList;
    progreso: string;
}>();

</script>