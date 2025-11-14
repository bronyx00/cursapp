import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth.store';

// Layouts
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import MarketingLayout from '@/layouts/MarketingLayout.vue';

// Todas las páginas
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import RegisterPage from '@/pages/RegisterPage.vue';
import AlumnoDashboard from '@/pages/AlumnoDashboard.vue';
import InstructorDashboard from '@/pages/InstructorDashboard.vue';
import LeaderboardPage from '@/pages/LeaderboardPage.vue';
import type { UserRole } from '@/types/user.types';
import AuthLayout from '@/layouts/AuthLayout.vue';


const routes = [
    // Rutas públicas 
    {
        path: '/',
        component: MarketingLayout,
        children: [
            { path: '/', name: 'Home', component: HomePage },
        ],
    },
    {
        path: '/',
        component: AuthLayout,
        children: [
            { path: '/login', name: 'Login', component: LoginPage },
            { path: '/register', name: 'Register', component: RegisterPage },
        ]
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
            {
                path: '/instructor/dashboard',
                name: 'InstructorDashboard',
                component: InstructorDashboard,
                meta: { roles: [2] } // Solo instructores
            }
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
    }
    
    if ((to.name === 'Login' || to.name === 'Home') && isAuthenticated) {
        // Redirige al dashboard correspondiente, una vez logueado
        if (userRole === 3) next({ name: 'MiAPrendizaje' });
        if (userRole === 2) next({ name: 'InstructorDashboard' });
        else next({ name: 'Home' }); // Fallback
    }

    const requiredRoles = to.meta.roles as UserRole[] | undefined;
    
    if (requiresAuth && requiredRoles && requiredRoles.length > 0) {
        if (!userRole || !requiredRoles.includes(userRole)) {
            // Si requiere un rol específico y el usuario no lo tiene
            return next({ name: 'Home' }); // Cambiar luego por una página no autorizada
        }
    }
    next();
});

export default router;