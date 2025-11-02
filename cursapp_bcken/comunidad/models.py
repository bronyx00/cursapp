from django.db import models
from core.models import Usuario
from cursos.models import Leccion

class PreguntaForo(models.Model):
    """
    Una pregunta (hilo) iniciada por un alumno o instructor,
    vinculada directamente a una lección específica.
    """
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='preguntas_foro')
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='preguntas_foro')
    titulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pregunta de Foro"
        verbose_name_plural = "Preguntas de Foro"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"Pregunta de {self.autor.username} en {self.leccion.titulo}: {self.titulo}"
    
class RespuestaForo(models.Model):
    """
    Una respuesta a una pregunta del foro.
    """
    pregunta = models.ForeignKey(PreguntaForo, on_delete=models.CASCADE, related_name='respuestas')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='respuestas_foro')
    cuerpo = models.TextField()
    
    # Permite al instructor o al autor marcarla como útil
    es_util = models.BooleanField(
        default=False,
        help_text="Marcada por el instructor como la respuesta correcta o más útil."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Respuesta de Foro"
        verbose_name_plural = "Respuestas de Foro"
        ordering = ['fecha_creacion']
        
    def __str__(self):
        return f"Respuesta de {self.autor.username} a '{self.pregunta.titulo}'"