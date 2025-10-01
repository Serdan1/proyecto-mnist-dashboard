# predict.py
# Este archivo contendrá las funciones para predecir dígitos manuscritos en imágenes
# utilizando un modelo CNN entrenado (cargado desde models/modelo_digitos.h5).
# Procesará imágenes de Paint (redimensionar, escala de grises, normalizar) y devolverá
# el dígito predicho. Será llamado desde main.py. Basado en los apuntes de clase
# (Temario.pdf, páginas 9-17).

# Planificación de funciones y flujo:
# 1. cargar_modelo(): Carga el modelo entrenado desde 'models/modelo_digitos.h5'.
#    - Verifica que el modelo exista y sea válido.
# 2. preprocesar_imagen(): Convierte una imagen de Paint en un formato usable por la CNN.
#    - Redimensiona a 28x28 píxeles.
#    - Convierte a escala de grises (1 canal).
#    - Normaliza píxeles (0-255 a 0-1).
#    - Invierte colores si es necesario (dígito blanco sobre fondo negro).
#    - Devuelve la imagen en forma (1, 28, 28, 1).
# 3. predecir_digito(): Usa el modelo cargado para predecir el dígito en una imagen preprocesada.
#    - Devuelve el dígito con mayor probabilidad (0-9) y las probabilidades de cada clase.
# 4. validar_prediccion(): Opcional, verifica si la predicción es razonable (ej. umbral de confianza).

import tensorflow as tf
from PIL import Image
import numpy as np

def cargar_modelo():
    # Cargar el modelo entrenado desde 'models/modelo_digitos.h5'
    model = tf.keras.models.load_model('models/modelo_digitos.h5')
    return model

def preprocesar_imagen(ruta_imagen):
    # Cargar la imagen desde la ruta
    img = Image.open(ruta_imagen).convert('L')  # Convertir a escala de grises
    
    # Convertir a array para análisis
    img_array = np.array(img)
    
    # Encontrar el recorte basado en el contenido (asumiendo fondo negro)
    coords = np.where(img_array < 255)  # Píxeles no blancos (dígito)
    if len(coords[0]) > 0:  # Si hay píxeles del dígito
        y_min, y_max = coords[0].min(), coords[0].max()
        x_min, x_max = coords[1].min(), coords[1].max()
        # Añadir un margen pequeño
        margin = 2
        y_min = max(0, y_min - margin)
        y_max = min(img_array.shape[0], y_max + margin)
        x_min = max(0, x_min - margin)
        x_max = min(img_array.shape[1], x_max + margin)
        # Recortar la imagen
        img = img.crop((x_min, y_min, x_max, y_max))
    
    # Redimensionar a 28x28 píxeles
    img = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    # Convertir a array numpy y normalizar (0-255 a 0-1)
    img_array = np.array(img) / 255.0
    
    # Reshape a (1, 28, 28, 1) para la CNN
    img_array = img_array.reshape(1, 28, 28, 1)
    
    return img_array

def predecir_digito(ruta_imagen):
    # Cargar el modelo
    model = cargar_modelo()
    
    # Preprocesar la imagen
    img_array = preprocesar_imagen(ruta_imagen)
    
    # Predecir el dígito
    prediccion = model.predict(img_array)
    digito = int(np.argmax(prediccion))  # Convertir a int de Python
    probabilidades = prediccion[0]  # Probabilidades de cada clase (0-9)
    
    # Validar la confianza de la predicción con manejo de error
    try:
        validar_prediccion(probabilidades)
    except ValueError as e:
        print(f"Advertencia: {e}. Devolviendo -1 como dígito por defecto.")
        digito = -1
    
    return digito, probabilidades

def validar_prediccion(probabilidades, umbral=0.5):
    # Validar que la probabilidad del dígito predicho supere el umbral
    digito_predicho = np.argmax(probabilidades)
    confianza = probabilidades[digito_predicho]
    if confianza < umbral:
        raise ValueError(f"Confianza insuficiente: {confianza:.2f} < {umbral}. Predicción poco fiable.")
    return True