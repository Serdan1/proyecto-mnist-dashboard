# main.py
# Este archivo es el punto de entrada principal del sistema. Orquestará la ejecución de todas las
# funcionalidades: entrenamiento de la CNN, predicción de dígitos, interfaz gráfica (dashboard),
# y subida de imágenes a Firebase Storage. Llamará a funciones y clases definidas en otros
# archivos (src/train.py, src/predict.py, src/dashboard.py, etc.).

import numpy as np
from src.train import cargar_datos, crear_modelo, compilar_modelo, entrenar_modelo, guardar_modelo
from src.predict import predecir_digito, validar_prediccion

def main():
    # Entrenamiento (opcional, si el modelo no existe)
    X_train, y_train, X_test, y_test = cargar_datos()
    model = crear_modelo()
    model = compilar_modelo(model)
    history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
    guardar_modelo(model)
    print("Entrenamiento completado y modelo guardado.")

    # Predicción con una imagen de prueba
    ruta_imagen = 'images/images_digito_1.png'
    digito, probabilidades = predecir_digito(ruta_imagen)
    confianza = probabilidades[np.argmax(probabilidades)]  # Confianza del dígito predicho
    print(f"Predicción: Dígito = {digito}, Confianza = {confianza:.2f}, Probabilidades = {probabilidades}")

if __name__ == "__main__":
    main()