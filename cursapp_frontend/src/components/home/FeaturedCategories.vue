<template>
  <section class="mt-9 overflow-hidden px-4 py-16 md:py-24 bg-secondary/40">
    <div class="container mx-auto grid grid-cols-1 items-center gap-8 md:grid-cols-3 md:gap-16">
      
      <div class="max-w-xl md:col-span-1 text-center md:text-left">
        <h2 class="text-3xl font-bold tracking-tighter text-foreground md:text-4xl">
          Aprende habilidades esenciales
        </h2>
        <p class="mt-4 text-lg text-muted-foreground">
          Desarrolla rápidamente las habilidades demandadas para impulsar tu carrera profesional en el cambiante mercado laboral.
        </p>
      </div>

      <div class="w-full md:col-span-2">
        <ul
          ref="scrollContainerRef"
          class="flex snap-x snap-mandatory gap-6 overflow-x-auto pb-6"
        >
          <template v-if="catalogStore.isLoading">
            <li v-for="i in 3" :key="i" class="w-3/4 flex-shrink-0 snap-start md:w-[calc((100%-48px)/3)]">
              <div class="h-96 w-full animate-pulse rounded-lg bg-muted"></div>
            </li>
          </template>
          
          <template v-else>
            <li
              v-for="cat in catalogStore.categorias"
              :key="cat.id"
              class="w-3/4 flex-shrink-0 snap-start md:w-[calc((100%-48px)/3)]"
            >
              <VerticalCategoryCard :categoria="cat" />
            </li>
          </template>
        </ul>
      </div>
    </div>

    <div class="hidden md:flex justify-center mt-8 gap-3">
      <Button 
        @click="scrollPrev" 
        variant="outline" 
        size="icon" 
        :disabled="arrivedState.left"
        class="hover:bg-accent hover:text-accent-foreground"
      >
        <ChevronLeft class="h-5 w-5" />
        <span class="sr-only">Anterior</span>
      </Button>
      <Button 
        @click="scrollNext" 
        variant="outline" 
        size="icon" 
        :disabled="arrivedState.right"
        class="hover:bg-accent hover:text-accent-foreground"
      >
        <ChevronRight class="h-5 w-5" />
        <span class="sr-only">Siguiente</span>
      </Button>
    </div>

  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import { useScroll } from '@vueuse/core';
import { useCatalogStore } from '@/store/catalog.store';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-vue-next';
import VerticalCategoryCard from './VerticalCategoryCard.vue'; 

const catalogStore = useCatalogStore();
const scrollContainerRef = ref<HTMLElement | null>(null);

const { arrivedState, measure } = useScroll(scrollContainerRef, {
  offset: { left: 10, right: 10 } 
});

const scrollNext = () => {
  if (!scrollContainerRef.value) return;
  const scrollAmount = scrollContainerRef.value.clientWidth + 24;
  
  scrollContainerRef.value.scrollBy({ 
    left: scrollAmount, 
    behavior: 'smooth'
  });
};

const scrollPrev = () => {
  if (!scrollContainerRef.value) return;
  const scrollAmount = scrollContainerRef.value.clientWidth + 24;
  
  scrollContainerRef.value.scrollBy({ 
    left: -scrollAmount, 
    behavior: 'smooth'
  });
};

onMounted(() => {
  catalogStore.fetchCategorias();
});

// // Observamos cuando 'isLoading' cambia (especialmente de true a false)
watch(() => catalogStore.isLoading, (isLoading) => {
  if (isLoading === false) {
    // Esperamos a que Vue renderice el 'v-else'
    nextTick(() => {
      // Forzamos a useScroll a "volver a medir" el contenedor,
      // que ahora SÍ tiene las tarjetas.
      measure();
    });
  }
});
</script>

<style scoped>
/* Ocultar la barra de scroll */
.overflow-x-auto {
  scrollbar-width: none; /* Firefox */
}
.overflow-x-auto::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
</style>