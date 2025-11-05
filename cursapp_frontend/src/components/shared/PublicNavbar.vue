<template>
  <header class="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur-sm">
    <div class="container flex h-16 items-center justify-between">
      
      <RouterLink to="/" class="flex items-center gap-2">
        <BookMarked class="h-6 w-6 text-primary" /> <span class="text-lg font-semibold">CursApp</span>
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
import { BookMarked } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';
import ThemeToggle from '@/components/shared/ThemeToggle.vue'; // Importamos el toggle
</script>