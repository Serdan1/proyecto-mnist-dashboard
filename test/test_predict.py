# test_predict.py
# Este archivo contendrá pruebas unitarias para verificar las funciones de src/predict.py.
# Probará el flujo de predicción de dígitos a partir de imágenes.

import unittest
import sys
import os
from PIL import Image
import numpy as np

# Ajustar el path al inicio para incluir la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import cargar_modelo, preprocesar_imagen, predecir_digito

class TestPredictFunctions(unittest.TestCase):
    def setUp(self):
        # Definir la ruta de la imagen de prueba
        self.ruta_imagen = 'images/images_digito_1.png'

    def test_cargar_modelo(self):
        # Prueba que cargar_modelo() devuelva un modelo válido
        model = cargar_modelo()
        self.assertIsNotNone(model)  # Verifica que no sea None
        # Nota: Requiere que models/modelo_digitos.h5 exista

    def test_preprocesar_imagen(self):
        # Prueba que preprocesar_imagen() devuelva un array con forma correcta
        img_array = preprocesar_imagen(self.ruta_imagen)
        self.assertEqual(img_array.shape, (1, 28, 28, 1))  # Forma esperada para la CNN
        # Guardar la imagen procesada para inspección
        processed_data = (img_array[0, :, :, 0] * 255).clip(0, 255).astype(np.uint8)
        processed_img = Image.fromarray(processed_data, mode='L')
        processed_img.save('images/procesada_digito_1.png')

    def test_predecir_digito(self):
        # Prueba que predecir_digito() devuelva un dígito y probabilidades
        digito, probabilidades = predecir_digito(self.ruta_imagen)
        print(f"Dígito predicho: {digito}")  # Imprimir el dígito para verificar
        self.assertIsInstance(digito, int)  # Verifica que el dígito sea un entero
        self.assertEqual(len(probabilidades), 10)  # 10 probabilidades para cada clase

if __name__ == '__main__':
    unittest.main()