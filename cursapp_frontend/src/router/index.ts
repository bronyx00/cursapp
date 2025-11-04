import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth.store';

// Todas las páginas
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import AlumnoDashboard from '@/pages/AlumnoDashboard.vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';

const routes = [
    // Rutas públicas 
    {
        path: '/',
        component: AuthLayout,
        children: [
            { path: '/', name: 'Home', component: HomePage },
            { path: '/login', name: 'Login', component: LoginPage },
        ],
    },

    // Rutas privadas (Dashboards)
    {
        path: '/',
        component: DashboardLayout,
        meta: { requiresAuth: true }, // Para proteger todas las rutas anidadas
        children: [
            {
                path: '/mi-aprendizaje',
                name: 'MiAprendizaje',
                component: AlumnoDashboard,
                meta: { roles: [3] } // Solo alumnos
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation Guard (Seguridad de Rutas)
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.isAuthenticated;

    // Intenta cargar el perfil si hay un token pero no hay usuario
    if (authStore.accessToken && !authStore.user) {
        await authStore.fetchProfile();
    }

    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const userRole = authStore.user?.rol;

    if (requiresAuth && !isAuthenticated) {
        // Si requiere autenticación y no la tiene, va al login
        next({ name: 'Login' });
    } else if (to.name === 'Login' && isAuthenticated) {
        // Redirige al dashboard correspondiente, una vez logueado
        if (userRole === 3) next({ name: 'MiAPrendizaje' });
        // if (userRole === 2) next({ name: 'InstructorDashboard' });
        else next({ name: 'Home' }); // Fallback
    } else if (requiresAuth && to.meta.roles && !to.meta.roles.includes(userRole)) {
        // Si requiere un rol específico y el usuario no lo tiene
        next({ name: 'Home' }); // Cambiar luego por una página no autorizada
    } else {
        // Todo bien
        next();
    }
});

export default router;