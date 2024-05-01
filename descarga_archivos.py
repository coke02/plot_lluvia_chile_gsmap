#Cargar entorno visrtual python en window "plot_lluvia\Scripts\activate.bat"
#Caregar entorno virtual python en linux "source plot_lluvia/bin/activate"
#ruta ftp /now/latest (ruta archivo "dat.gz")
#https://www.researchgate.net/post/Visualization_of_precipitation_data_using_Python_or_R

#codigo para descargar archivos de ftp GSMap

import ftplib
import os
import re

# Datos de conexión al servidor FTP
ftp_address = ''
username = ''
password = ''
#Esto no debería estar en el código final se debe usar un archivo de configuración o usar variables de entorno

# Directorio de destino para las descargas
download_directory = 'Descarga_Datos'

# Si el directorio no existe, créalo
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Conectar al servidor FTP
ftp = ftplib.FTP(ftp_address)
ftp.login(username, password)

# Cambiar al directorio correcto
ftp.cwd('/now/latest')

# Obtener la lista de archivos
files = ftp.nlst()

# Utilizar expresión regular para filtrar los archivos requeridos
pattern = re.compile(r'gsmap_now.\d{8}.\d{4}.dat.gz')
filtered_files = [file for file in files if pattern.match(file)]

# Ordenar la lista y tomar los últimos 5 archivos
filtered_files.sort()
last_five_files = filtered_files[-20:]

# Descargar los archivos
for filename in last_five_files:
    local_filepath = os.path.join(download_directory, filename)
    with open(local_filepath, 'wb') as local_file:
        ftp.retrbinary('RETR ' + filename, local_file.write)

# Cerrar la conexión FTP
ftp.quit()

print("Descarga completada. Archivos guardados en:", download_directory)