from django.db import models
from core.models import Usuario

class Categoria(models.Model):
    """
    Categorías principales para clasificar los cursos (Ej: Python, Diseño Gráfico, Marketing).
    Usado para recomendación basada en contenido.
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre
    
class Etiqueta(models.Model):
    """
    Etiquetas para granularidad y filtrado fino (Ej: REST API, VueJS).
    Usado par recomendación basada en contenido.
    """
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        
    def __str__(self):
        return self.nombre
    

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
    
    # Relaciones para Recomendación Basada en Contenido
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        related_name='cursos',
        null=True,
        blank=True,
        help_text='Clasificación principal del curso.'
    )
    etiquetas = models.ManyToManyField(
        Etiqueta,
        related_name='cursos',
        blank=True,
        help_text='Palabras claves para búsqueda y recomendación.'
    )
    
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
    
    # Estado del curso
    estado = models.PositiveSmallIntegerField(choices=ESTADOS_CHOICES, default=ESTADO_BORRADOR)
    
    total_resenas = models.PositiveIntegerField(default=0)
    
    # Promedios de las reseñas
    promedio_calificacion_general = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    promedio_calidad_contenido = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    promedio_claridad_explicacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    promedio_utilidad_practica = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    promedio_soporte_instructor = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
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
    TIPO_ARTICULO = 5
    
    TIPOS_CHOICES = (
        (TIPO_VIDEO, 'Video'),
        (TIPO_DOCUMENTO, 'Documento/PDF'),
        (TIPO_CUESTIONARIO, 'Cuestionario/Examen'),
        (TIPO_SCORM, 'Paquete SCORM'),
        (TIPO_ARTICULO, 'Artículo/Código'),
    )
    
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_PROCESANDO = 'procesando'
    ESTADO_COMPLETADO = 'completado'
    ESTADO_ERROR = 'error'
    
    ESTADO_PROCESAMIENTO_CHOICES = (
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_PROCESANDO, 'Procesando Video'),
        (ESTADO_COMPLETADO, 'Completado y Listo'),
        (ESTADO_ERROR, 'Error de Procesamiento'),
    )
    
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=0)
    tipo_contenido = models.PositiveSmallIntegerField(choices=TIPOS_CHOICES, default=TIPO_VIDEO, verbose_name='Tipo de Contenido')
    
    cuerpo_articulo = models.TextField(
        blank=True,
        null=True,
        help_text="Contenido en Markdown para lecciones de tipo Artículo/Código."
    )
    
    # Campo para almacenar la URL o el archivo del contenido.
    # Para SCORM, almacenará la ruta al paquete.
    archivo_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='Ruta o URL del contenido multimedia/SCORM')
    archivo = models.FileField(upload_to='lecciones/%Y/%m/', blank=True, null=True)
    
    # Estado del video de la leccion
    estado_procesamiento = models.CharField(max_length=20, choices=ESTADO_PROCESAMIENTO_CHOICES, default=ESTADO_PENDIENTE)
    
    duracion_minutos = models.PositiveIntegerField(default=0, help_text='Tiempo estimado de duración.')
    
    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ['orden']
        unique_together = ('modulo', 'orden')
        
    def __str__(self):
        return f"Lección {self.orden}: {self.titulo}"
    
class Cupon(models.Model):
    """
    Representa un cupón de descuento.
    Puede ser creado con un Instructor (limitado a sus cursos) o un Admin (global)
    """
    codigo = models.CharField(max_length=50, unique=True, help_text="El código que el alumno usará")
    # El instructor que creó este cupón (si es nulo, es un cupón de admin/plataforma)
    instructor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='cupones',
        null=True,
        blank=True,
        limit_choices_to={'rol': Usuario.ROL_INSTRUCTOR}
    )
    # A qué cursos aplica este cupón
    cursos = models.ManyToManyField(
        Curso,
        related_name='cupones',
        blank=True, # Si está vacío, puede aplicar a todos (lógica de admin)
        help_text="Cursos a los que aplica ete cupón."
    )
    
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Descuento en porcentaje (ej. 25.00)")
    fecha_expiracion = models.DateTimeField(null=True, blank=True)
    usos_maximos = models.PositiveIntegerField(default=100)
    usos_actuales = models.PositiveIntegerField(default=0, editable=False)
    
    class Meta:
        verbose_name = "Cupón"
        verbose_name_plural = "Cupones"
        
    def __str__(self):
        return f"{self.codigo} ({self.porcentaje_descuento})"
    
    @property
    def esta_activo(self):
        """Verifica si el cupón es válido (no expirado y con usos)."""
        from django.utils import timezone
        if self.fecha_expiracion and self.fecha_expiracion < timezone.now():
            return False
        return self.usos_actuales < self.usos_maximos