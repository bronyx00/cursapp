from django.apps import AppConfig


class EvaluacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evaluacion'
    
    def ready(self):
        import evaluacion.signals # Importa las señales al iniciar la app
