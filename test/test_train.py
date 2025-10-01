# test_train.py
# Este archivo contendrá pruebas unitarias para verificar las funciones de src/train.py.
# Probará el flujo completo de entrenamiento de la CNN con MNIST.

import unittest
from src.train import cargar_datos, crear_modelo, compilar_modelo, entrenar_modelo, guardar_modelo

class TestTrainFunctions(unittest.TestCase):
    def test_cargar_datos(self):
        # Prueba que cargar_datos() devuelva datos con las formas esperadas
        X_train, y_train, X_test, y_test = cargar_datos()
        self.assertEqual(X_train.shape[1:], (28, 28, 1))  # Forma de cada imagen
        self.assertEqual(y_train.shape[1], 10)  # One-hot encoding para 10 clases
        self.assertEqual(len(X_train), len(y_train))  # Igual número de imágenes y etiquetas
        self.assertEqual(len(X_test), len(y_test))

    def test_crear_modelo(self):
        # Prueba que crear_modelo() devuelva un modelo válido
        model = crear_modelo()
        self.assertIsNotNone(model)  # Verifica que no sea None
        self.assertEqual(model.input_shape, (None, 28, 28, 1))  # Forma de entrada esperada

    def test_compilar_modelo(self):
        # Prueba que compilar_modelo() configure el modelo correctamente
        model = crear_modelo()
        compiled_model = compilar_modelo(model)
        self.assertIsNotNone(compiled_model.optimizer)  # Verifica que tenga optimizador
        self.assertEqual(compiled_model.loss, 'categorical_crossentropy')

    def test_entrenar_modelo(self):
        # Prueba que entrenar_modelo() devuelva un historial
        X_train, y_train, X_test, y_test = cargar_datos()
        model = crear_modelo()
        model = compilar_modelo(model)
        history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
        self.assertIn('loss', history.history)  # Verifica que devuelva historial con loss
        self.assertIn('accuracy', history.history)

    def test_guardar_modelo(self):
        # Prueba que guardar_modelo() no falle (verificación manual pendiente)
        X_train, y_train, X_test, y_test = cargar_datos()
        model = crear_modelo()
        model = compilar_modelo(model)
        history = entrenar_modelo(model, X_train, y_train, X_test, y_test)
        guardar_modelo(model)  # No falla si la carpeta existe
        # Nota: Verificar el archivo models/modelo_digitos.h5 requerirá ejecución

if __name__ == '__main__':
    unittest.main()