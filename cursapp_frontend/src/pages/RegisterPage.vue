<template>
  <div>
    <div class="mb-8 text-center md:text-left">
      <h1 class="text-3xl font-bold tracking-tight">Crea tu cuenta</h1>
      <p class="mt-2 text-muted-foreground">Completa el formulario para empezar.</p>
    </div>

    <form @submit.prevent="handleRegister" class="grid gap-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="grid gap-2">
          <Label for="first_name">Nombre</Label>
          <Input id="first_name" v-model="formData.first_name" required />
        </div>
        <div class="grid gap-2">
          <Label for="last_name">Apellido</Label>
          <Input id="last_name" v-model="formData.last_name" required />
        </div>
      </div>

      <div class="grid gap-2">
        <Label for="username">Usuario</Label>
        <Input id="username" v-model="formData.username" required />
      </div>

      <div class="grid gap-2">
        <Label for="email">Email</Label>
        <Input id="email" v-model="formData.email" type="email" required />
      </div>

      <div class="grid gap-2">
        <Label for="password">Contraseña</Label>
        <Input id="password" v-model="formData.password" type="password" required />
      </div>

      <div class="grid gap-3">
        <Label>Quiero registrarme como:</Label>
        <RadioGroup v-model="formData.rol" default-value="3" class="flex gap-4">
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="rol-alumno" value="3" />
            <Label for="rol-alumno" class="font-normal">Alumno</Label>
          </div>
          <div class="flex items-center space-x-2">
            <RadioGroupItem id="rol-instructor" value="2" />
            <Label for="rol-instructor" class="font-normal">Instructor</Label>
          </div>
        </RadioGroup>
      </div>

      <p v-if="errorMsg" class="text-sm text-destructive">{{ errorMsg }}</p>
      
      <Button type="submit" class="w-full" :disabled="isLoading">
        {{ isLoading ? 'Creando cuenta...' : 'Crear cuenta' }}
      </Button>
    </form>

    <div class="mt-6 text-center text-sm text-muted-foreground">
      ¿Ya tienes una cuenta?
      <RouterLink to="/login" class="font-semibold text-primary underline-offset-4 hover:underline">
        Inicia sesión
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
// Asumo que tienes 'RadioGroup' (npx shadcn-vue@latest add radio-group)
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';

const formData = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password: '',
  rol: 3, // Por defecto Alumno (3)
});

const errorMsg = ref<string | null>(null);
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  isLoading.value = true;
  errorMsg.value = null;
  try {
    // Necesitaremos crear esta acción en el store
    await authStore.register(formData); 
    
    // Si el registro fue exitoso, loguear al usuario
    await authStore.login({
      username: formData.username,
      password: formData.password
    });

    if (authStore.esAlumno) {
      router.push({ name: 'MiAprendizaje' });
    } else {
      router.push({ name: 'Home' }); // Ajustar si tienes dashboard de instructor
    }
  } catch (error: any) {
    console.error(error);
    if (error.response?.data) {
      // Captura errores de validación del backend (DRF)
      const errors = error.response.data;
      if (errors.username) errorMsg.value = `Usuario: ${errors.username[0]}`;
      else if (errors.email) errorMsg.value = `Email: ${errors.email[0]}`;
      else errorMsg.value = 'Ocurrió un error. Verifica tus datos.';
    } else {
      errorMsg.value = 'No se pudo conectar al servidor.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>