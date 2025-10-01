# train.py
# Este script será usado para entrenar una Red Neuronal Convolucional (CNN) con el dataset MNIST
# para reconocer dígitos manuscritos (0-9). Utilizará TensorFlow/Keras y guardará el modelo
# en la carpeta 'models/' como modelo_digitos.h5. Basado en los apuntes de clase (Temario.pdf,
# páginas 9-17).

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

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

def cargar_datos():
    # Cargar el dataset MNIST
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    # Normalizar píxeles (0-255 a 0-1)
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    
    # Reshape a (muestras, 28, 28, 1) para CNN
    X_train = X_train.reshape(-1, 28, 28, 1)
    X_test = X_test.reshape(-1, 28, 28, 1)
    
    # Convertir etiquetas a one-hot encoding (10 clases)
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    
    return X_train, y_train, X_test, y_test

def crear_modelo():
    # Crear la arquitectura de la CNN
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, (5, 5), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(36, (5, 5), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    return model

def compilar_modelo(model):
    # Compilar el modelo con optimizador, pérdida y métricas
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def entrenar_modelo(model, X_train, y_train, X_test, y_test):
    # Entrenar el modelo con los datos
    history = model.fit(X_train, y_train,
                        epochs=3,
                        batch_size=1000,
                        validation_data=(X_test, y_test))
    
    # Mostrar curvas de pérdida y precisión
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Pérdida (Loss)')
    plt.xlabel('Épocas')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'], label='Val Acc')
    plt.title('Precisión (Accuracy)')
    plt.xlabel('Épocas')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    
    return history

def guardar_modelo(model):
    # Guardar el modelo entrenado en la carpeta 'models/'
    model.save('models/modelo_digitos.h5')
    print("Modelo guardado como models/modelo_digitos.h5")

