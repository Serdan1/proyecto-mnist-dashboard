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
from tkinter import filedialog, messagebox
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
firebase_admin.initialize_app(cred, {"storageBucket": "proyecto-mnist-dashboard.firebasestorage.app"})

def iniciar_interfaz():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Reconocedor de Dígitos")
    ventana.geometry("400x300")

    # Etiqueta para instrucciones
    instruccion = tk.Label(ventana, text="Arrastra una imagen o usa el botón para cargarla")
    instruccion.pack(pady=10)

    # Área para soltar imágenes con soporte básico
    area_drop = tk.Label(ventana, text="Suelta la imagen aquí", bg="lightgray", width=40, height=15)
    area_drop.pack(pady=20)

    # Función para simular drag-and-drop (placeholder en Codespaces)
    def on_drop(event):
        if event.data:
            ruta_imagen = event.data
            procesar_imagen(ruta_imagen, area_drop)

    # Simulación de drop (en Codespaces, usaremos filedialog como alternativa)
    def procesar_imagen(ruta_imagen, area):
        try:
            digito, probabilidades = manejar_drop(ruta_imagen)
            mostrar_resultado(digito, probabilidades, area)
            url = subir_a_firebase(ruta_imagen, digito)
            mostrar_resultado_url(url, area)
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar: {e}")

    # Botón para cargar imagen
    boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=lambda: cargar_imagen(area_drop))
    boton_cargar.pack(pady=10)

    # Etiqueta para resultados
    resultado = tk.Label(ventana, text="Resultado: -")
    resultado.pack(pady=10)

    # Ejecutar la ventana (deshabilitado en Codespaces por ahora)
    # ventana.mainloop()

    return ventana  # Devolver la ventana para uso externo si es necesario

def cargar_imagen(area):
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if ruta_imagen:
        procesar_imagen(ruta_imagen, area)

def manejar_drop(ruta_imagen):
    # Procesar el evento de soltar una imagen y devolver resultados
    try:
        # Preprocesar la imagen
        img_array = preprocesar_imagen(ruta_imagen)
        
        # Predecir el dígito
        digito, probabilidades = predecir_digito(ruta_imagen)
        print(f"Predicción para {ruta_imagen}: Dígito = {digito}, Probabilidades = {probabilidades}")
        return digito, probabilidades  # Devolver los valores para la orquestación
    except Exception as e:
        print(f"Error al procesar la imagen {ruta_imagen}: {e}")
        return None, None  # Devolver None en caso de error

def mostrar_resultado(digito, probabilidades, area):
    # Actualizar la interfaz con el dígito predicho
    if digito is not None and probabilidades is not None:
        resultado_texto = f"Número: {digito}, Confianza: {np.max(probabilidades):.2f}"
        area.config(text=resultado_texto)
        print(f"Resultado preparado: {resultado_texto}")
    else:
        area.config(text="Error en la predicción")

def mostrar_resultado_url(url, area):
    # Actualizar la interfaz con la URL de Firebase
    if url:
        area.config(text=f"URL: {url}")
        print(f"URL mostrada: {url}")
    else:
        area.config(text="Error al subir la imagen")

import numpy as np  # Añadido para np.max en mostrar_resultado

if __name__ == "__main__":
    print("Interfaz gráfica deshabilitada en Codespaces. Usa un entorno con GUI para ejecutarla.")
    # iniciar_interfaz()  # Comentar esta línea hasta que tengamos GUI
    # Ejemplo de uso de manejar_drop (para probar en Codespaces)
    manejar_drop('images/images_digito_1.png')