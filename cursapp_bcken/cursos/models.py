from django.db import models
from core.models import Usuario

class Curso(models.Model):
    """
    Representa un curso en el marketplace.
    Soporta la información de monetización y contenido principal.
    """
    
    ESTADO_BORRADOR = 1
    ESTADO_PUBLICADO = 2
    ESTADO_SUSPENDIDO = 3
    
    ESTADOS_CHOICES = (
        (ESTADO_BORRADOR, 'Borrador'),
        (ESTADO_PUBLICADO, 'Publicado'),
        (ESTADO_SUSPENDIDO, 'Suspendido'),
    )
    
    titulo = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, help_text='URL amigable')
    descripcion = models.TextField(max_length=500)
    
    # Relación con el instructor
    instructor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, # Si el Instructor es eliminado, el curso se queda sin profesor.
        limit_choices_to={'rol': Usuario.ROL_INSTRUCTOR}, # Solo Instructores pueden crear cursos
        null=True,
        blank=True
    )
    
    # Monetización: Precios anclado al USD del BCV
    
    precio_usd = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        default=0.00,
        help_text='Precio USD'
    )
    
    # Credenciales
    req_certificado = models.BooleanField(default=False)
    
    # Estadi del curso
    estado = models.PositiveSmallIntegerField(choices=ESTADOS_CHOICES, default=ESTADO_BORRADOR)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
# --- Estructura de Contenido (Módulo y Lección) ---
class Modulo(models.Model):
    """
    Un módulo o sección dentro de un Curso.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=500)
    orden = models.PositiveIntegerField(default=0, help_text='Orden de aparición en el curso.')
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['orden']
        unique_together = ('curso', 'orden') # Asegura que no haya dos módulos con el mismo orden en el mismo curso.
        
    def __str__(self):
        return f"{self.curso.titulo} - Módulo {self.orden}: {self.titulo}"
    
class Leccion(models.Model):
    """
    Una lección individual dentro de un Módulo.
    Contiene el contenido didáctico (video, documento, SCORM).
    """
    TIPO_VIDEO = 1
    TIPO_DOCUMENTO = 2
    TIPO_CUESTIONARIO = 3
    TIPO_SCORM = 4
    
    TIPOS_CHOICES = (
        (TIPO_VIDEO, 'Video'),
        (TIPO_DOCUMENTO, 'Documento/PDF'),
        (TIPO_CUESTIONARIO, 'Cuestionario/Examen'),
        (TIPO_SCORM, 'Paquete SCORM'),
    )
    
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=0)
    tipo_contenido = models.PositiveSmallIntegerField(choices=TIPOS_CHOICES, default=TIPO_VIDEO, verbose_name='Tipo de Contenido')
    
    # Campo para almacenar la URL o el archivo del contenido.
    # Para SCORM, almacenará la ruta al paquete.
    archivo_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='Ruta o URL del contenido multimedia/SCORM')
    archivo = models.FileField(upload_to='lecciones/%Y/%m/', blank=True, null=True)
    
    duracion_minutos = models.PositiveIntegerField(default=0, help_text='Tiempo estimado de duración.')
    
    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ['orden']
        unique_together = ('modulo', 'orden')
        
    def __str__(self):
        return f"Lección {self.orden}: {self.titulo}"
    
class Categoria(models.Model):
    """Para organizar cursos (IA y Navegación)."""
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.nombre
    