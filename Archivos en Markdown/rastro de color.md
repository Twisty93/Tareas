# rastro de color.py

Código que crea un efecto de capa de invisibilidad usando detección de color rojo,
reemplazando el área roja por un fondo previamente capturado y mostrando un rastro rojo.

```python
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.waitKey(2000)

ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()

# Crear una imagen negra para almacenar el rastro
trail = np.zeros_like(background)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    color_trail = np.zeros_like(frame)
    color_trail[np.where(mask != 0)] = (0, 0, 255)  # Pintar en rojo

    trail = cv2.addWeighted(trail, 0.7, color_trail, 0.3, 0)

    mask_inv = cv2.bitwise_not(mask)

    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    res2 = cv2.bitwise_and(background, background, mask=mask)

    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    final_output = cv2.add(final_output, trail)

    cv2.imshow("Capa de Invisibilidad con Rastro", final_output)
    cv2.imshow("Mascara Roja", mask)
    cv2.imshow("Rastro", trail)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

```