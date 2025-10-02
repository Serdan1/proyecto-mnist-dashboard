# predict.py
# Este archivo contendrá las funciones para predecir dígitos a partir de imágenes usando un modelo
# de CNN entrenado previamente. Basado en los apuntes de clase (Temario.pdf).

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import os

# Cargar el modelo entrenado
def cargar_modelo():
    modelo_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_digitos.h5')
    modelo = load_model(modelo_path)
    return modelo

# Preprocesar la imagen
def preprocesar_imagen(ruta_imagen):
    # Abrir y convertir la imagen a escala de grises
    img = Image.open(ruta_imagen).convert('L')
    # Redimensionar a 28x28 (tamaño estándar de MNIST)
    img = img.resize((28, 28), Image.LANCZOS)
    # Convertir a array y normalizar
    img_array = np.array(img) / 255.0
    # Redimensionar para que coincida con la entrada del modelo (1, 28, 28, 1)
    img_array = img_array.reshape(1, 28, 28, 1)
    return img_array

# Predecir el dígito
def predecir_digito(ruta_imagen):
    modelo = cargar_modelo()
    img_array = preprocesar_imagen(ruta_imagen)
    # Obtener las probabilidades
    probabilidades = modelo.predict(img_array)
    # Obtener el dígito con mayor probabilidad
    digito = np.argmax(probabilidades[0])
    # Verificar la confianza (ajustamos el umbral a 0.3)
    confianza = np.max(probabilidades[0])
    if confianza < 0.3:  # Umbral reducido a 0.3
        print(f"Advertencia: Confianza insuficiente: {confianza:.2f} < 0.3. Predicción poco fiable. Devolviendo -1 como dígito por defecto.")
        digito = -1
    return digito, probabilidades[0]

if __name__ == "__main__":
    # Ejemplo de uso
    ruta_imagen = os.path.join(os.path.dirname(__file__), '..', 'images', 'images_digito_1.png')
    digito, probabilidades = predecir_digito(ruta_imagen)
    print(f"Dígito predicho: {digito}, Probabilidades: {probabilidades}")