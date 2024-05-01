'''
import matplotlib
matplotlib.use('TkAgg')  # Puede usar otros backends como 'Agg', 'Qt4Agg', 'Qt5Agg', etc.
import matplotlib.pyplot as plt
['GTK3Agg', 'GTK3Cairo', 'GTK4Agg', 'GTK4Cairo', 'MacOSX', 'nbAgg', 'QtAgg', 'QtCairo', 'Qt5Agg',
'Qt5Cairo', 'TkAgg', 'TkCairo', 'WebAgg', 'WX', 'WXAgg', 'WXCairo', 'agg', 'cairo', 'pdf', 'pgf',
'ps', 'svg', 'template']
'''

import requests
import json
import pytz
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import matplotlib
matplotlib.use('agg')  # Puede usar otros backends como 'Agg', 'Qt4Agg', 'Qt5Agg', etc.
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from datetime import datetime, timedelta
import listado_estaciones_automaticas
utc_zone = pytz.utc
local_zone = pytz.timezone('Chile/Continental')

now = datetime.now()
dayHour = now.strftime("%d-%m-%Y %H-%M-%S")
ayer = now - timedelta(days=1)
estacionesAutomaticas = listado_estaciones_automaticas.diccionario_estacionesAutomaticas.values()

#key and user
api_user = ''
api_key = ''
#esto no debería estar en el código final se debe usar un archivo de configuración o usar variables de entorno

latitudes = []
longitudes = []
nombreEstacionesAguaCaida = []
aguaCaidamm = []
dayNow = datetime.now().strftime("%d-%m-%Y")
for estacion in estacionesAutomaticas:
    url = f'https://climatologia.meteochile.gob.cl/application/servicios/getEmaResumenDiario/{estacion}?usuario={api_user}&token={api_key}'

    response = requests.get(url)
    data = json.loads(response.text)

    try:
        agua_caida = round(data['datos']['aguaCaidaDiaria'][dayNow]['valor'],1)
        
    except(KeyError, TypeError, Exception ) as e:
        estacion_sin_registro_agua = f"Error: {e}"
        continue

    if agua_caida > 0:
        agua = f"{agua_caida} mm"
        try:
            codigo_Nacional = data['datosEstacion']['codigoNacional']
        except(KeyError, TypeError, Exception ) as e:
            estacion_sincodigo = f"Error: {e}"
            continue
        aguaCaidamm.append(float(agua_caida))
        #archivo.write(f"Fecha: {dayNow}\n")
        nombre_estacion = data['datosEstacion']['nombreEstacion']
        nombreEstacion_correcto = nombre_estacion.encode('latin-1').decode('utf-8')
        latitud= data['datosEstacion']['latitud']
        nombreEstacionesAguaCaida.append(nombreEstacion_correcto)
        longitud= data['datosEstacion']['longitud']
        latitudes.append(float(latitud))
        longitudes.append(float(longitud))
    else:
        #print("No llovió\n")
        nombre_estacion = data['datosEstacion']['nombreEstacion']
        nombreEstacion_correcto = nombre_estacion.encode('latin-1').decode('utf-8')
        #print(f"Nombre Estacion: {nombreEstacion_correcto}\n")
        
#print (f"cantinada de estaciones analizadas: {len(estacionesAutomaticas)}\n")
#print(f"Total estaciones con registro de lluvia para hoy: {(aguaCaidamm)}\n")
#print (f"latitudes, {latitudes})\n", f"longitudes, {longitudes}")

with open('estaciones_lluvia_datos.txt', 'w') as file:
    file.write(f"Latitudes: {latitudes}\nLongitudes: {longitudes}\n")

fig = plt.figure(figsize=(20, 15))
gs = fig.add_gridspec(1, 4)

ax1 = fig.add_subplot(gs[0:1, 0:3], projection=ccrs.PlateCarree())
# Crear un mapa usando Cartopy

ax1.set_extent([-85, -60, -70, -15]) # Limitar el mapa a Chile
#ax1.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.OCEAN)
#ax.add_feature(cfeature.COASTLINE)
ax1.add_feature(cfeature.BORDERS, linestyle=':')
ax1.add_feature(cfeature.LAKES, alpha=0.5)
ax1.add_feature(cfeature.RIVERS)

gl = ax1.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
gl.bottom_labels = True  # Habilitar las etiquetas en la parte inferior
gl.right_labels = False  # Desactivar las etiquetas en el lado derecho
gl.top_labels = False   # Desactivar las etiquetas superiores
gl.left_labels = True  # Habilitar las etiquetas izquierdas

ax1.scatter(longitudes, latitudes, color='red', s=30, marker='o', transform=ccrs.Geodetic())
ax1.set_title('Estaciones con Registro de Lluvia')

ax2 = fig.add_subplot(gs[0, 3])
ax2.barh(nombreEstacionesAguaCaida, aguaCaidamm, color='skyblue', edgecolor='black', linewidth=1.2, align='center', height=0.5)
ax2.set_xlabel('Milímetros de Agua Caída')
ax2.set_title('Precipitación por Estación')
ax2.set_xlim(0, max(aguaCaidamm) + 0.4)

fig.subplots_adjust(left=0.01, right=0.99, wspace=0.2, hspace=0.2)

plt.tight_layout()

plt.savefig(f'mapa_y_grafico_lluvias_{dayHour}.png',bbox_inches='tight')

#plt.show()


