from django.contrib import admin
from .models import PreguntaForo, RespuestaForo

class RespuestaForoInline(admin.TabularInline):
    """Permite moderar respuestas dentro de la pregunta."""
    model = RespuestaForo
    fields = ('autor', 'cuerpo', 'es_util')
    readonly_fields = ('autor', 'cuerpo')
    extra = 0
    autocomplete_fields = ('autor',)
    
@admin.register(PreguntaForo)
class PreguntaForoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'leccion', 'fecha_creacion')
    search_fields = ('titulo', 'autor__username', 'leccion__titulo')
    autocomplete_fields = ('autor', 'leccion') # Optimiza
    inlines = [RespuestaForoInline]
    
@admin.register(RespuestaForo)
class RespuestaForoAdmin(admin.ModelAdmin):
    list_display = ('get_pregunta_titulo', 'autor', 'es_util', 'fecha_creacion')
    search_fields = ('cuerpo', 'autor__username', 'pregunta__titulo')
    autocomplete_fields = ('autor', 'pregunta')
    
    @admin.display(description='Pregunta')
    def get_pregunta_titulo(self, obj):
        return obj.pregunta.titulo