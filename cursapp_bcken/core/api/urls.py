from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # Genera Access y Refresh Tokens (Login)
    TokenRefreshView, # Usa Refresh Token para obtener nuevo Access Token
    )
from .viewsets import RegistroUsuarioAPIView, PerfilUsuarioAPIView

urlpatterns = [
    # JWL (Login y Refresco de Token)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Registro Personalizado
    path('sign-up/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    
    # Perfil del Usuario
    path('perfil/', PerfilUsuarioAPIView.as_view(), name='perfil_usuario'),
]