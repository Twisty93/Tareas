# Enfatizar color version 2.0 con trackbar.py

Captura video en tiempo real, aplica filtro de color HSV configurable con trackbars,
y muestra la imagen original, máscara y resultado filtrado para facilitar ajuste dinámico.

```python
import cv2 as cv
import numpy as np

def nothing(x):
    pass

cv.namedWindow('Controles')

# Crear trackbars para ajustar los valores HSV 
cv.createTrackbar('Hue Min', 'Controles', 40, 179, nothing)
cv.createTrackbar('Hue Max', 'Controles', 90, 179, nothing)
cv.createTrackbar('Sat Min', 'Controles', 40, 255, nothing)
cv.createTrackbar('Sat Max', 'Controles', 255, 255, nothing)
cv.createTrackbar('Val Min', 'Controles', 40, 255, nothing)
cv.createTrackbar('Val Max', 'Controles', 255, 255, nothing)

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        print("Error al capturar frame")
        break

    # Leer valores de los trackbars
    h_min = cv.getTrackbarPos('Hue Min', 'Controles')
    h_max = cv.getTrackbarPos('Hue Max', 'Controles')
    s_min = cv.getTrackbarPos('Sat Min', 'Controles')
    s_max = cv.getTrackbarPos('Sat Max', 'Controles')
    v_min = cv.getTrackbarPos('Val Min', 'Controles')
    v_max = cv.getTrackbarPos('Val Max', 'Controles')

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower_bound, upper_bound)

    res = cv.bitwise_and(img, img, mask=mask)

    cv.imshow('Video Original', img)
    cv.imshow('Máscara', mask)
    cv.imshow('Resultado Filtrado', res)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC para salir
        break

cap.release()
cv.destroyAllWindows()

```