from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import Sum, F, Q, DecimalField
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.shortcuts import get_object_or_404
from evaluacion.models import Inscripcion, PuntosAlumno, ProgresoLeccion, Resena, Transaccion
from cursos.models import Curso, Leccion, Cupon
from core.models import Usuario
from utils.monetizacion import obtener_tasa_bcv
from .serializers import (
    InscripcionSerializer, 
    InscripcionCrearSerializer, 
    LeaderboardSerializer,
    ScormProgresoSerializer,
    ResenaSerializer,
    MiAprendizajeSerializer
)

# --- PERMISOS PERSONALIZADOS ---
class IsOwnerOfResenaOrReadOnly(permissions.BasePermission):
    """
    Permiso para que solo el alumno que escribió la reseña pueda
    editarla o borrarla.
    """
    def has_object_permission(self, request, view, obj):
        # Permite lectura (GET) a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite escritura solo si es el dueño de la inscripción
        return obj.inscripcion.alumno == request.user

# --- VIEWSETS ---
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
        codigo_cupon = serializer.validated_data.get('codigo_cupon')
        alumno = request.user
        
        # Verificación de preexistencia
        if Inscripcion.objects.filter(alumno=alumno, curso_id=curso_id, estado_pago__in=[Inscripcion.ESTADO_PAGADO, Inscripcion.ESTADO_PENDIENTE]).exists():
            return Response(
                {"error": "Ya tienes una inscripción (activa o pendiente de pago) para este curso."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        curso = get_object_or_404(Curso, pk=curso_id, estado=Curso.ESTADO_PUBLICADO)
        
        # Lógica de Cupones y Cálculo de Precio
        precio_final = curso.precio_usd
        cupon_aplicado = None
        
        if codigo_cupon:
            try:
                cupon = Cupon.objects.get(codigo__iexact=codigo_cupon)
                
                # Validar si el cupón está activo
                if not cupon.esta_activo:
                    raise ValidationError("Este cupón ha expirado o ha alcanzado su límite de usos.")
                
                # Validar si aplica a este curso
                if cupon.cursos.exists() and not cupon.cursos.filter(pk=curso.id).exists():
                    raise ValidationError("Este cupón no es válido para este curso.")
                
                # Si todo el válido, aplica el descuento
                descuento = (precio_final * cupon.porcentaje_descuento) / Decimal('100.00')
                precio_final = precio_final - descuento
                cupon_aplicado = cupon # Guarda cupón para incrementar su uso
            except Cupon.DoesNotExist:
                raise ValidationError("El código de cupón ingresado no existe.")
            except Exception as e:
                # Captura cualquier otra validación
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creación de la Inscripción Pendiente
        inscripcion = Inscripcion.objects.create(
            alumno=alumno,
            curso=curso,
            precio_pagado_usd=precio_final,
            estado_pago=Inscripcion.ESTADO_PENDIENTE
        )
        
        # Incrementar uso del cupón (si se usó)
        if cupon_aplicado:
            cupon_aplicado.usos_actuales += 1
            cupon_aplicado.save(update_fields=['usos_actuales'])
        
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
                    "precio_original_usd": str(curso.precio_usd),
                    "precio_final_usd": str(round(precio_final, 2)), # Precio con descuento (Si aplica)
                    "cupon_aplicado": codigo_cupon if cupon_aplicado else None,
                    "tasa_bcv": str(tasa_bcv),
                    "monto_ves": str(round(monto_ves, 2)),
                    "metodos": ["Pago Movil", "Transferencia", "TDC/TDD"],
                    "referencia_pago": inscripcion.id
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
        
        if created:
            # Si es la primera vez, el punto de entrada es 'ab-initio' (desde el inicio)
            progreso.entry_point = 'ab-initio'
        else:
            # Si ya existía, el punto de entrada es 'resume' (continuar)
            progreso.entry_point = 'resume'
            
        return progreso
    
class ResenaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Reseñas.
    - Anidada bajo 'cursos' para listar reseñas de un curso.
    - Permite a alumnos inscritos crear
    - Permite a alumnos propietarios editar o borrar.
    """
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOfResenaOrReadOnly]
    
    def get_queryset(self):
        # Filtra las reseñas basadas en el curso_pk de la URL
        curso_pk = self.kwargs.get('curso_pk')
        if curso_pk:
            return Resena.objects.filter(inscripcion__curso_id=curso_pk).order_by('-fecha_creacion')
        return Resena.objects.none() # No mostrar todas las reseñas globalmente
    
    def perform_create(self, serializer):
        # El serializador ya valida la propiedad de la inscripción
        serializer.save()

class InstructorDashboardAPIView(generics.GenericAPIView):
    """
    Endpoint de analísticas (Dashboard) para Instructores.
    Provee un resumen de ganancias, incripciones y pagos pendientes.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwars):
        user = request.user
        
        # Verifica que el usuario sea instructor
        if not user.es_instructor:
            raise PermissionDenied("Solo los instructores pueden acceder al Dashboard.")
        
        # Obtiene todas las transacciones de este instructor
        transacciones = Transaccion.objects.filter(inscripcion__curso__instructor=user)
        
        # Calcular agregados de ganancias
        analiticas = transacciones.aggregate(
            ganancias_totales_usd=Sum('monto_instructor_usd'),
            ganancias_pendientes_usd=Sum(
                'monto_instructor_usd',
                filter=Q(estado_pago_instructor=Transaccion.ESTADO_PENDIENTE)
            ),
            ganancias_pagadas_usd=Sum(
                'monto_instructor_usd',
                filter=Q(estado_pago_instructor=Transaccion.ESTADO_PAGADO)
            )
        )
        
        # Calcular total de inscripciones pagadas
        total_inscripciones = Inscripcion.objects.filter(
            curso__instructor=user,
            estado_pago=Inscripcion.ESTADO_PAGADO
        ).count()
        
        # Calcular total de reseñas
        total_resenas = Resena.objects.filter(inscripcion__curso__instructor=user).count()
        
        return Response({
            'total_inscripciones': total_inscripciones,
            'total_resenas': total_resenas,
            'ganancias_totales_usd': analiticas.get('ganancias_totales_usd') or 0.00,
            'ganancias_pendientes_usd': analiticas.get('ganancias_pendientes_usd') or 0.00,
            'ganancias_pagadas_usd': analiticas.get('ganancias_pagadas_usd') or 0.00,
        })
        
class MiAprendizajeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para el Dashboard "Mi Aprendizaje" del alumno.
    Devuelve solo las inscripciones PAGADAS y ACTIVAS.
    """
    serializer_class = MiAprendizajeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Devuelve solo los cursos pagos del usuario actual
        return Inscripcion.objects.filter(
            alumno=self.request.user,
            estado_pago=Inscripcion.ESTADO_PAGADO
        ).select_related('curso', 'curso__instructor')
        
class PagoWebhookAPIView(APIView):
    """
    Endpoint de Webhook para que la pasarela de pago externa
    confirme que un pago fue exitoso.
    """
    # PERMISO PÚBLICO
    # La pasarela de pago no tiene un token de usuario
    permission_classes = [permissions.AllowAny]
    
    # DESACTIVAR CSRF
    # Necesario para que la API externa pueda hacer POST
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # SEGURIDAD
        # Se debe colocar una firma que envia la pasarela de pago
        # para verificar que es una petición legitima y no es un ataque.
        
        # OBTENER DATOS
        # Asumiendo que la pasarela nos envía un JSON como:
        # { "evento": "pago_exitoso", "referencia": <ID_DE_LA_INSCRIPCION> }
        data = request.data
        evento = data.get('evento')
        referencia_id = data.get('referencia')
        
        if evento == 'pago_exitoso' and referencia_id:
            try:
                # Encontrar y actualizar la Inscripción
                inscripcion = Inscripcion.objects.get(
                    id=referencia_id,
                    estado_pago=Inscripcion.ESTADO_PENDIENTE
                )
                
                inscripcion.estado_pago = Inscripcion.ESTADO_PAGADO
                inscripcion.referencia_pago = data.get('id_transaccion_gateway')
                inscripcion.save(update_fields=['estado_pago', 'referencia_pago'])
                
                return Response(
                    {"status": "ok", "inscripcion_id": inscripcion.id},
                    status=status.HTTP_200_OK
                )
            except Inscripcion.DoesNotExist:
                return Response(
                    {"error": "Inscripción no encontrada o ya procesada."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": f"Error interno: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        return Response(
            {"error": "Datos de webhook inválidos"}, 
            status=status.HTTP_400_BAD_REQUEST
        )