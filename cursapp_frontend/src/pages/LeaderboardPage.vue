<template>
    <div>
    <h1 class="text-2xl font-bold md:text-3xl">Clasificación General (XP)</h1>
    <p class="mt-2 text-secondary-foreground/70">
      Mira quiénes lideran la plataforma acumulando puntos de experiencia (XP).
    </p>

    <div v-if="gamificationStore.isLoading" class="mt-8 text-center">
      Cargando clasificación...
    </div>
    
    <div class="mt-8 grid gap-4 md:hidden">
      <Card v-for="(user, index) in gamificationStore.leaderboard" :key="user.id">
        <CardContent class="flex items-center gap-4 p-4">
          <span class="text-xl font-bold" :class="getRankColor(index + 1)">
            #{{ index + 1 }}
          </span>
          
          <Avatar class="h-10 w-10">
            <AvatarImage v-if="user.foto_perfil" :src="user.foto_perfil" :alt="user.username" />
            <AvatarFallback>
              {{ user.username.substring(0, 2).toUpperCase() }}
            </AvatarFallback>
          </Avatar>
          
          <div class="flex-1">
            <p class="font-medium">{{ user.full_name || user.username }}</p>
            <p class="text-sm text-secondary-foreground/70">{{ user.puntuacion_total }} XP</p>
          </div>
        </CardContent>
      </Card>
    </div>

    <Card class="mt-8 hidden md:block">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="w-[80px]">Posición</TableHead>
            <TableHead>Alumno</TableHead>
            <TableHead class="text-right">Puntuación (XP)</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow
            v-for="(user, index) in gamificationStore.leaderboard"
            :key="user.id"
          >
            <TableCell class="text-lg font-medium" :class="getRankColor(index + 1)">
              #{{ index + 1 }}
            </TableCell>
            <TableCell>
              <div class="flex items-center gap-3">
                <Avatar class="h-9 w-9">
                  <AvatarImage v-if="user.foto_perfil" :src="user.foto_perfil" :alt="user.username" />
                  <AvatarFallback>
                    {{ user.username.substring(0, 2).toUpperCase() }}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <div class="font-medium">{{ user.full_name || user.username }}</div>
                  <div class="text-sm text-secondary-foreground/70">@{{ user.username }}</div>
                </div>
              </div>
            </TableCell>
            <TableCell class="text-right text-lg font-medium text-accent">
              {{ user.puntuacion_total }} XP
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </Card>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useGamificationStore } from '@/store/gamification.store';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage} from '@/components/ui/avatar';
import {
    Table,
    TableBody,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';

const gamificationStore = useGamificationStore();

onMounted(() => {
    gamificationStore.fetchLeaderboard();
});

// Función de estilo para destacar el Top 3
const getRankColor = (rank: number) => {
  if (rank === 1) return 'text-amber-400'; // Oro
  if (rank === 2) return 'text-slate-400'; // Plata
  if (rank === 3) return 'text-amber-700'; // Bronce
  return 'text-secondary-foreground/70';
};
</script>