import os
import hashlib

# encontrar archivos duplicados
'''
El script muestra un lista de archivos duplicados (mismo nombre final) de la carpeta indicada
Nota: Este script no se encarga de organizar o eliminar los archivos ya existentes || 
Solo se encarga de maper los archivos duplicados
'''

def encontrar_duplicados(carpeta):
    hash_archivos = {}
    duplicados = []
    for carpeta_actual, subcarpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_archivo = os.path.join(carpeta_actual, archivo)
            hash_archivo = hashlib.md5(open(ruta_archivo, 'rb').read()).hexdigest()
            if hash_archivo not in hash_archivos:
                hash_archivos[hash_archivo] = ruta_archivo
            else:
                duplicados.append((ruta_archivo, hash_archivos[hash_archivo]))
    return duplicados

# indicar la ruta de la carpeta a organizar
duplicados = encontrar_duplicados('C:/Users/risse/Downloads')
for duplicado in duplicados:
    print(duplicado)
    print('-----------------------------------------')