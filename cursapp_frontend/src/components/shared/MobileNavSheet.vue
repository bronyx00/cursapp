<template>
  <div class="flex h-full flex-col">
    <div class="p-4" v-if="!authStore.isAuthenticated">
      <Button as-child class="w-full">
        <RouterLink to="/login" @click="emit('navigated')">Iniciar Sesión</RouterLink>
      </Button>
      <Button variant="outline" as-child class="mt-3 w-full">
        <RouterLink to="/register" @click="emit('navigated')">Registrarse</RouterLink>
      </Button>
    </div>

    <nav class="flex flex-col gap-1 p-4">
      <h3 class="px-3 text-sm font-semibold text-muted-foreground">Navegación</h3>
      <RouterLink
        to="/"
        @click="emit('navigated')"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-base font-medium transition-all hover:bg-accent"
      >
        <Home class="h-5 w-5" />
        Inicio
      </RouterLink>
      <RouterLink
        vS-if="authStore.esAlumno"
        to="/mi-aprendizaje"
        @click="emit('navigated')"
        class="flex items-center gap-3 rounded-lg px-3 py-2 text-base font-medium transition-all hover:bg-accent"
      >
        <LayoutDashboard class="h-5 w-5" />
        Mi Aprendizaje
      </RouterLink>
    </nav>

    <div class="flex-1 overflow-y-auto">
      <nav class="flex flex-col gap-1 p-4 pt-0">
        <h3 class="px-3 text-sm font-semibold text-muted-foreground">Categorías</h3>
        
        <div v-if="categoryStore.isLoading" class="px-3">
          <div v-for="i in 6" :key="i" class="mt-3 h-6 w-3/4 animate-pulse rounded-md bg-muted"></div>
        </div>

        <RouterLink
          v-for="cat in categoryStore.categorias"
          :key="cat.id"
          :to="`/categorias/${cat.slug}`"
          @click="emit('navigated')"
          class="flex items-center justify-between rounded-lg px-3 py-2 text-base font-medium transition-all hover:bg-accent"
        >
          <span>{{ cat.nombre }}</span>
          <ChevronRight class="h-5 w-5 text-muted-foreground" />
        </RouterLink>
      </nav>
    </div>

    <div class="mt-auto border-t p-4">
      <ThemeToggle />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';
import { useCatalogStore } from '@/store/catalog.store';
import { Button } from '@/components/ui/button';
import ThemeToggle from '@/components/shared/ThemeToggle.vue';
import { Home, LayoutDashboard, ChevronRight } from 'lucide-vue-next';

const authStore = useAuthStore();
const categoryStore = useCatalogStore();

const emit = defineEmits(['navigated']);

onMounted(() => {
  categoryStore.fetchCategorias();
});
</script>