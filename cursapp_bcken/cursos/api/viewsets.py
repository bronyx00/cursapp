from rest_framework import viewsets, permissions, exceptions
from rest_framework.decorators import action
from django.db.models import Count
from cursos.models import Curso, Modulo, Leccion, Categoria
from .serializers import CursoListSerializer, CursoDetailSerializer, ModuloSerializer, LeccionSerializer, CategoriaSerializer
from evaluacion.models import InteraccionLeccion

# --- Permisos Personalizados ---
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso de alto nivel para todo el contenido de 'cursos'.
    - Permite lectura (GET) a todos.
    - Permite CREAR (POST) solo a Instructores.
    - Permite EDITAR/BORRAR (PUT/DELETE) solo al Instructor PROPIETARIO
    """
    def has_permission(self, request, view):
        # Permite lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Deniega escritura a usuarios no autenticados
        if not request.user.is_authenticated:
            return False
        
        # Permite CREAR solo si es Instructor
        return request.user.es_instructor
    
    def has_object_permission(self, request, view, obj):
        # Permite lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Deniega si no es instructor
        if not request.user.es_instructor:
            return False
        
        # Determinar el propietario
        owner = None
        if isinstance(obj, Curso):
            # Si el objeto es un Curso, el dueño es 'instructor'
            owner = obj.instructor
        elif isinstance(obj, Modulo):
            # Si el objeto es un Modulo, el dueño es 'curso.instructor'
            owner = obj.curso.instructor
        elif isinstance(obj, Leccion):
            # Si el objeto es una Leccion, el dueño es 'modulo.curso.instructor'
            owner = obj.modulo.curso.instructor
            
        # Permitir solo si el usuario es el propietario
        return owner == request.user
    
# --- ViewSets ---
class CursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar y recuperar cursos (Catálogo) y gestionarlos (CRUD).
    - El público general solo ve cursos PUBLICADOS.
    - El instructor propietario ve TODOS sus cursos (Borrador, Publicado, Suspendido).
    """
    queryset = Curso.objects.all().order_by('-fecha_creacion')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] # Lectura pública, escritura solo para Instructores.
    
    def get_serializer_class(self):
        """Alterna entre el serializer de listado y el de detalle."""
        if self.action == 'list':
            return CursoListSerializer
        return CursoDetailSerializer
        
    def get_queryset(self):
        """
        Filtra dinámicamente los cursos visibles basado en el rol del usuario.
        """
        user = self.request.user
        
        # Si el usuario no está autenticado O no es instructor
        if not user.is_authenticated or not user.es_instructor:
            # Mostrar solo cursos PUBLICADOS
            return self.queryset.filter(estado=Curso.ESTADO_PUBLICADO)
        
        # Si el usuario es instructor
        from django.db.models import Q
        
        return self.queryset.filter(
            Q(instructor=user) | Q(estado=Curso.ESTADO_PUBLICADO)
        ).distinct() # Para evitar duplicados si un curso es público y es mío
        
    def perform_create(self, serializer):
        # Asigna automáticamente al usuario logueado como el instructor del curso
        serializer.save(instructor=self.request.user)
        
        
class ModuloViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de Módulos."""
    serializer_class = ModuloSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
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
    permission_classes = [IsOwnerOrReadOnly]
    
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
    
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y recuperar Categorías. Solo lectura
    """
    queryset = Categoria.objects.annotate(num_cursos=Count('cursos')).order_by('nombre')
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny] # Público
