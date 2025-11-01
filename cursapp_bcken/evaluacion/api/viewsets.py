from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from evaluacion.models import Inscripcion, PuntosAlumno, ProgresoLeccion
from cursos.models import Curso, Leccion
from core.models import Usuario
from utils.monetizacion import obtener_tasa_bcv
from .serializers import (
    InscripcionSerializer, 
    InscripcionCrearSerializer, 
    LeaderboardSerializer,
    ScormProgresoSerializer
)

class InscripcionViewSet(viewsets.ModelViewSet):
    """
    Permite a los Alumnos inscribirse en cursos y ver su historial de inscripciones.
    Solo muestra las inscripciones Activas (Pagadas) o Pendientes.
    """
    queryset = Inscripcion.objects.all()
    # Solo usuarios autenticados pueden interactuar con sus inscripciones.
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InscripcionCrearSerializer
        return InscripcionSerializer
    
    def get_queryset(self):
        # Solo un alumno puede ver sus propias inscripciones.
        if self.request.user.is_authenticated and self.request.user.rol == self.request.user.ROL_ALUMNO:
            return Inscripcion.objects.filter(
                alumno=self.request.user,
                estado_pago__in=[Inscripcion.ESTADO_PAGADO, Inscripcion.ESTADO_PENDIENTE]
            ).order_by('-fecha_inscripcion')
        return Inscripcion.objects.none()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        curso_id = serializer.validated_data['curso'].id
        alumno = request.user
        
        # Verificación de preexistencia
        if Inscripcion.objects.filter(alumno=alumno, curso_id=curso_id, estado_pago=Inscripcion.ESTADO_PAGADO).exists():
            return Response(
                {"error": "Ya estás inscrito y tu curso está activo."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        curso = get_object_or_404(Curso, pk=curso_id, estado=Curso.ESTADO_PUBLICADO)
        
        # Creación de la Inscripción Pendiente
        inscripcion = Inscripcion.objects.create(
            alumno=alumno,
            curso=curso,
            precio_pagado_usd=curso.precio_usd,
            estado_pago=Inscripcion.ESTADO_PENDIENTE
        )
        
        # Obtener la tasa del BCV y preparar la respuesta de pago
        tasa_bcv = obtener_tasa_bcv()
        monto_ves = curso.precio_usd * tasa_bcv
        
        
        # Preparación para la Pasarela de Pago
        # Aquí se integraría la lógica para generar una URL de pago, o una factura.
        # Por ahora, devolvemos los datos para que el frontend inicie el proceso.
        
        response_serializer = InscripcionSerializer(inscripcion)
        return Response(
            {
                "mensaje": "Pre-inscripción creada. Continúe al pago.",
                "inscripcion": response_serializer.data,
                "datos_pago": {
                    "precio_usd": str(curso.precio_usd),
                    "tasa_bcv": str(tasa_bcv),
                    "monto_ves": str(round(monto_ves, 2)),
                    "metodos": ["Pago Movil", "Transferencia", "TDC/TDD"]
                }
            },
            status=status.HTTP_201_CREATED
        )
        
class LeaderboardAPIView(generics.ListAPIView):
    """
    API para la Tabla de Clasificación Global (Leaderboard).
    Muestra la puntuación total de los alumnos.
    """
    serializer_class = LeaderboardSerializer
    # Permitir que el Leaderboard sea visible públicamente para fomentar la competencia
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Ordena los usuarios por el campo 'xp_totales'
        # Esto siempre será instantaneo, incluso con miles de usuarios.
        return Usuario.objects.filter(
            rol=Usuario.ROL_ALUMNO,
            xp_totales__gt=0
        ).order_by('-xp_totales')
        
class ScormProgresoAPIView(generics.RetrieveUpdateAPIView):
    """
    API Endpoint para la comunicación SCORM (LMSInitialize y LMSCommit).
    
    - GET (LMSInitialize):
      Recupera el estado actual del progreso SCORM (suspend_data, estado, puntuacion).
      
    - PUT/PATCH (LMSCommit):
      Guarda (Commitea) el nuevo estado SCORM enviado desde el player de Vue.js.
    """
    serializer_class = ScormProgresoSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo alumnos autenticados
    lookup_field = 'leccion_pk' # Usaremos el ID del la lección desde la URL
    
    def get_object(self):
        # Identificar al usuario y la lección
        user = self.request.user
        leccion_id = self.kwargs.get('leccion_pk')
        leccion = get_object_or_404(Leccion, pk=leccion_id)
        
        # Validar Roles y Tipo de Contenido
        if not user.es_alumno:
            raise PermissionDenied("Solo los alumnos pueden reportar progreso SCORM.")
        
        if leccion.tipo_contenido != Leccion.TIPO_SCORM:
            raise PermissionDenied("Esta lección no es de tipo SCORM.")
        
        # Validar Inscripción
        # Asegura que el alumno esté inscrito y haya pagado el curso.
        try: 
            inscripcion = Inscripcion.objects.get(
                alumno=user,
                curso=leccion.modulo.curso,
                estado_pago=Inscripcion.ESTADO_PAGADO
            )
        except Inscripcion.DoesNotExist:
            raise PermissionDenied("No estás inscrito en este curso o tu pago aún está pendiente.")
        
        # Obtener (o Crear si es la primera vez) el registro de progreso
        # Esto permite que la primera llamada GET (LMSInitialize) funcione
        progreso, created = ProgresoLeccion.objects.get_or_create(
            inscripcion=inscripcion,
            leccion=leccion
        )
        
        if leccion:
            # Si es la primera vez, el punto de entrada es 'ab-initio' (desde el inicio)
            progreso.entry_point = 'ab-initio'
        else:
            # Si ya existía, el punto de entrada es 'resume' (continuar)
            progreso.entry_point = 'resume'
            
        return progreso