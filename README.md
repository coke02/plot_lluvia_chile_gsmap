Checking rainfall record at weather stations

Este proyecto extrae datos meteorológicos de fuentes gratuitas para analizar y visualizar patrones de precipitación en Chile. Utiliza datos de las siguientes fuentes, las cuales requieren registro:

    Climatología de Chile: https://climatologia.meteochile.gob.cl/
        Datos utilizados para identificar estaciones meteorológicas que registran precipitaciones diarias.
    GSMaP: https://sharaku.eorc.jaxa.jp/GSMaP/
        Acceso a archivos .dat a través de FTP.

Componentes del Proyecto
compruebaEstaciones.py

    Verifica nombres y códigos de las estaciones.
    Genera un archivo con un listado de las estaciones automáticas (listado_estaciones_automaticas.py).

mapaLLuvia_2plots.py

    Utiliza el listado actualizado de estaciones para generar dos archivos:
        Una imagen PNG (mapa_y_grafico_lluvias_<fecha_hora>.png) que muestra un mapa de Chile y un gráfico de barras con la cantidad de precipitación y nombres de estaciones.
        Un documento de texto con las coordenadas de las estaciones que registraron lluvia.

descarga_archivos.py

    Descarga los últimos 20 archivos .dat de GSMaP en la carpeta "Descarga_Datos".

crea_imagenes_chile.py

    Genera un archivo GIF que muestra el movimiento o patrones de precipitación en el cuadrante sudamericano, específicamente en Chile.

Registro y Acceso

Para acceder a los servicios y datos necesarios, es obligatorio registrarse en los sitios web mencionados anteriormente.

Uso

El proyecto se creo usando virtaulenv de python, por ahora no tiene comprobaciones rigurosas y todavia esta en desarrollo ya que el objetivo final seria integrarlo en servicios de mensajerias como "telegram"   

Las contribuciones son bienvenidas. Para contribuir, por favor clona el repositorio y crea un pull request con tus cambios.
Licencia por definir xD........

Salidas:![mapa_y_grafico_lluvias_25-04-2024 17-12-53](https://github.com/coke02/plot_lluvia_chile_gsmap/assets/25438330/8547e8f2-09be-420a-ba4c-f6ad6d31d9f7)

![salida_chile_estaciones_25-04-2024 17-21-12](https://github.com/coke02/plot_lluvia_chile_gsmap/assets/25438330/61130c3d-534a-40d6-aead-80da64011ad4)

Salida global ejemplo:

![salida_global](https://github.com/coke02/plot_lluvia_chile_gsmap/assets/25438330/08260078-6fef-4480-85a5-f1d2a96c1ce7)



