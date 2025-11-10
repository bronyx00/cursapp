<template>
  <div class="flex min-h-screen w-full items-center justify-center bg-background">
    <div class="relative grid h-screen w-full grid-cols-1 md:grid-cols-2">

      <div class="relative hidden h-full flex-col bg-muted p-10 text-white md:flex">
        <div class="absolute inset-0 bg-accent" />
        
        <RouterLink to="/" class="relative z-20 flex items-center text-lg font-medium text-accent-foreground">
          cursapp
        </RouterLink>

        <div class="relative z-20 mt-auto">
          <blockquote class="space-y-2">
            <p class="text-lg text-accent-foreground/80">
              "Esta plataforma cambió por completo mi carrera. Pasé de cero a mi primer
              trabajo como desarrollador en 6 meses."
            </p>
            <footer class="text-sm font-medium text-accent-foreground">Ana Pérez, Dev. Frontend</footer>
          </blockquote>
        </div>
      </div>

      <div class="relative flex h-full items-center justify-center p-8">
        <Button as-child variant="ghost" class="absolute top-4 left-4 md:hidden">
          <RouterLink to="/">
            <ChevronLeft class="mr-2 h-4 w-4" />
            Inicio
          </RouterLink>
        </Button>

        <div class="w-full max-w-sm">
          <RouterView />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { Button } from '@/components/ui/button';
import { ChevronLeft } from 'lucide-vue-next';
</script>