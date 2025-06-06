# Dibujo Manzana.py

Código para dibujar una manzana,
usando degradados para el cuerpo, un brillo, tallo curvado y hoja con contorno.

```python
import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Dibujar la manzana con degradado
for i in range(100, 0, -5):
    color = (0, 0, 255 - i)  # Degradado rojo oscuro al centro
    cv.ellipse(img, (250, 300), (80 + i//5, 100 + i//10), 0, 0, 360, color, -1)

# Dibujar el brillo de la manzana
cv.circle(img, (220, 260), 20, (255, 255, 255), -1)

cv.line(img, (250, 210), (255, 250), (50, 25, 0), 10)
cv.line(img, (255, 250), (250, 260), (50, 25, 0), 10)

# Dibujar la hoja con contorno
leaf_pts = np.array([[250, 200], [280, 160], [310, 190], [280, 200]], np.int32)
leaf_pts = leaf_pts.reshape((-1, 1, 2))
cv.fillPoly(img, [leaf_pts], (0, 180, 0))
cv.polylines(img, [leaf_pts], True, (0, 100, 0), 3)

cv.imshow('Manzana Realista', img)
cv.waitKey(0)
cv.destroyAllWindows()

```