# animacion primitiva.py

Este script muestra una animación simple de un círculo verde que se mueve en diagonal
sobre un fondo blanco, utilizando OpenCV para el renderizado y control de ventanas.

+BEGIN_SRC python

```python
import cv2 as cv
import numpy as np

img = np.ones((500, 500), dtype=np.uint8) * 255

for i in range(400):
    # limpiado de pantalla
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    cv.circle(img, (0 + i, 0 + i), 20, (0, 234, 21), -1)
    cv.imshow('img', img)
    cv.waitKey(40)

cv.waitKey(0)
cv.destroyAllWindows()
#+END_SRC


```