from rest_framework import generics, permissions
from rest_framework.response import Response
from core.models import Usuario
from .serializers import RegistroUsuarioSerializer, PerfilUsuarioSerializer

class RegistroUsuarioAPIView(generics.CreateAPIView):
    """
    Endpoint para el registro de nuevos usuarios (Alumno o Instructor).
    Permite el registro sin autenticación.
    """
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [permissions.AllowAny] # Permitir a cualquiera registrarse
    
class PerfilUsuarioAPIView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para ver y actualizar el perfil del usuario autenticado.
    """
    serializer_class = PerfilUsuarioSerializer
    # Solo usuarios autenticados pueden ver o editar su perfil.
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Devuelve el objeto Usuario del usuario autenticado."""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """Permite a los usuarios ver su propio perfil."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)