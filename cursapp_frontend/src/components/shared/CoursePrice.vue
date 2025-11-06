<template>
  <div class="flex flex-col items-start leading-none">
    <span class_name="text-2xl font-bold text-foreground">
      ${{ precioUsd }}
    </span>
    
    <span v-if="precioVes" class="text-sm text-muted-foreground mt-1">
      (Bs. {{ formatoVes(precioVes) }})
    </span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  precioUsd: number | string;
  precioVes?: number | string | null;
}>();

// Helper simple para formatear el bolivar
const formatoVes = (valor: number | string) => {
  const num = Number(valor);
  return new Intl.NumberFormat('es-VE', {
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
};
</script>