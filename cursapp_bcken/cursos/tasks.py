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
    try:
        # 1. Obtener la lección y marcarla como "Procesando"
        leccion = Leccion.objects.get(id=leccion_id)
        leccion.estado_procesamiento = Leccion.ESTADO_PROCESANDO
        leccion.save()
        
        # --- INICIO DE LÓGICA DE PROCESAMIENTO (Simulación) ---
        
        # En producción, aquí llamarías a FFMPEG usando 'leccion.archivo.path'
        # Ejemplo:
        # input_path = leccion.archivo.path
        # output_path = f"/media/hls/{leccion_id}/video.m3u8"
        # subprocess.run(['ffmpeg', '-i', input_path, output_path])
        
        # Simulamos un procesamiento de 30 segundos
        time.sleep(30) 
        
        # --- FIN DE LA LÓGICA DE PROCESAMIENTO ---
        
        # 2. Actualizar la lección con el resultado
        # (Simulamos la nueva URL del video procesado en HLS)
        leccion.archivo_url = f"{leccion.archivo.url}.m3u8" # Simulamos la URL del manifiesto
        leccion.estado_procesamiento = Leccion.ESTADO_COMPLETADO
        leccion.save(update_fields=['archivo_url', 'estado_procesamiento'])
        
        return f"Video {leccion_id} procesado exitosamente."

    except Leccion.DoesNotExist:
        print(f"Error Tarea: Lección ID {leccion_id} no encontrada.")
        return f"Error: Lección {leccion_id} no encontrada."
    except Exception as e:
        print(f"Error Tarea procesando {leccion_id}: {e}")
        # Marcar la lección como fallida
        try:
            leccion = Leccion.objects.get(id=leccion_id)
            leccion.estado_procesamiento = Leccion.ESTADO_ERROR
            leccion.save(update_fields=['estado_procesamiento'])
        except Leccion.DoesNotExist:
            pass # No se puede hacer nada si ya fue borrada
        return f"Error procesando {leccion_id}."