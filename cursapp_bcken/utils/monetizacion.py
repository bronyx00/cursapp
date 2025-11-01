import requests
from django.core.cache import cache
from django.conf import settings
from decimal import Decimal

# Definición de constantes
API_URL = "https://api.dolarvzla.com/public/exchange-rate"
CAMPO_NAME = "current" # Nombre del campo que especifica la Tasa BCV en la API
CACHE_KEY = "bcv_exchange_rate"
CACHE_TIMEOUT = 60 * 60 * 6 # 6 horas de caché

def obtener_tasa_bcv():
    """
    Obtener la tasa de cambio USD/VES del BCV, usando caché para optimizar.
    Si la API falla, devuelve un valor predeterminado o la última tasa conocida.
    """
    # Intentar obtener de la caché
    tasa = cache.get(CACHE_KEY)
    if tasa is not None:
        return Decimal(tasa)
    
    # Si no está en caché, consultar la API externa
    try:
        response = requests.get(API_URL, timeout=5) 
        response.raise_for_status() # Lanza HTTPError si la respuesta es un error
        data = response.json()
        
        # Parsear la respuesta y encontrar la tasa del BCV
        tasa_str = data.get(CAMPO_NAME, None).get('usd')
        
        if tasa_str:
            tasa = Decimal(tasa_str)
            # Almacena en caché antes de devolver
            cache.set(CACHE_KEY, tasa_str, CACHE_TIMEOUT)
            return tasa
        # Si la API responde pero no tiene el campo esperado
        print("Advertencia: API de BCV no devolvió la tasa 'rate'.")
        return Decimal('0.00') # Valor por defecto de emergencia
    except requests.RequestException as e:
        print(f"Error al conectar con la API de BCV: {e}")
        # Retornar la última tasa conocida o un valor fijo en caso de fallo total
        return Decimal('0.00')
    