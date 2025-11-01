from django.urls import path
from .viewsets import RecomendacionAPIView

urlpatterns = [
    # Ruta final: /api/v1/recomendacion/cursos/
    path('cursos/', RecomendacionAPIView.as_view(), name='recomendar-cursos'),
]