<template>
    <div class="w-full max-w-sm rounded-lg border bg-white p-8 shadow-md dark:border-slate-800 dark:bg-slate-900">
        <h1 class="mb-6 text-center text-2xl font-bold">Iniciar Sesión</h1>
        <form @submit.prevent="handleLogin">
            <div class="grid gap-4">
                <div class="grid gap-2">
                    <label for="username">Usuario</label>
                    <Input
                        id="username"
                        v-model="username"
                        placeholder="tu-usuario"
                        required
                    />
                </div>
                <div class="grid gap-2">
                    <label for="password">Contraseña</label>
                    <Input
                        id="password"
                        v-model="password"
                        type="password"
                        required
                    />
                </div>
                <p v-if="errorMsg" class="text-sm to-red-500">{{ errorMsg }}</p>
                <Button type="submit" class="w-full" :disabled="isLoading">
                    {{ isLoading ? 'Cargando...' : 'Entrar' }}
                </Button>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';
import Button from '@/components/ui/button/Button.vue';
import Input from '@/components/ui/input/Input.vue';

const username = ref('');
const password = ref('');
const errorMsg = ref<string | null>(null);
const isLoading = ref(false);

const authStore = useAuthStore()
const router = useRouter();

const handleLogin = async () => {
    isLoading.value = true;
    errorMsg.value = null;
    try {
        await authStore.login({
            username: username.value,
            password: password.value,
        });

        // Redireccion basada en el rol
        if (authStore.esAlumno) {
            router.push({ name: 'MiAprendizaje' });
        } else {
            // Redirigir a otro lado si no es alumno
            router.push({ name: 'Home' });
        }
    } catch (error) {
        console.error(error);
        errorMsg.value = 'Usuario o contraseña incorrectos.';
    } finally {
        isLoading.value = false;
    }
};

</script>