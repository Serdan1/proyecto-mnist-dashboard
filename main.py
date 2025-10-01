# main.py
# Este archivo es el punto de entrada principal del sistema. Orquestará la ejecución de todas las
# funcionalidades: entrenamiento de la CNN, predicción de dígitos, interfaz gráfica (dashboard),
# y subida de imágenes a Firebase Storage. Llamará a funciones y clases definidas en otros
# archivos (src/train.py, src/predict.py, src/dashboard.py, etc.).

from src.train import cargar_datos, crear_modelo, compilar_modelo, entrenar_modelo, guardar_modelo
from src.dashboard import manejar_drop, mostrar_resultado, subir_a_firebase

def main():
    # Entrenamiento (opcional, si el modelo no existe)
    try:
        X_train, y_train, X_test, y_test = cargar_datos()
        model = crear_modelo()
        model = compilar_modelo(model)
        history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
        guardar_modelo(model)
        print("Entrenamiento completado y modelo guardado.")
    except FileExistsError:
        print("Usando modelo existente: models/modelo_digitos.h5")

    # Orquestar predicción y subida con una imagen de prueba
    ruta_imagen = 'images/images_digito_1.png'
    try:
        # Simular el manejo de drop
        digito, probabilidades = manejar_drop(ruta_imagen)
        mostrar_resultado(digito, probabilidades)
        url_firebase = subir_a_firebase(ruta_imagen, digito)
        print(f"Imagen subida con éxito. URL: {url_firebase}")
    except Exception as e:
        print(f"Error en la orquestación: {e}")

if __name__ == "__main__":
    main()