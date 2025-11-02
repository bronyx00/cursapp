from django.db import models
from core.models import Usuario
from cursos.models import Leccion
from django.db.models import Sum
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# -------------------------------------------------------------
# 1. Modelos de Evaluación (Cuestionario, Pregunta, Respuesta)
# -------------------------------------------------------------

class Cuestionario(models.Model):
    """
    Representa un examen o cuestionario que está asignado a una Lección.
    Soporta la evaluación automatizada.
    """
    leccion = models.OneToOneField(
        Leccion,
        on_delete=models.CASCADE,
        related_name='cuestionario',
        help_text='Cuestionario asociado a esta lección.'
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    
    # Parámetros de la Evaluación
    calificacion_minima = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=70.00,
        help_text='Porcentaje mínimo requerido para aprobar.'
    )
    maximo_intentos = models.PositiveSmallIntegerField(
        default=3,
        help_text='Número máximo de veces que el alumno puede intentar el cuestionario.'
    )
    
    class Meta:
        verbose_name = "Cuestionario"
        verbose_name_plural = "Cuestionarios"
        
    def __str__(self):
        return f"Cuestionario: {self.titulo} ({self.leccion.titulo})"
    
class Pregunta(models.Model):
    """
    Representa una pregunta de evaluación.
    Se puede reutilizar en múltiples Cuestionarios.
    """
    TIPO_OPCION_MULTIPLE = 1
    TIPO_VERDADERO_FALSO = 2
    TIPO_EMPAREJAMIENTO = 3
    
    TIPO_PREGUNTA_CHOICE = (
        (TIPO_OPCION_MULTIPLE, 'Opción Múltiple'),
        (TIPO_VERDADERO_FALSO, 'Verdadero/Falso'),
        (TIPO_EMPAREJAMIENTO, 'Emparejamiento'),
    )
    
    cuestionario = models.ManyToManyField(
        Cuestionario,
        related_name='preguntas',
        blank=True,
        help_text="Los cuestionarios que usan esta pregunta."
    )
    
    texto_pregunta = models.TextField()
    tipo_pregunta = models.PositiveSmallIntegerField(
        choices=TIPO_PREGUNTA_CHOICE,
        default=TIPO_OPCION_MULTIPLE
    )
    puntuacion = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    
    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        
    def __str__(self):
        return f"{self.get_tipo_pregunta_display()}: {self.texto_pregunta[:50]}..."
    
class OpcionRespuesta(models.Model):
    """
    Opciones de respuesta para preguntas de Opción Múltiple o Verdadero/Falso.
    """
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='opciones'
    )
    texto_opcion = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Opción de Respuesta"
        verbose_name_plural = "Opciones de Respuesta"
        
    def __str__(self):
        return f"{self.texto_opcion} ({'Correcta' if self.es_correcta else 'Incorrecta'})"
    
# -------------------------------------------------------------
# 2. Modelos de Trazabilidad y Progreso
# -------------------------------------------------------------

class Inscripcion(models.Model):
    """
    Registrar la inscripción de un Alumno a un Curso.
    """
    
    # Definición de Estados de Pago
    ESTADO_PENDIENTE = 1
    ESTADO_PAGADO = 2
    ESTADO_FALLIDO = 3
    
    ESTADOS_PAGO_CHOICHES = (
        (ESTADO_PENDIENTE, 'Pendiente de Pago'),
        (ESTADO_PAGADO, 'Pagado'),
        (ESTADO_FALLIDO, 'Fallido/Cancelado'),
    )
    
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='inscripciones_curso',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
    
    # Campo de monetización
    precio_pagado_usd = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Precio en USD del curso al momento de la inscripción."
    )
    estado_pago = models.PositiveSmallIntegerField(
        choices=ESTADOS_PAGO_CHOICHES,
        default=ESTADO_PENDIENTE,
        verbose_name="Estado de Pago"
    )
    referencia_pago = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    porcentaje_progreso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Porcentaje de finalización total del curso."
    )
    calificacion_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Calificación promedio al final del curso."
    )
    
    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        # unique_together = ('alumno', 'curso') # Un alumno solo puede inscribirse una vez al mismo curso.
        
    def __str__(self):
        return f"{self.alumno.username} inscrito en {self.curso.titulo}"
    
