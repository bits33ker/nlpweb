# Demo NLP para Gustavo.
La demo consiste en varias sub paginas que muestran distintos artchivos en espanol y su consiguiente analisis.
https://www.youtube.com/watch?v=vs6dXL9Wp7s&list=RDCMUC1mxuk7tuQT2D0qTMgKji3w&index=2

## Run:
'''
django-admin startproject locallibrary: Crea directorio y website para visualizacion
python3 manage.py startapp catalog: Crea la app para el manejo del modelo.
 python3 manage.py createsuperuser: Crea usuario admin como superuser.
    Usuario: admin
    passw: admin    
python3 manage.py runserver
'''


## SQlite:
'''
.import audios.csv textos_audio: importa el csv.

.schema textos_audio: muestra la forma de la tabla.

select count(dinstinct name) from textos_audio: Cuenta la cantidad de archivos de audio distintos.
'''