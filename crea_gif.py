# Importar librerías
import os
import imageio.v3
import pytz
from datetime import datetime, timedelta

utc_zone = pytz.utc
local_zone = pytz.timezone('Chile/Continental')

now = datetime.now()
dayHour = now.strftime("%d-%m-%Y %H-%M-%S")

# Ubicación de la base de datos
path = 'IMG_generadas/'
archivos = sorted(os.listdir(path))
img_array = []

# Leer todos los archivos formato imagen desde path
for x in range(0, len(archivos)):
    nomArchivo = archivos[x]
    dirArchivo = path + str(nomArchivo)
    print(dirArchivo)

    # Asignar a variable leer_imagen, el nombre de cada imagen
    leer_imagen = imageio.imread(dirArchivo)

    # añadir imágenes al arreglo img_array
    img_array.append(leer_imagen)

# Guardar Gif con loop infinito y duración de fotograma de 0.8 == duration=800 segundos
imageio.mimwrite(f'salida_chile_estaciones_{dayHour}.gif', img_array, 'GIF', duration=800, loop=0)