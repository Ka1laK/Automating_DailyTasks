import os
import time
import subprocess


def verificar_descargas(directorio, intervalo):
    """
    Verifica si hay archivos descargandose en la carpeta de descargas y apaga la PC si no hay descargas activas
    
    - Revisa el directorio especificado cada cierto intervalo
    - Si el directorio esta vacio, cierra aplicaciones activas y apaga el sistema
    
    Parametros:
        directorio: Ruta de la carpeta de descargas
        intervalo: Tiempo (en segundos) entre verificaciones
    """
    directorio = 'C:/Users/risse/Downloads'
    intervalo = 60
    try:
        while True:
            # verificar si la carpeta de descargas esta vacia
            if not os.listdir(directorio):
                print("No se detectaron descargas activas. Cerrando aplicaciones...")
                
                # cierra las aplicaciones activas (modifica esta lista si es necesario)
                aplicaciones_a_cerrar = ['notepad.exe', 'chrome.exe', 'spotify.exe']
                for app in aplicaciones_a_cerrar:
                    subprocess.call(f'taskkill /F /IM {app}', shell=True)
                
                print("Apagando el sistema...")
                os.system('shutdown /s /t 1')
                break

            else:
                print(f"Descargas activas detectadas en '{directorio}'. Verificando nuevamente en {intervalo} segundos")
            
            time.sleep(intervalo)
    
    except FileNotFoundError:
        print(f"Error: La carpeta '{directorio}' no existe. Verifica la ruta e intenta nuevamente")
    except PermissionError:
        print("Error: Permisos insuficientes para acceder al directorio o cerrar aplicaciones")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


if __name__ == "__main__":
    verificar_descargas()
