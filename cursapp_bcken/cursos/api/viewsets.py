from rest_framework import viewsets, permissions
from cursos.models import Curso, Modulo, Leccion
from .serializers import CursoListSerializer, CursoDetailSerializer, ModuloSerializer, LeccionSerializer

# --- Permisos Personalizados ---

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Permite GET (lectura) a todos, pero solo permite PUT/POST/DELETE
    si el usuario es Instructor (o Admin, ya que el admin es superusuario)
    """
    
    def has_permission(self, request, view):
        # Permite lectura (GET, HEAD, OPTIONS) a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        # Solo permite escritura si el usuario está autenticado y es instructor
        return request.user.is_autenticated and request.user.es_instructor
    
# --- ViewSets ---

class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar y recuperar cursos (Catálogo) y gestionarlos (CRUD)
    """
    queryset = Curso.objects.filter(estado=Curso.ESTADO_PUBLICADO).order_by('-fecha_creacion')
    permission_classes = [IsInstructorOrReadOnly] # Lectura pública, escritura solo para Instructores.
    
    def get_serializer_class(self):
        """Alterna entre el serializer de listado y el de detalle."""
        if self.action == 'list':
            return CursoListSerializer
        return CursoDetailSerializer
    
    # Sobreescribir el create/update para enlazar automáticamente al instructor
    def perform_create(self, serializer):
        # Asigna automáticamente al usuario logueado como el instructor del curso
        serializer.save(instructor=self.request.user)
        
    # Mejorar la queryset para que los profesores solo vean sus cursos cuando esta en ESTADO_BORRADOR
    # def get_queryset(self):
    #     if self.request.user.is_authenticated and self.request.user.es_profesor:
    #         return Curso.objects.filter(profesor=self.request.user).order_by('-fecha_creacion')
    #     return Curso.objects.filter(esta_publicado=True).order_by('-fecha_creacion')
        
class ModuloViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de Módulos."""
    serializer_class = ModuloSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    # Filtrar los módulos por el curso (se accede por /cursos/{curso_ud}/modulos)
    def get_queryset(self):
        curso_pk = self.kwargs.get('curso_pk') # Obtenido de las URLs anidadas
        if curso_pk:
            return Modulo.objects.filter(curso__pk=curso_pk).order_by('orden')
        return Modulo.objects.all().order_by('orden')
    
    # Lógica para crear un módulo asignándolo al curso correcto
    # def perform_create(self, serializer):
    #     # Lógica compleja de asignación a un curso existente
    #     pass
    
class LeccionViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de Lecciones."""
    serializer_class = LeccionSerializer
    permission_classes = [IsInstructorOrReadOnly]
    
    # Filtrar las lecciones por el módulo (se accede por /modulos/{modulo_id}/lecciones)
    def get_queryset(self):
        modulo_pk = self.kwargs.get('modulo_pk')
        if modulo_pk:
            return Leccion.objects.filter(modulo__pk=modulo_pk).order_by('orden')
        return Leccion.objects.all().order_by('orden')
    
    # Lógica para crear una lección asignándola al módulo correcto
    # def perform_create(self, serializer):
    #     # Lógica compleja de asignación a un módulo existente
    #     pass