<template>
  <div>
    <div class="mb-8 text-center md:text-left">
      <h1 class="text-3xl font-bold tracking-tight">Bienvenido de vuelta</h1>
      <p class="mt-2 text-muted-foreground">Ingresa tus credenciales para continuar.</p>
    </div>

    <form @submit.prevent="handleLogin" class="grid gap-6">
      <div class="grid gap-2">
        <Label for="username">Usuario</Label>
        <Input
          id="username"
          v-model="username"
          placeholder="Usuario"
          required
        />
      </div>
      <div class="grid gap-2">
        <div class="flex items-center justify-between">
          <Label for="password">Contraseña</Label>
          <a href="#" class="text-sm text-muted-foreground underline-offset-4 hover:text-primary hover:underline">
            ¿Olvidaste tu contraseña?
          </a>
        </div>
        <Input
          id="password"
          v-model="password"
          type="password"
          required
        />
      </div>
      
      <p v-if="errorMsg" class="text-sm text-destructive">{{ errorMsg }}</p>
      
      <Button type="submit" class="w-full" :disabled="isLoading">
        {{ isLoading ? 'Ingresando...' : 'Entrar' }}
      </Button>
    </form>

    <div class="mt-6 text-center text-sm text-muted-foreground">
      ¿No tienes una cuenta?
      <RouterLink to="/register" class="font-semibold text-primary underline-offset-4 hover:underline">
        Regístrate aquí
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label'; 

const username = ref('');
const password = ref('');
const errorMsg = ref<string | null>(null);
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  isLoading.value = true;
  errorMsg.value = null;
  try {
    await authStore.login({
      username: username.value,
      password: password.value,
    });

    if (authStore.esAlumno) {
      router.push({ name: 'MiAprendizaje' });
    } else if (authStore.esInstructor) {
      router.push({ name: 'InstructorDashboard' });
    } else {
      router.push({ name: 'Home' }); // Ajustar si tienes dashboard de instructor
    }
  } catch (error) {
    console.error(error);
    errorMsg.value = 'Usuario o contraseña incorrectos.';
  } finally {
    isLoading.value = false;
  }
};
</script>