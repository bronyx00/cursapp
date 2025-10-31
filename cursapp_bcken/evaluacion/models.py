from django.db import models
from core.models import Usuario
from cursos.models import Leccion
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
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='inscripciones_curso',
        limit_choices_to={'rol': Usuario.ROL_ALUMNO}
    )
    curso = models.ForeignKey('cursos.Curso', on_delete=models.CASCADE)
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
        unique_together = ('alumno', 'curso') # Un alumno solo puede inscribirse una vez al mismo curso.
        
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
    fecha_completado = models.DateTimeField(null=False, blank=True)
    
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