import os 
from celery import Celery

# Configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cursapp_bcken.settings')

app = Celery('cursapp_bcken')

# Usa la configuración de Django (Celery buscará variables con el prefijo 'CELERY_')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas automáticamente en todas las apps
# Buscará archivos llamados 'tasks.py' en todas las apps
app.autodiscover_tasks()