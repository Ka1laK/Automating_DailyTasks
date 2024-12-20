#NOTA:
# Ejecutar este comando en la terminal para instalar la libreria pytss3
# pip install pyttsx3 tkinter PyPDF2 docx2txt
import pyttsx3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PyPDF2
import docx2txt
import re
import threading

# Variables globales
engine = pyttsx3.init()
pausado = False
index_actual = 0
palabra_actual = 0 
texto_frases = []
thread = None
lock = threading.Lock()



def configurar_engine(idioma, velocidad):
    """configuracion del motor de texto a voz"""
    if idioma == "Español":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0')
    elif idioma == "Ingles":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
    engine.setProperty('rate', max(100, min(velocidad, 200)))
    engine.setProperty('volume', 1.0)



def convertir_texto_voz():
    global pausado, index_actual, texto_frases, thread

    if thread and thread.is_alive():
        messagebox.showwarning("Advertencia", "El motor ya en progreso (leyendo ... )")
        return

    texto = entrada_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Advertencia", "El campo de texto esta vacio.")
        return

    idioma = combo_idioma.get()
    velocidad = escala_velocidad.get()

    configurar_engine(idioma, velocidad)
    texto_frases = dividir_texto2frases(texto)
    pausado = False
    index_actual = 0

    thread = threading.Thread(target=leer_frases)
    thread.start()


def leer_frases():
    """lee las frases del texto, manteniendo el progreso en palabras"""
    global pausado, index_actual, palabra_actual, texto_frases

    while index_actual < len(texto_frases):
        frase = texto_frases[index_actual]
        palabras = frase.split()
        total_palabras = len(palabras)

        while palabra_actual < total_palabras:
            with lock:
                if pausado:
                    return

            palabra = palabras[palabra_actual:]
            frase_restante = " ".join(palabra)

            resaltar_frase(frase_restante)
            engine.say(frase_restante)
            engine.runAndWait()
            palabra_actual = total_palabras
        palabra_actual = 0
        index_actual += 1


def dividir_texto2frases(texto):
    """divide el texto en frases usando expresiones regulares"""
    oraciones = re.split(r'(?<=[.!?])\s+', texto)
    return oraciones


def resaltar_frase(frase):
    """resalta la frase actual en el campo de texto"""
    limpiar_resaltado()
    start_idx = entrada_texto.search(frase, "1.0", tk.END)
    if start_idx:
        end_idx = f"{start_idx}+{len(frase)}c"
        entrada_texto.tag_add("highlight", start_idx, end_idx)
        entrada_texto.tag_configure("highlight", background="yellow")


def limpiar_resaltado():
    """elimina el resaltado en el texto despues de ser leida"""
    entrada_texto.tag_remove("highlight", "1.0", tk.END)


def guardar_audio():
    texto = entrada_texto.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Advertencia", "El campo de texto esta vacío.")
        return

    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")]
    )
    if ruta_archivo:
        configurar_engine(combo_idioma.get(), escala_velocidad.get())
        engine.save_to_file(texto, ruta_archivo)
        engine.runAndWait()
        messagebox.showinfo("Exito", "Audio guardado correctamente...")


def toggle_pausa():
    global pausado, thread

    with lock:
        pausado = not pausado
    if not pausado:
        thread = threading.Thread(target=leer_frases)
        thread.start()



def subir_archivo():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos PDF", "*.pdf"), ("Archivos Word", "*.docx"), ("Archivos TXT", "*.txt")]
    )
    if ruta_archivo:
        if ruta_archivo.endswith(".pdf"):
            texto = leer_pdf(ruta_archivo)
        elif ruta_archivo.endswith(".docx"):
            texto = leer_word(ruta_archivo)
        elif ruta_archivo.endswith(".txt"):
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                texto = file.read()
        else:
            texto = "Formato de archivo no soportado"

        entrada_texto.delete("1.0", tk.END)
        entrada_texto.insert(tk.END, texto)


def leer_pdf(ruta_archivo):
    texto = ""
    with open(ruta_archivo, 'rb') as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        for pagina in lector_pdf.pages:
            texto += pagina.extract_text()
    return texto


def leer_word(ruta_archivo):
    return docx2txt.process(ruta_archivo)


# Interfaz grafica
root = tk.Tk()
root.title("Convertidor de Texto a Voz")

etiqueta_texto = tk.Label(root, text="Ingrese el texto (máximo 100000 caracteres):")
etiqueta_texto.pack()

entrada_texto = tk.Text(root, height=10, width=50, wrap=tk.WORD)
entrada_texto.pack()

boton_subir = tk.Button(root, text="Subir archivo (PDF, Word o TXT)", command=subir_archivo)
boton_subir.pack()

etiqueta_idioma = tk.Label(root, text="Seleccione el idioma:")
etiqueta_idioma.pack()

combo_idioma = ttk.Combobox(root, values=["Español", "Ingles"])
combo_idioma.set("Español")
combo_idioma.pack()

etiqueta_velocidad = tk.Label(root, text="Seleccione la velocidad de la voz:")
etiqueta_velocidad.pack()

escala_velocidad = tk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL)
escala_velocidad.set(150)
escala_velocidad.pack()

boton_convertir = tk.Button(root, text="Convertir a Voz", command=convertir_texto_voz)
boton_convertir.pack()

boton_pausar = tk.Button(root, text="Pausar/Reanudar", command=toggle_pausa)
boton_pausar.pack()

boton_guardar = tk.Button(root, text="Guardar Audio", command=guardar_audio)
boton_guardar.pack()

root.mainloop()
