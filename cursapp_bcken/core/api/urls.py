from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, # Usa Refresh Token para obtener nuevo Access Token
    )
from .viewsets import RegistroUsuarioAPIView, PerfilUsuarioAPIView, MyTokenObtainPairView

urlpatterns = [
    # JWL (Login y Refresco de Token)
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registro Personalizado
    path('sign-up/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    
    # Perfil del Usuario
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil_usuario'),
]