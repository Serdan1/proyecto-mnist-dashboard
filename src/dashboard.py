# dashboard.py
# Este archivo contendrá la lógica para crear una interfaz gráfica (dashboard) con Tkinter
# que permita arrastrar y soltar imágenes de dígitos dibujados en Paint. Integrará la
# predicción de dígitos (llamando a funciones de predict.py) y subirá las imágenes a
# Firebase Storage (usando credenciales de config/firebase-credentials.json).
# Será orquestado desde main.py. 

# Planificación de funciones y flujo:
# 1. iniciar_interfaz(): Configura la ventana principal de Tkinter con soporte para drag-and-drop.
#    - Define un área para soltar imágenes y un espacio para mostrar resultados.
# 2. manejar_drop(): Procesa el evento cuando se suelta una imagen en la interfaz.
#    - Carga la imagen desde la ruta arrastrada.
#    - Llama a preprocesar_imagen() y predecir_digito() desde predict.py.
# 3. mostrar_resultado(): Actualiza la interfaz con el dígito predicho y la URL de Firebase.
#    - Muestra texto o gráficos (ej. "Número: 1", "URL: [link]").
# 4. subir_a_firebase(): Sube la imagen original a Firebase Storage.
#    - Usa credenciales de config/firebase-credentials.json.
#    - Genera un nombre único (ej. digito_1_20251001_0530.png) y devuelve la URL pública.