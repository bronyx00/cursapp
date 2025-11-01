from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from evaluacion.models import Inscripcion, PuntosAlumno
from cursos.models import Curso
from utils.monetizacion import obtener_tasa_bcv
from .serializers import InscripcionSerializer, InscripcionCrearSerializer, LeaderboardSerializer

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
        # Agrupa por alumno y suma los puntos
        leaderboard = PuntosAlumno.objects.values(
            'alumno',
            'alumno__username',
            'alumno__first_name',
            'alumno__last_name'
        ).annotate(
            puntos_totales=Sum('puntos')
        ).order_by('-puntos_totales') # Ordena de mayor a menor
        
        return leaderboard