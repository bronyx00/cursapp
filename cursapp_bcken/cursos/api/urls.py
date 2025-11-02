from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .viewsets import CursoViewSet, ModuloViewSet, LeccionViewSet
from evaluacion.api.viewsets import ResenaViewSet

# Router Principal para el Curso
router = DefaultRouter()
router.register(r'catalogo', CursoViewSet, basename='curso-catalogo')

# Router Anidado para Módulos (curso/{pk}/modulos/)
cursos_router = routers.NestedSimpleRouter(router, r'catalogo', lookup='curso')
cursos_router.register(r'modulos', ModuloViewSet, basename='curso-modulos')

# Router Anidado para Lecciones (curso/1/modulos/2/lecciones/)
modulos_router = routers.NestedSimpleRouter(cursos_router, r'modulos', lookup='modulo')
modulos_router.register(r'lecciones', LeccionViewSet, basename='modulo-lecciones')

# Router Anidado para Reseñas (cursos/{curso_pk}/resenas/)
resenas_router = routers.NestedSimpleRouter(router, r'catalogo', lookup='curso')
resenas_router.register(r'resenas', ResenaViewSet, basename='curso-resenas')

urlpatterns = router.urls + cursos_router.urls + modulos_router.urls + resenas_router.urls