# dashboard.py
# Este archivo contendrá la lógica para crear una interfaz gráfica (dashboard) con Tkinter
# que permita arrastrar y soltar imágenes de dígitos dibujados en Paint. Integrará la
# predicción de dígitos (llamando a funciones de predict.py) y subirá las imágenes a
# Firebase Storage (usando credenciales de config/firebase-credentials.json).
# Será orquestado desde main.py. Basado en los apuntes de clase (Temario.pdf).

# Planificación de funciones y flujo:
# 1. iniciar_interfaz(): Configura la ventana principal de Tkinter con soporte para drag-and-drop.
#    - Define un área para soltar imágenes y un espacio para mostrar resultados.
# 2. manejar_drop(): Procesa el evento cuando se suelta una imagen en la interfaz.
#    - Carga la imagen desde la ruta arrastrada.
#    - Llama a preprocesar_imagen() y predecir_digito() desde predict.py.
# 3. mostrar_resultado(): Actualiza la interfaz con el dígito predicho y la URL de Firebase.
#    - Muestra texto o gráficos (ej. "Número: 1", "URL: [link]").
# 4. subir_a_firebase(): Sube la imagen original a Firebase Storage.
#    - Usa credenciales de config/firebase-credentials.json.
#    - Genera un nombre único (ej. digito_1_20251001_1900.png) y devuelve la URL pública.

import sys
import os
import tkinter as tk
from tkinter import filedialog
from src.predict import preprocesar_imagen, predecir_digito
import time
import firebase_admin
from firebase_admin import credentials, storage

# Ajustar el path al inicio con una ruta absoluta explícita
project_root = "/workspaces/proyecto-mnist-dashboard"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Inicializar Firebase con el bucket correcto
cred = credentials.Certificate("config/firebase-credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "proyecto-mnist-dashboard.appspot.com"})

def iniciar_interfaz():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Reconocedor de Dígitos")
    ventana.geometry("400x300")

    # Etiqueta para instrucciones
    instruccion = tk.Label(ventana, text="Arrastra una imagen o usa el botón para cargarla")
    instruccion.pack(pady=10)

    # Área para soltar imágenes (placeholder)
    area_drop = tk.Label(ventana, text="Suelta la imagen aquí", bg="lightgray", width=40, height=15)
    area_drop.pack(pady=20)

    # Botón para cargar imagen (placeholder)
    boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=lambda: filedialog.askopenfilename())
    boton_cargar.pack(pady=10)

    # Etiqueta para resultados (placeholder)
    resultado = tk.Label(ventana, text="Resultado: -")
    resultado.pack(pady=10)

    # Nota: La ventana no se ejecuta en Codespaces; usar en entorno con GUI
    # ventana.mainloop()

def manejar_drop(ruta_imagen):
    # Procesar el evento de soltar una imagen
    try:
        # Preprocesar la imagen
        img_array = preprocesar_imagen(ruta_imagen)
        
        # Predecir el dígito
        digito, probabilidades = predecir_digito(ruta_imagen)
        print(f"Predicción para {ruta_imagen}: Dígito = {digito}, Probabilidades = {probabilidades}")
        mostrar_resultado(digito, probabilidades)
        subir_a_firebase(ruta_imagen, digito)  # Llamar a subir_a_firebase
    except Exception as e:
        print(f"Error al procesar la imagen {ruta_imagen}: {e}")

def mostrar_resultado(digito, probabilidades):
    # Preparar la salida para la interfaz (placeholder)
    resultado_texto = f"Número: {digito}, Probabilidades: {probabilidades}"
    print(f"Resultado preparado: {resultado_texto}")  # Simulación de salida en consola
    # Nota: Esto se integrará con la etiqueta 'resultado' en iniciar_interfaz() en un entorno con GUI

def subir_a_firebase(ruta_imagen, digito):
    # Subir la imagen a Firebase Storage
    timestamp = time.strftime("%Y%m%d_%H%M")
    nombre_archivo = f"digito_{digito}_{timestamp}.png"
    print(f"Subiendo {ruta_imagen} como {nombre_archivo} a Firebase Storage...")
    bucket = storage.bucket()
    blob = bucket.blob(nombre_archivo)
    blob.upload_from_filename(ruta_imagen)
    url = blob.public_url
    print(f"URL generada: {url}")
    return url

if __name__ == "__main__":
    print("Interfaz gráfica deshabilitada en Codespaces. Usa un entorno con GUI para ejecutarla.")
    # iniciar_interfaz()  # Comentar esta línea hasta que tengamos GUI
    # Ejemplo de uso de manejar_drop (para probar en Codespaces)
    manejar_drop('images/images_digito_1.png')