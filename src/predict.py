# predict.py
# Este archivo contendrá las funciones para predecir dígitos manuscritos en imágenes
# utilizando un modelo CNN entrenado (cargado desde models/modelo_digitos.h5).
# Procesará imágenes de Paint (redimensionar, escala de grises, normalizar) y devolverá
# el dígito predicho. Será llamado desde main.py. 

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