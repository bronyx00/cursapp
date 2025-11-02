from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import InscripcionViewSet, LeaderboardAPIView, ScormProgresoAPIView, InstructorDashboardAPIView

router = DefaultRouter()
# Usaremos 'matricula' para la ruta
router.register(r'matricula', InscripcionViewSet, basename='matricula')

urlpatterns = router.urls + [
    # Ruta para la tabla de Clasificación
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
    
    # Endpoint para SCORM: api/v1/evaluacion/scorm/commit/<id_de_leccion>/
    path('scorm/commit/<int:leccion_pk>/', ScormProgresoAPIView.as_view(), name='scorm-commit'),
    
    # Endpoint para el Dashboard del Instructor
    path('instructor/dashboard/', InstructorDashboardAPIView.as_view(), name='instructor-dashboard'),
]