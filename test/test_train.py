# test_train.py
# Este archivo contendrá pruebas unitarias para verificar las funciones de src/train.py.
# Probará el flujo completo de entrenamiento de la CNN con MNIST.

# Importar las funciones a probar
from src.train import cargar_datos, crear_modelo, compilar_modelo, entrenar_modelo, guardar_modelo

def test_entrenamiento_completo():
    # 1. Cargar los datos
    X_train, y_train, X_test, y_test = cargar_datos()
    
    # 2. Crear y compilar el modelo
    model = crear_modelo()
    model = compilar_modelo(model)
    
    # 3. Entrenar el modelo
    history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
    
    # 4. Guardar el modelo
    guardar_modelo(model)
    
    # 5. Verificación (pendiente de implementación)
    # - Comprobar que el modelo se guarda en models/modelo_digitos.h5
    # - Verificar que las curvas de pérdida y precisión se muestren