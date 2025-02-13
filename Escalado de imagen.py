# Cargar la imagen en escala de grises
import cv2 as cv
import numpy as np
img = cv.imread('casa.jpg', 1)

# Definir el factor de escala
scale_x, scale_y = 0.5, 0.5

# Aplicar el escalado usando cv.resize()
scaled_img = cv.resize(img, None, fx=scale_x, fy=scale_y)


# Mostrar la imagen original y la escalada
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Escalada', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()



#+END_SRC


#+RESULTS:

