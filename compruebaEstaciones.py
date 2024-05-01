'''
Devuleve un archivo con el listado de estaciones de la red EMA de MeteoChile con su respectivo código nacional
'''

import requests
import json
import pytz
from datetime import datetime, timedelta
utc_zone = pytz.utc
local_zone = pytz.timezone('Chile/Continental')
now = datetime.now()
ayer = now - timedelta(days=1)

user_token = ''
token_api = ''
#esto no debería estar en el código final se debe usar un archivo de configuración o usar variables de entorno

try:
    # Obtener datos de las estaciones
    url = f'https://climatologia.meteochile.gob.cl/application/servicios/getEstacionesRedEma?usuario={user_token}&token={token_api}'
    response = requests.get(url)
    data = json.loads(response.text)
except Exception as e:
    print(f'Error al obtener datos de las estaciones: {e}')
    exit()
# Crear diccionario de estaciones
diccionario_estacionesAutomaticas = {}
total_estaciones = data['datosEstacion']
for DatosEstacion in total_estaciones:
    nombreEstacion = DatosEstacion['nombreEstacion']
    nombreEstacion = nombreEstacion.replace('O"Higgins', 'OHiggins')
    codigoNacional = DatosEstacion['codigoNacional']
    diccionario_estacionesAutomaticas[nombreEstacion] = codigoNacional

try:
    # Guardar el diccionario en un archivo con codificación UTF-8
    with open('listado_estaciones_automaticas.py', 'w', encoding='utf-8') as file:
        dayNow = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        file.write(f"#Fecha scaneo estaciones: {dayNow}, total Estaciones a la fecha: {len(diccionario_estacionesAutomaticas)}\n")
        file.write("diccionario_estacionesAutomaticas = {\n")
        for estacion, codigo in diccionario_estacionesAutomaticas.items():
            file.write(f'\t"{estacion}": {codigo},\n')
        file.write("}\n")
except Exception as e:
    print(f'Error al guardar el archivo: {e}')
    exit()


