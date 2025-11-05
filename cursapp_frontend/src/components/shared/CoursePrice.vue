<template>
  <div class="flex flex-col items-start leading-none">
    <span class_name="text-2xl font-bold text-foreground">
      ${{ precioUsd }}
    </span>
    
    <span v-if="precioVes" class="text-sm text-muted-foreground mt-1">
      ({{ formatoVes(precioVes) }})
    </span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  precioUsd: number | string;
  precioVes?: number | string | null;
}>();

// Un helper simple para formatear la moneda local
const formatoVes = (valor: number | string) => {
  const num = Number(valor);
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'VES',
    minimumFractionDigits: 2,
  }).format(num);
};
</script>