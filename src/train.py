# train.py
# Este script será usado para entrenar una Red Neuronal Convolucional (CNN) con el dataset MNIST
# para reconocer dígitos manuscritos (0-9). Utilizará TensorFlow/Keras y guardará el modelo
# en la carpeta 'models/' como modelo_digitos.h5. 

# Planificación de funciones y flujo:
# 1. cargar_datos(): Carga el dataset MNIST y lo divide en entrenamiento y prueba.
#    - Normaliza los píxeles (0-255 a 0-1) y reshape a (28, 28, 1).
#    - Convierte etiquetas a one-hot encoding (10 clases).
# 2. crear_modelo(): Define la arquitectura de la CNN.
#    - Capas convolucionales (Conv2D) con filtros (ej. 16, 36) y activación ReLU.
#    - Capas de pooling (MaxPooling2D) para reducir dimensiones.
#    - Capas densas (Dense) con salida softmax para 10 dígitos.
# 3. compilar_modelo(): Configura el modelo con optimizador (Adam), pérdida (categorical_crossentropy),
#    y métrica (accuracy).
# 4. entrenar_modelo(): Entrena la CNN con los datos, usando épocas (ej. 3-5) y batch_size (ej. 1000).
#    - Muestra curvas de pérdida (loss) y precisión (accuracy) con matplotlib.
# 5. guardar_modelo(): Guarda el modelo entrenado en 'models/modelo_digitos.h5'.
#    - Verifica que se guarde correctamente.