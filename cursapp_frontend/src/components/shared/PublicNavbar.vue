<template>
  <header class="sticky top-0 z-40 w-full border-b bg-background/90 backdrop-blur-sm">
    <div class="container mx-auto px-8 flex h-14 items-center justify-between">
      
      <RouterLink to="/" class="flex items-center gap-2">
        <span class="text-3xl font-bold tracking-[.028em] text-primary">cursa<span class="text-accent">pp</span></span>
      </RouterLink>

      <nav class="flex items-center gap-2">
        <Button variant="ghost" as-child>
          <RouterLink to="/login">Iniciar Sesión</RouterLink>
        </Button>
        <Button as-child> <RouterLink to="/register">Registrarse</RouterLink>
        </Button>
        
        <ThemeToggle />
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Button } from '@/components/ui/button';
import ThemeToggle from '@/components/shared/ThemeToggle.vue'; // Importamos el toggle
</script>   