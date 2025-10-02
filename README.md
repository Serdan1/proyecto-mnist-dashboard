# Proyecto MNIST Dashboard

## Descripción
Este proyecto implementa una aplicación de reconocimiento de dígitos manuscritos utilizando una Red Neuronal Convolucional (CNN) entrenada con el dataset MNIST. La aplicación permite cargar o arrastrar imágenes de dígitos dibujados (por ejemplo, en Paint), predecir el número mediante un modelo de TensorFlow/Keras, y subir las imágenes a Firebase Storage con una URL pública. La interfaz gráfica está desarrollada con Tkinter, extendida con `tkinterdnd2` para soportar drag-and-drop. Este proyecto sigue las guías del temario de clase (páginas 9-17), que cubren la construcción de CNN, el dataset MNIST, backpropagation, funciones de activación (ReLU, softmax), y técnicas para manejar overfitting (dropout, regularización).

## Características
- Predicción de dígitos manuscritos con una CNN entrenada (precisión de validación ~97.45% con 3 épocas).
- Interfaz gráfica interactiva con soporte para drag-and-drop y carga manual.
- Subida automática de imágenes a Firebase Storage con URL accesible.
- Depuración integrada con mensajes en consola para facilitar el desarrollo.
- Umbral de confianza ajustable (actualmente 0.2) para validar predicciones.

## Requisitos
- **Python 3.8 o superior**
- Librerías requeridas (instalables vía `pip`):
  - `tensorflow` (para el modelo CNN)
  - `keras` (integrado con TensorFlow)
  - `firebase-admin` (para interacción con Firebase Storage)
  - `numpy` (para cálculos matriciales)
  - `pillow` (para procesamiento de imágenes)
  - `matplotlib` (para visualización durante el entrenamiento)
  - `pyrebase4` (para autenticación Firebase, opcional)
  - `tkinterdnd2` (para drag-and-drop en Tkinter)
- Una cuenta de Firebase con credenciales (`firebase-credentials.json`) configurada.

## Instalación

### Clonar el repositorio
1. Asegúrate de tener Git instalado.
2. Clona el repositorio:
   git clone https://github.com/Serdan1/proyecto-mnist-dashboard.git
   cd proyecto-mnist-dashboard
   pip install tensorflow keras firebase-admin numpy pillow matplotlib pyrebase4 tkinterdnd2

3. Configura Firebase:
- Ve a la consola de Firebase, selecciona tu proyecto, y genera un archivo de servicio (`firebase-credentials.json`).
- Coloca este archivo en la carpeta `config/` del proyecto.
4. Verifica las instalaciones:
   pip show tensorflow
   pip show tkinterdnd2


### Generar el modelo
1. Ejecuta el script principal para entrenar y guardar el modelo:
  python main.py
2. Verifica que `models/modelo_digitos.h5` se cree:
  dir models


## Uso
1. Ejecuta la aplicación:
  python -m src.dashboard

2. **Cargar una imagen**:
- Haz clic en "Cargar Imagen", selecciona una imagen (p. ej., `images/images_digito_1.png`) en formato PNG o JPG.
- La interfaz mostrará el dígito predicho (p. ej., "Número: 1, Confianza: 0.85") y la URL de Firebase tras subirla.
3. **Arrastrar y soltar**:
- Arrastra una imagen (p. ej., `im2.png`) al área "Suelta la imagen aquí".
- Si la confianza es mayor a 0.2, se mostrará el dígito y la URL; de lo contrario, se indicará "Confianza insuficiente".
4. Copia la URL generada y ábrela en un navegador para ver la imagen subida.

## Estructura del Proyecto
- `main.py`: Punto de entrada para entrenar el modelo y orquestar la predicción.
- `src/`:
  - `dashboard.py`: Lógica de la interfaz gráfica con Tkinter y drag-and-drop.
  - `predict.py`: Funciones para preprocesar imágenes y predecir dígitos con la CNN.
  - `train.py`: Entrenamiento de la CNN usando MNIST.
- `config/`: Almacena `firebase-credentials.json` para autenticación.
- `images/`: Incluye ejemplos como `images_digito_1.png` y `im2.png`.
- `models/`: Contiene el modelo entrenado (`modelo_digitos.h5`).
- `test/`: Archivos de prueba (p. ej., `test_predict.py`).

## Desempeño
- El modelo CNN fue entrenado con 3 épocas, alcanzando una precisión de validación del 97.45% en el dataset MNIST.
- El tiempo de predicción por imagen es ~74ms en una CPU estándar (SSE3, AVX2 habilitados).
- La subida a Firebase depende de la conexión a internet (típicamente <1s).


## Ejemplos de Uso
- **Imagen clara (images_digito_1.png)**: Predice "1" con confianza >0.85 y sube a Firebase.
- **Imagen ruidosa (im2.png)**: Puede requerir un umbral menor (p. ej., 0.2) para aceptar predicciones como "7" o "8".
- **Formato incompatible**: Asegúrate de usar PNG o JPG; otros formatos provocarán un error.

## Contribución
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad:
   git checkout -b feature/nueva-funcionalidad
3. Realiza tus cambios y confirma:
   git add .
   git commit -m "Descripción de los cambios"
4. Envía la rama:
   git push origin feature/nueva-funcionalidad
5. Abre un Pull Request en GitHub.



## Notas de Desarrollador
- El modelo usa una CNN con capas convolucionales, pooling, y fully connected.
- La función de activación ReLU y el softmax se han aplicado.
- El dropout (0.25) se usa para mitigar overfitting.
- La depuración con `print()` en la consola indica cada etapa (inicialización, predicción, subida).
- El umbral de confianza (0.2) es ajustable en `procesar_imagen()` para tolerar imágenes ruidosas.



