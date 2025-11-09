<template>
  <header class="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur-sm">
    <div class="container mx-auto grid h-16 grid-cols-3 items-center gap-4 md:flex md:justify-between">
      
      <div class="flex justify-start md:hidden">
        <Sheet v-model:open="isMobileMenuOpen">
          <SheetTrigger as-child>
            <Button variant="ghost" size="icon" class="shrink-0">
              <Menu class="h-5 w-5" />
              <span class="sr-only">Abrir menú</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" class="flex flex-col p-0">
            <MobileNavSheet @navigated="isMobileMenuOpen = false" />
          </SheetContent>
        </Sheet>
      </div>

      <div class="flex justify-center md:flex-1 md:justify-start">
        <RouterLink to="/" class="flex items-center gap-2">
          <span class="text-2xl font-bold tracking-tight">cursapp</span>
        </RouterLink>
      </div>

      <div class="flex items-center justify-end">
        <nav class="hidden items-center gap-2 md:flex">


          <Button variant="ghost" as-child>
            <RouterLink to="/planes">Planes y precios</RouterLink>
          </Button>
          <Button variant="ghost" as-child>
            <RouterLink to="/business">Cursapp Business</RouterLink>
          </Button>
          <Button variant="ghost" as-child>
            <RouterLink to="/instructores">Enseña en Cursapp</RouterLink>
          </Button>
          

          <Separator orientation="vertical" class="mx-2 h-6" />
          <Button variant="ghost" as-child>
            <RouterLink to="/login">Iniciar Sesión</RouterLink>
          </Button>
          <Button as-child>
            <RouterLink to="/register">Registrarse</RouterLink>
          </Button>
          <ThemeToggle />
        </nav>

        <div class="flex items-center gap-1 md:hidden">
          <Button variant="ghost" size="icon">
            <Search class="h-5 w-5" />
            <span class="sr-only">Buscar</span>
          </Button>
          <Button variant="ghost" size="icon">
            <ShoppingCart class="h-5 w-5" />
            <span class="sr-only">Carrito</span>
          </Button>
        </div>
      </div>

    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { Button } from '@/components/ui/button';
import ThemeToggle from '@/components/shared/ThemeToggle.vue';
import { Menu, Search, ShoppingCart } from 'lucide-vue-next';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import MobileNavSheet from './MobileNavSheet.vue';
// 1. Importar el nuevo componente Separator
import { Separator } from '@/components/ui/separator'; 

const isMobileMenuOpen = ref(false);
</script>