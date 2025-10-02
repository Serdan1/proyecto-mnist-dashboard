# Proyecto MNIST Dashboard

Este proyecto es un sistema para reconocer dígitos dibujados y subirlos a Firebase Storage.

## Funcionalidades
- Entrena un modelo de CNN para predecir dígitos (usando MNIST).
- Predice dígitos a partir de imágenes dibujadas (ej. images/images_digito_1.png).
- Sube las imágenes a Firebase Storage y genera una URL pública.

## Requisitos
- Python 3.12
- TensorFlow, Keras, firebase-admin (instalados con pip)

## Instalación
1. Clona el repositorio: `git clone https://github.com/Serdan1/proyecto-mnist-dashboard.git`
2. Instala dependencias: `pip install -r requirements.txt` (crea requirements.txt si es necesario)
3. Configura Firebase: Añade firebase-credentials.json en config/

## Uso
- Ejecuta el programa: `python main.py`
- La predicción y subida se orquestan automáticamente.

## Notas
- Las reglas de Firebase Storage están configuradas como públicas (`if true`) para pruebas. Ajusta a `if request.auth != null` para seguridad.