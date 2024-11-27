import os
import shutil

def organizador_carpetas(carpeta):
    tipos_archivos = {
        'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'Videos': ['.mp4', '.avi', '.mkv', '.webm', '.flv', '.3gp'],
        'Audios': ['.mp3', '.wav', '.flac', '.ogg', '.wma'],
        'Documentos': ['.pdf', '.doc', '.docx', '.csv', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz', '.tgz'],
        'Ejecutables': ['.exe', '.msi'],
        'Programas': ['.deb', '.rpm', '.apk'],
        'Fuentes': ['.ttf', '.otf', '.fon'],
        'Archivos': ['.iso', '.img', '.bin', '.jar'],
        'Presentaciones': ['.pps', '.pptx'],
        'Plantillas': ['.potx', '.potm'],
        'Archivos de texto': ['.txt'],
        'Archivos de programacion': ['.cpp'],
        'Archivos de Power BI': ['.pbix'],
        'Archivos de SQL': ['.sql'],
        'Archivos de Cisco Packet Tracer': ['.pkt'],
        'Otros': []
    }

    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)

        if os.path.isfile(ruta_archivo):
            extension = os.path.splitext(archivo)[1].lower()
            movido = False
            for carpeta_tipo, extensiones in tipos_archivos.items():
                if extension in extensiones:
                    carpeta_destino = os.path.join(carpeta, carpeta_tipo)
                    os.makedirs(carpeta_destino, exist_ok=True)
                    shutil.move(ruta_archivo, os.path.join(carpeta_destino, archivo))
                    movido = True
                    break
        
    if not movido:
        carpeta_otros = os.path.join(carpeta, 'Otros')
        os.makedirs(carpeta_destino, exist_ok=True)
        shutil.move(ruta_archivo, os.path.join(carpeta_otros, archivo))
    
    print('Organizacion de carpetas finalizada')


'''
El script organizara los archivos de la carpeta segun su extension en subcarpetas
Imagenes, Videos, Audios, Documentos, Comprimidos, Ejecutables, Programas, entre otros
Nota: Este script no se encarga de organizar las carpetas ya existentes || 
Usted puede modificar la cantidad de extensiones y carpetas segun sus necesidades 
'''

organizador_carpetas('C:/Users/risse/Downloads')
