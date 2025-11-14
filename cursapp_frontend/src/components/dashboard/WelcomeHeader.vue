<template>
  <div>
    <h1 class="text-3xl font-bold tracking-tight text-foreground md:text-4xl">
      Bienvenido, {{ authStore.user?.first_name || authStore.user?.username }}
    </h1>
    <p class="mt-2 text-lg text-muted-foreground">
      Sigamos aprendiendo. Aquí tienes un resumen de tu actividad.
    </p>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/auth.store';
const authStore = useAuthStore();
</script>