class ProgresoLeccion(models.Model):
    """
    Mide el progreso individual del alumno en cada leccion.
    Soporta el seguimiento en Tiendo de dedicación y Estado de finalización.
    """
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='progreso_lecciones'
    )
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    
    # Tiempo de dedicación
    tiempo_dedicado_minutos = models.PositiveIntegerField(default=0, help_text="Tiempo total que el alumno ha pasado en la lección.")
    
    # Porcentaje de estado de finalización del curso
    porcentaje_visto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Porcentaje de video/contenido visto."
    )
    
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    # cmi.core.lesson_status (Estado de la lección)
    # Almacena el estado detallado reportado por el SCORM
    ESTADO_SCORM_CHOICES = (
        ('passed', 'Aprobado'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
        ('incomplete', 'Incompleto'),
        ('browsed', 'Visto por encima'),
        ('not attempted', 'No intenrado'),
    )
    estado_scorm = models.CharField(
        max_length=20,
        choices=ESTADO_SCORM_CHOICES,
        default='Not attempted',
        blank=True
    )
    
    # cmi.core.score.raw (Puntuación)
    puntuacion_scorm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Puntuación (0-100) reportada por el SCORM"
    )
    
    # cmi.suspend_data (Datos de Suspención)
    # Campo CRÍTICO. Guarda dónde quedó el usuario en el SCORM (Ej: "página 3, video 1:20")
    suspend_data = models.TextField(
        blank=True,
        null=True,
        help_text="Datos de suspensión del SCORM (dónde guardar)"
    )
    
    # cmi.core.entry (Punto de entrada)
    # 'ab-initio' (primera vez), 'resume' (continuar)
    entry_point = models.CharField(max_length=10, default='ab-initio', blank=True)
    
        
    class Meta:
        verbose_name = "Progreso de Lección"
        verbose_name_plural = "Progresos de Lección"
        unique_together = ('inscripcion', 'leccion') # Un alumno solo tiene un registro de progreso por lección.
        
    def __str__(self):
        return f"Progreso {self.leccion.titulo}: {self.porcentaje_visto}%"
    
class IntentoCuestionario(models.Model):
    """
    Almacena un intento de un alumno en un Cuestionario.
    Utilizado para el registro de calificaciones.
    """
    inscripciones = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='intentos_cuestionario'
    )
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
    fecha_intento = models.DateTimeField(auto_now_add=True)
    
    # Registro de calificaciones
    puntuacion_obtenida = models.DecimalField(max_digits=5, decimal_places=2)
    puntuacion_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    aprobado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Intento de Cuestionario"
        verbose_name_plural = "Intentos de Cuestionario"
        ordering = ['-fecha_intento'] # Ordenamos para obtener el último o el mejor intento fácilmente.
        
    def __str__(self):
        return f"Intento de {self.cuestionario.titulo} - Puntuación: {self.puntuacion_obtenida}"
    
class InteraccionLeccion(models.Model):
    """
    Registra el historial de visualización y 'tasa implícita' para alimentar
    el motor de recomendación.
    """
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='interacciones'
    )
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='interacciones'
    )
    
    # Data para Recomendación
    # Tasa implícita: cuánto tiempo retuvo la lección el interés.
    tasa_interes = models.PositiveSmallIntegerField(
        default=0,
        help_text="Tasa de interés implícita"
    )
    
    ultima_vista = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Interacción de Lección"
        verbose_name_plural = "Interacciones de Lección"
        # Solo un registro de interacción por alumno y lección.
        unique_together = ('alumno', 'leccion')
        
    def __str__(self):
        return f"{self.alumno.username} interactuó con {self.leccion.titulo}"

# -------------------------------------------------------------
# 3. Modelos de Credenciales (Certificados e Insignias)
# -------------------------------------------------------------

class Certificado(models.Model):
    """
    Representa el certificado emitido al finalizar y aprobar un curso.
    Incluye un código único para la validación.
    """
    inscripcion = models.OneToOneField(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='certificado',
        help_text="Inscripción que generó este certificado."
    )
    
    # Mecanismo de Validación (Código Único y Verificable)
    codigo = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Código único e inmutable para la verificación del certificado."
    )

    fecha_emision = models.DateTimeField(auto_now_add=True)
    url_certificado = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL al documento PDF/imagen del certificado."
    )
    
    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        
    def __str__(self):
        return f"Certificado para {self.inscripcion.alumno.username} en {self.inscripcion.curso.titulo}"
    
