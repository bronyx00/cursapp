from rest_framework import serializers
from evaluacion.models import Inscripcion, ProgresoLeccion, Resena
from core.api.serializers import PerfilUsuarioSerializer
from core.models import Usuario

class InscripcionSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una nueva inscripción (Iniciar un proceso de pago)
    """
    curso_titulo = serializers.ReadOnlyField(source='curso.titulo')
    
    class Meta:
        model = Inscripcion
        fields = (
            'id', 'curso', 'curso_titulo', 'alumno',
            'precio_pagado_usd', 'estado_pago', 'referencia_pago',
            'fecha_inscripcion'
        )
        read_only_fields = ('alumno', 'precio_pagado_usd', 'estado_pago', 'referencia_pago')
        
class InscripcionCrearSerializer(serializers.ModelSerializer):
    """
    Serializer simplicado solo para la creación.
    El alumno solo necesita enviar el ID del curso.
    """
    codigo_cupon = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        write_only=True
    )
    class Meta:
        model = Inscripcion
        fields = ('curso', 'codigo_cupon')
        
    def create(self, validated_data):
        # La lógica de creación se moverá al ViewSet para obtener el usuario y el precio.
        return super().create(validated_data)
    
class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer especial para la tabla de calificación (Leaderboard).
    Usa el modelo Usuario.
    """
    full_name = serializers.CharField(source='get_full_name')
    puntuacion_total = serializers.IntegerField(source='xp_totales') # Usamos XP para el Leaderboard
    
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'full_name', 'puntuacion_total', 'foto_perfil')
        
class ScormProgresoSerializer(serializers.ModelSerializer):
    """
    Serializer específico para la comunicación SCORM.
    Maneja los campos CMI (Computer-Managed Instruction) que guardamos
    en el modelo ProgresoLeccion
    """
    class Meta:
        model = ProgresoLeccion
        
        # Campos que se podrán LEER y ACTUALIZAR desde Vue.js
        fields = (
            'id',
            'leccion',
            'estado_scorm', # (Ej: 'completed', 'failed', 'incomplete') 
            'puntuacion_scorm', # (Ej: 80.5)
            'suspend_data', # (Ej: "pagina_3, pregunta_5")
            'entry_point', # (Ej: 'resume' o 'ab-inition')
            'completado'
        )
        read_only_fields = ('id', 'leccion')
        
class ResenaSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar y crear reseñas multifacéticas.
    """
    # Mostrar quién escribió la reseña (solo lectura)
    alumno = PerfilUsuarioSerializer(source='inscripcion.alumno', read_only=True)
    
    # Campo para que el usuario envíe el ID de la inscripción
    inscripcion_id = serializers.PrimaryKeyRelatedField(
        queryset=Inscripcion.objects.all(),
        source='inscripcion',
        write_only=True
    )
    
    class Meta:
        model = Resena
        fields = (
            'id',
            'inscripcion_id', # Para escribir
            'alumno', # Para leer
            'comentario',
            'calificacion_general',
            'calificacion_calidad_contenido',
            'calificacion_claridad_explicacion',
            'calificacion_utilidad_practica',
            'calificacion_soporte_instructor',
            'fecha_creacion',
        )
        read_only_fields = ('id', 'fecha_creacion', 'alumno')
        
    def validate_inscripcion_id(self, inscripcion):
        """
        Asegura que el usuario que postea es el dueño de la inscripción.
        Asegura que el curso esté pagado.
        """
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("Contexto de request no disponible.")
        if inscripcion.alumno != request.user:
            raise serializers.ValidationError("No puedes dejar una reseña para una inscripción que no te pertenece.")
        if inscripcion.estado_pago != Inscripcion.ESTADO_PAGADO:
            raise serializers.ValidationError("Solo puedes dejar reseñas de cursos que hayas pagado.")
        if Resena.objects.filter(inscripcion=inscripcion).exists():
            raise serializers.ValidationError("Ya has enviado una reseña para este curso.")
        
        return inscripcion