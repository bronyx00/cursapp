from celery import shared_task
from .models import Leccion
import time # Para simular el procesamiento
import subprocess # (Opcional) Para llamar a FFMPEG en el futuro

@shared_task
def process_video_task(leccion_id):
    """
    Tarea asíncrona robusta para "procesar" un video subido.
    (Simulación de FFMPEG)
    """
    # 1. Marcar como "Procesando"
    try:
        leccion = Leccion.objects.get(id=leccion_id)
        leccion.estado_procesamiento = Leccion.ESTADO_PROCESANDO
        leccion.save(update_fields=['estado_procesamiento']) # 👈 Actualización eficiente
    except Leccion.DoesNotExist:
        print(f"Error Tarea: Lección ID {leccion_id} no encontrada.")
        return f"Error: Lección {leccion_id} no encontrada."
    
    # 2. Iniciar procesamiento
    try:
        # --- INICIO DE LÓGICA DE PROCESAMIENTO (Simulación) ---
        # (Aquí iría la lógica pesada de FFMPEG)
        time.sleep(30) # Simulacion
        url_simulada = f"{leccion.archivo.url}.m3u8" # Simulado
        # --- FIN DE LA LÓGICA DE PROCESAMIENTO ---
        
        # 3. 🚨 CORRECCIÓN DE ROBUSTEZ (Evitar Race Conditions)
        # Volvemos a obtener el objeto FRESCO de la BD antes de guardar
        leccion_actualizada = Leccion.objects.get(id=leccion_id)
        
        leccion_actualizada.archivo_url = url_simulada
        leccion_actualizada.estado_procesamiento = Leccion.ESTADO_COMPLETADO
        leccion_actualizada.save(
            update_fields=['archivo_url', 'estado_procesamiento']
        )
        
        return f"Video {leccion_id} procesado exitosamente."

    except Exception as e:
        print(f"Error Tarea procesando {leccion_id}: {e}")
        # Marcar la lección como fallida
        try:
            leccion_fallida = Leccion.objects.get(id=leccion_id)
            leccion_fallida.estado_procesamiento = Leccion.ESTADO_ERROR
            leccion_fallida.save(update_fields=['estado_procesamiento'])
        except Leccion.DoesNotExist:
            pass # No se puede hacer nada si ya fue borrada
        return f"Error procesando {leccion_id}."