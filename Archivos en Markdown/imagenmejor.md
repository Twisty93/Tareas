# imagenmejor.py

Código para cargar una imagen y mejorar su resolución usando un modelo preentrenado de super-resolución (FSRCNN).
El script carga la imagen, aplica la mejora, guarda y muestra el resultado final.

```python
import cv2
import numpy as np
import os

def enhance_image(image_path, model_path, scale=4):
    # Verificar si el modelo existe
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo en {model_path}")
        return
    
    # Cargar el modelo de super-resolución
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("fsrcnn", scale)  # Modelos disponibles: 'edsr', 'fsrcnn', 'lapsrn'
    
    # Cargar la imagen
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return
    
    # Mostrar imagen original para verificar carga
    cv2.imshow("Imagen Original", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Aplicar super-resolución
    enhanced_image = sr.upsample(image)
    
    # Guardar la imagen mejorada en la misma carpeta del script
    enhanced_path = os.path.join(os.getcwd(), "enhanced_image.png")
    success = cv2.imwrite(enhanced_path, enhanced_image)
    
    if success:
        print(f"Imagen mejorada guardada en: {enhanced_path}")
    else:
        print("Error: No se pudo guardar la imagen mejorada.")
        return

    # Verificar si el archivo de imagen mejorada existe
    if not os.path.exists(enhanced_path):
        print("Error: El archivo de la imagen mejorada no existe.")
        return
    
    # Mostrar la imagen mejorada
    enhanced_display = cv2.imread(enhanced_path)
    if enhanced_display is not None:
        cv2.imshow("Imagen Mejorada", enhanced_display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: No se pudo mostrar la imagen mejorada.")
    
# Ruta de la imagen de entrada y el modelo preentrenado
image_path = "casa.jpg"  # Reemplazado con la imagen del usuario
model_path = "FSRCNN_x4.pb"  # Descarga el modelo de OpenCV y colócalo en la misma carpeta

enhance_image(image_path, model_path)

```