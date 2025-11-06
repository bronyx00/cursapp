<template>
  <RouterLink
    :to="`/categorias/${categoria.slug}`"
    class="group block h-96 w-full overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:shadow-xl"
  >
    <div class="relative h-full w-full">
      <img 
        :src="getCategoryImage(categoria.slug)" 
        :alt="categoria.nombre" 
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
      />
      
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
      
      <div class="absolute bottom-0 left-0 p-5 text-white">
        <h3 class="text-2xl font-semibold">{{ categoria.nombre }}</h3>
        <p class="mt-1 text-sm text-white/80 line-clamp-2">
          {{ categoria.descripcion || 'Explora esta categoría' }}
        </p>
        
        <div class="mt-4 inline-flex items-center gap-2 text-sm font-medium text-white transition-transform duration-300 group-hover:translate-x-1">
          Ver cursos
          <ArrowRight class="h-4 w-4" />
        </div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { ArrowRight } from 'lucide-vue-next';
import type { Categoria } from '@/types/cursos.types'; // Asumiendo que exportaste este tipo

defineProps<{
  categoria: Categoria;
}>();

// Misma función de placeholder de la respuesta anterior
const placeholderImages: Record<string, string> = {
  'desarrollo-web': 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-4.0.3&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=600&h=800',
  'desarrollo-movil': 'https://images.unsplash.com/photo-1607252650355-f7fd0460eeBF?ixlib=rb-4.0.3&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=600&h=800',
  'data-science': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=600&h=800',
  'default': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=600&h=800'
};

const getCategoryImage = (slug: string) => {
  return placeholderImages[slug] || placeholderImages.default;
};
</script>