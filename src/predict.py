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
    
    return digito, probabilidades