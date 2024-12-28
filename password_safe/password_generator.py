import random
import re

def generador_password(tamanio):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]{}|;:,.<>?/"
    password = ""
    for i in range(tamanio):
        password += random.choice(caracteres)
    return password

def evaluar_password(password):
    puntaje = 0
    longitud = len(password)
    tiene_minusculas = bool(re.search(r'[a-z]', password))
    tiene_mayusculas = bool(re.search(r'[A-Z]', password))
    tiene_digitos = bool(re.search(r'[0-9]', password))
    tiene_simbolos = bool(re.search(r'[!@#$%^&*()_+-=[\]{}|;:,.<>?/]', password))

    if longitud >= 12:
        puntaje += 2
    elif longitud >= 8:
        puntaje += 1

    if tiene_minusculas:
        puntaje += 1
    if tiene_mayusculas:
        puntaje += 1
    if tiene_digitos:
        puntaje += 1
    if tiene_simbolos:
        puntaje += 1

    if puntaje >= 4:
        return "Fuerte"
    elif puntaje >= 3:
        return "Moderada"
    else:
        return "Debil"


contrasenia_segura = generador_password(16)
vida = evaluar_password(contrasenia_segura)



print(f"Contrasenia generada: {contrasenia_segura}")
print(f"Fortaleza de la contrasenia: {vida}")