class Insignia(models.Model):
    """
    Representa una insignia (Badge) que el alumno obtiene por logros.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    imagen_url = models.URLField(max_length=500)
    
    # Criterio de logros (ej: Completar 10 lecciones, 5 cursos, etc.)
    criterio_logros = models.CharField(
        max_length=255,
        help_text="Criterio a cumplir para obtener la insignia."
    )
    
    class Meta:
        verbose_name = "Insignia"
        verbose_name_plural = "Insignias"
        
    def __str__(self):
        return self.nombre
    
class InsigniaObtenida(models.Model):
    """
    Registro de que un alumno ha ganado una Insignia.
    """
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='insignias_obtenias',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Insignia Obtenida"
        verbose_name_plural = "Insignias Obtenidas"
        unique_together = ('alumno', 'insignia') # Un alumno solo puede obtener la misma insignia una vez.
    
    def __str__(self):
        return f"{self.alumno.username} obtuvo {self.insignia.nombre}"
    
# -------------------------------------------------------------
# 4. Modelos de Gamificación (Puntos y Recompensas)
# -------------------------------------------------------------

class PuntosAlumno(models.Model):
    """
    Registra las transacciones de puntos ganados por un Alumno.
    La suma de todas las entradas define la puntuación total del alumno.
    """
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='puntos_ganados',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    puntos = models.IntegerField(default=0, help_text="Puntos ganados o restados")
    motivo = models.CharField(
        max_length=255,
        help_text="Razón por la cual se otorgaron/restaron los puntos."
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Puntos de Alumno"
        verbose_name_plural = "Puntos de Alumnos"
        ordering = ['-fecha_registro']
        
    def __str__(self):
        return f"{self.alumno.username}: {self.puntos} puntos por {self.motivo}"
    
    # Propiedad para obtener la puntuación total del alumno (Para Leaderboard)
    @classmethod
    def obtener_puntuacion_total(cls, alumno_id):
        """Calcula la puntuacion total de un alumno."""
        return cls.objects.filter(alumno_id=alumno_id).aggregate(total=Sum('puntos'))['total'] or 0
    
class Recompensa(models.Model):
    """
    Define un artículo o beneficio que puede ser canjeado con puntos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo_puntos = models.PositiveIntegerField(help_text="Costo de la recompensa en puntos.")
    
    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"
        
    def __str__(self):
        return f"{self.nombre} ({self.costo_puntos} puntos)"
    
    
class CanjeRecompensa(models.Model):
    """
    Registra el canje de una recompensa por parte de un alumno.
    """
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='canjes_realizados',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    recompensa = models.ForeignKey(Recompensa, on_delete=models.CASCADE)
    fecha_canje = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Canje de Recompensa"
        verbose_name_plural = "Canjes de Recompensa"
        ordering = ['-fecha_canje']
        
    def __str__(self):
        return f"{self.alumno.username} canjeó {self.recompensa.nombre}"
    
# -------------------------------------------------------------
# 5. Modelo de Reseñas y Calificaciones Multifacéticas
# -------------------------------------------------------------

class Resena(models.Model):
    """
    Una reseña multifacética dejada por un alumno.
    Vinculada a la Inscripción para asegurar que solo alumnos pagos califiquen.
    """
    # Votación de 1 a 5 estrellas
    STAR_CHOICES = [
        (1, '1 Estrella'),
        (2, '2 Estrellas'),
        (3, '3 Estrellas'),
        (4, '4 Estrellas'),
        (5, '5 Estrellas'),
    ]
    
    # 1 reseña por inscripción
    inscripcion = models.OneToOneField(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='reseña',
        help_text="Inscripción (compra) asociada a esta reseña."
    )
    
    # Comentario cualitativo
    comentario = models.TextField(blank=True, null=True)
    
    # --- Calificaciones Específicas (Multifacéticas) ---
    calificacion_general = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=STAR_CHOICES
    )
    calificacion_calidad_contenido = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=STAR_CHOICES,
        help_text="Calidad de la información y materiales."
    )
    calificacion_claridad_explicacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=STAR_CHOICES,
        help_text="Qué tan bien explica el instructor."
    )
    calificacion_utilidad_practica = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=STAR_CHOICES,
        help_text="Qué tan útil o entretenido fue el curso."
    )
    calificacion_soporte_instructor = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=STAR_CHOICES,
        help_text="Rapidez y calidad de respuesta del instructor."
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-fecha_creacion']
        unique_together = ('inscripcion',) # Asegura que la inscripción sea única
        
    def __str__(self):
        return f"Reseña de {self.inscripcion.alumno.username} para {self.inscripcion.curso.titulo}"
    