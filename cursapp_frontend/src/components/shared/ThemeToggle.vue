<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" size="icon">
                <Sun class="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                <Moon class="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                <span class="sr-only">Toggle theme</span>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
            <DropdownMenuItem @click="setTheme('light')">
                <Sun class="mr-2 h-4 w-4" />
                <span>Claro</span>
            </DropdownMenuItem>
            <DropdownMenuItem @click="setTheme('dark')">
                <Moon class="mr-2 h-4 w-4" />
                <span>Oscuro</span>
            </DropdownMenuItem>
            <DropdownMenuItem @click="setTheme('auto')">
                <Laptop class="mr-2 h-4 w-4" />
                <span>Sistema</span>
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup lang="ts">
import { useColorMode, type BasicColorSchema } from '@vueuse/core' // Importar BasicColorSchema
import { Moon, Sun, Laptop } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const mode = useColorMode({
  selector: 'html',
  attribute: 'class',
  modes: {
    light: 'light',
    dark: 'dark',
  },
})

// CORRECCIÓN AQUÍ: El tipo debe ser BasicColorSchema
const setTheme = (theme: BasicColorSchema | 'auto') => {
  mode.value = theme
}
</script>