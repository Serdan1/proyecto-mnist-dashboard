# dashboard.py
# Este archivo contendrá la lógica para crear una interfaz gráfica (dashboard) con Tkinter
# que permita arrastrar y soltar imágenes de dígitos dibujados en Paint. Integrará la
# predicción de dígitos (llamando a funciones de predict.py) y subirá las imágenes a
# Firebase Storage (usando credenciales de config/firebase-credentials.json).
# Será orquestado desde main.py. Basado en los apuntes de clase (Temario.pdf).

# Planificación de funciones y flujo:
# 1. iniciar_interfaz(): Configura la ventana principal de Tkinter con soporte para drag-and-drop.
# 2. manejar_drop(): Procesa la imagen arrastrada o cargada.
# 3. mostrar_resultado(): Actualiza la interfaz con el dígito predicho.
# 4. subir_a_firebase(): Sube la imagen original a Firebase Storage y devuelve la URL pública.

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import *  # Importar tkinterdnd2
from tkinterdnd2 import TkinterDnD  # Asegurar la inicialización
from src.predict import preprocesar_imagen, predecir_digito
import time
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np

# Definición de subir_a_firebase antes de usarla
def subir_a_firebase(ruta_imagen, digito):
    timestamp = time.strftime("%Y%m%d_%H%M")
    nombre_archivo = f"digito_{digito}_{timestamp}.png"
    print(f"Subiendo {ruta_imagen} como {nombre_archivo} a Firebase Storage...")
    bucket = storage.bucket(name="proyecto-mnist-dashboard.firebasestorage.app")
    blob = bucket.blob(nombre_archivo)
    blob.upload_from_filename(ruta_imagen)
    blob.make_public()
    url = blob.public_url
    print(f"URL generada: {url}")
    return url

print("Iniciando script dashboard.py")  # Depuración inicial

# Ajustar el path al inicio con una ruta relativa al proyecto
project_root = os.path.dirname(os.path.dirname(__file__))
print(f"Project root: {project_root}")  # Depuración
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print("Path ajustado")

try:
    # Inicializar Firebase con el bucket correcto
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'firebase-credentials.json')
    print(f"Buscando credenciales en: {cred_path}")  # Depuración
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Archivo no encontrado: {cred_path}")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {"storageBucket": "proyecto-mnist-dashboard.firebasestorage.app"})
    print("Firebase inicializado correctamente")
except Exception as e:
    print(f"Error al inicializar Firebase: {e}")
    sys.exit(1)

def iniciar_interfaz():
    try:
        ventana = TkinterDnD.Tk()
        print("Ventana creada con soporte TkinterDnD")
        ventana.title("Reconocedor de Dígitos")
        ventana.geometry("400x300")

        instruccion = tk.Label(ventana, text="Arrastra una imagen o usa el botón para cargarla")
        instruccion.pack(pady=10)
        print("Instrucción empaquetada")

        area_drop = tk.Label(ventana, text="Suelta la imagen aquí", bg="lightgray", width=40, height=15)
        area_drop.pack(pady=20)
        print("Área de drop empaquetada")

        def drop(event):
            print(f"Evento de drop detectado: {event.data}")  # Depuración
            ruta_imagen = event.data
            if os.path.isfile(ruta_imagen):
                procesar_imagen(ruta_imagen)
            else:
                print(f"Ruta inválida: {ruta_imagen}")

        area_drop.drop_target_register(DND_FILES)
        area_drop.dnd_bind('<<Drop>>', drop)
        print("Área de drop configurada")

        def procesar_imagen(ruta_imagen):
            try:
                digito, probabilidades = manejar_drop(ruta_imagen)
                if digito is not None and np.max(probabilidades) >= 0.2:  # Umbral reducido a 0.2
                    mostrar_resultado(digito, probabilidades, area_drop)
                    url = subir_a_firebase(ruta_imagen, digito)
                    mostrar_resultado_url(url, area_drop)
                else:
                    area_drop.config(text="Confianza insuficiente. Intenta otra imagen.")
                    print("Predicción descartada por baja confianza")
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar: {e}")

        boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=lambda: cargar_imagen(procesar_imagen))
        print("Botón creado")
        boton_cargar.pack(pady=10)
        print("Botón empaquetado")

        print("Iniciando mainloop")
        ventana.mainloop()
    except Exception as e:
        print(f"Error al iniciar la interfaz: {e}")
        sys.exit(1)

def cargar_imagen(procesar_func):
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if ruta_imagen:
        procesar_func(ruta_imagen)

def manejar_drop(ruta_imagen):
    try:
        img_array = preprocesar_imagen(ruta_imagen)
        digito, probabilidades = predecir_digito(ruta_imagen)
        print(f"Predicción para {ruta_imagen}: Dígito = {digito}, Probabilidades = {probabilidades}")
        return digito, probabilidades
    except Exception as e:
        print(f"Error al procesar la imagen {ruta_imagen}: {e}")
        return None, None

def mostrar_resultado(digito, probabilidades, area):
    if digito is not None and probabilidades is not None:
        resultado_texto = f"Número: {digito}, Confianza: {np.max(probabilidades):.2f}"
        area.config(text=resultado_texto)
        print(f"Resultado preparado: {resultado_texto}")
    else:
        area.config(text="Error en la predicción")

def mostrar_resultado_url(url, area):
    if url:
        area.config(text=f"URL: {url}")
        print(f"URL mostrada: {url}")
    else:
        area.config(text="Error al subir la imagen")

if __name__ == "__main__":
    print("Entrando al main")
    iniciar_interfaz()