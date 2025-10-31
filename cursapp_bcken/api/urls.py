from django.urls import path, include

urlpatterns = [
    # Rutas de autenticación (login, logout, registro, perfiles)
    path('auth/', include('core.api.urls')),
    
    # Rutas del catálogo y gestión de (Cursos, Módulo, Lecciones)
    path('cursos/', include('cursos.api.urls')),
    
    # Rutas de evaluación progreso y matriculación (Inscripción, Exámenes, Certificados)
    path('evaluacion/', include('evaluacion.api.urls')),
]