import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth.store';

// Layouts
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import MarketingLayout from '@/layouts/MarketingLayout.vue';

// Todas las páginas
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import AlumnoDashboard from '@/pages/AlumnoDashboard.vue';
import LeaderboardPage from '@/pages/LeaderboardPage.vue';

const routes = [
    // Rutas públicas 
    {
        path: '/',
        component: MarketingLayout,
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
            {
                path: '/leaderboard',
                name: 'Leaderboard',
                component: LeaderboardPage,
                meta: { roles: [3] }
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

    // Aseguramos de que el store se inicialice
    if (!authStore.user && authStore.accessToken) {
        try {
            await authStore.fetchProfile();
        } catch (e) {
            // Token inválido, limpiar
            authStore.logout();
        }
    }

    const isAuthenticated = authStore.isAuthenticated;
    const userRole = authStore.user?.rol;

    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    
    if (requiresAuth && !isAuthenticated) {
        // Si requiere autenticación y no la tiene, va al login
        next({ name: 'Login' });
    } else if ((to.name === 'Login' || to.name === 'Home') && isAuthenticated) {
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