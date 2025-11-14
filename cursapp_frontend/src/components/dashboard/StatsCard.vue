<template>
  <Card>
    <CardHeader>
      <CardTitle class="text-xl">Mis Estadísticas</CardTitle>
    </CardHeader>
    <CardContent class="grid grid-cols-2 gap-6">
      <div class="flex items-center gap-3">
        <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-accent/10">
          <Trophy class="h-6 w-6 text-accent" />
        </div>
        <div>
          <p class="text-2xl font-bold">{{ authStore.user?.xp_totales || 0 }}</p>
          <p class="text-sm text-muted-foreground">XP Totales</p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
          <Database class="h-6 w-6 text-primary" />
        </div>
        <div>
          <p class="text-2xl font-bold">{{ authStore.user?.puntos_totales || 0 }}</p>
          <p class="text-sm text-muted-foreground">Puntos</p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <div class="flex h-12 w-12 items-center justify-center rounded-lg bg-emerald-500/10">
          <CheckCircle class="h-6 w-6 text-emerald-500" />
        </div>
        <div>
          <p class="text-2xl font-bold">{{ cursosCompletados }}</p>
          <p class="text-sm text-muted-foreground">Cursos Comp.</p>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from '@/store/auth.store';
import { useLearningStore } from '@/store/learning.store';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Trophy, Database, CheckCircle } from 'lucide-vue-next';

const authStore = useAuthStore();
const learningStore = useLearningStore();

const cursosCompletados = computed(() => {
  return learningStore.misCursos.filter(c => c.completado).length;
});
</script>