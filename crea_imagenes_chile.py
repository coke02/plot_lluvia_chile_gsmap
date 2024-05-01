import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import gzip
import struct
import os

# Directorio de destino para las imagenes
img_directory = 'IMG_generadas'
txtitle = 'Hourly Rain Rate Data '

with open('estaciones_lluvia_datos.txt', 'r') as file:
    lines = file.readlines()
    latitudes = eval(lines[0].split(': ')[1])
    longitudes = eval(lines[1].split(': ')[1])

def process_file(filename):
    i=0
    rain=[0]*3600*1200
    with gzip.open(filename, "rb") as f:
        while True:
            data=f.read(4)
            if len(data) < 4:
                break
            rain[i]=struct.unpack('f',data)[0]
            i=i+1
        hprecipRateGC=np.reshape(rain, (1200,3600))

    Lon = np.linspace(0.05, 359.95, 3600)
    Lat = np.linspace(59.95, -59.95, 1200)
    #titulo
    title =  txtitle, os.path.splitext(os.path.basename(filename))[0]

    fig=plt.figure(figsize=(6,8))
    interval=list(np.arange(1,30,1))
    interval.insert(0,0.1)
    cmap=cm.jet
    cmap.set_under('w', alpha=0)

    m=Basemap(projection='cyl',
    resolution='i',
    llcrnrlat=-59.45, urcrnrlat=-15.78, llcrnrlon=-95.92, urcrnrlon=-56.78) #Chile
    m.drawmeridians(np.arange(0, 360, 10), labels=[True,False,False,True])
    m.drawparallels(np.arange(-90, 90, 10), labels=[True,False,False,True])
    m.drawcoastlines(linewidth=0.1, color='gray')
    m.drawcountries(linewidth=0.3, color='black')
    m.drawmapboundary(fill_color='#b8f7fc')
    m.fillcontinents(color='#a17c5c',lake_color='#b8f7fc')
    plt.title(title)
    Lon_adjusted = np.where(Lon > 180, Lon - 360, Lon)
    Lon_adjusted_mesh, Lat_mesh = np.meshgrid(Lon_adjusted, Lat)

    x, y = m(Lon_adjusted_mesh, Lat_mesh)
    im = m.pcolormesh(x, y, hprecipRateGC, cmap=cmap, vmin=interval[0], vmax=interval[-1], latlon=True)

    cb = m.colorbar(im, "right", size="2.5%")

    # Convertir las longitudes si es necesario
    longitudes_adjusted = np.where(np.array(longitudes) > 180, np.array(longitudes) - 360, longitudes)

    # Dibujar cada estación en el mapa
    for lat, lon in zip(latitudes, longitudes_adjusted):
        xpt, ypt = m(lon, lat)
        m.plot(xpt, ypt, 'ro',  markersize=2)  # 'ro' significa marcador rojo en forma de círculo


    output_filename = os.path.splitext(os.path.basename(filename))[0] + '.png'
    output_filename = os.path.join(img_directory, output_filename)
    print("Guardando imagen:", output_filename)
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Procesar todos los archivos en el directorio 'Descarga_Datos'
data_directory = 'Descarga_Datos'
for file in os.listdir(data_directory):
    if file.endswith('.dat.gz'):
        process_file(os.path.join(data_directory, file))