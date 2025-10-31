from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import InscripcionViewSet, LeaderboardAPIView

router = DefaultRouter()
# Usaremos 'matricula' para la ruta
router.register(r'matricula', InscripcionViewSet, basename='matricula')

urlpatterns = router.urls + [
    # Ruta para la tabla de Clasificación
    path('leaderboard/', LeaderboardAPIView.as_view(), name='leaderboard'),
]