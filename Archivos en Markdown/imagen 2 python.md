# imagen 2 python.py

Conversión entre distintos espacios de color y modificación para resaltar tonos amarillos en una imagen# Código que carga una imagen y realiza múltiples conversiones entre espacios de color.
Además, modifica la imagen para cambiar su tonalidad a amarillo y muestra las imágenes resultantes.

```python
import cv2 as cv
import numpy as np

img= cv.imread('1a.jpg',1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img3 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img4 = cv.cvtColor(img, cv.COLOR_BGR2HSV)
img5 = cv.cvtColor(img, cv.COLOR_XYZ2RGB)
img6 = cv.cvtColor(img, cv.COLOR_RGB2Luv)
img7 = cv.cvtColor(img, cv.COLOR_BGR2Luv)
img8 = cv.cvtColor(img, cv.COLOR_Luv2RGB)
img9 = cv.cvtColor(img, cv.COLOR_Luv2BGR)
img10 = cv.cvtColor(img, cv.COLOR_HSV2RGB)
img11 = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
img12 = cv.cvtColor(img11, cv.COLOR_BGRA2BGR565)






img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Modificar los valores para hacerla amarilla
img_hsv[:, :, 0] = 30  # H (tono) ajustado a amarillo
img_hsv[:, :, 1] = 255 # S (saturación) al máximo
img_hsv[:, :, 2] = 255 # V (brillo) al máximo

# Convertir de nuevo a BGR
img_yellow = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)



cv.imshow('img2',img2)



x,y=img2.shape[:2]
print(x,y)
for i in range (x):
    for j in range (y):
        img2[i,j]=255-img2[i,j]
        cv.imshow('img20',img2)

cv.imshow('Original', img)
cv.imshow('Amarillo', img_yellow)



cv.imshow('img',img)
cv.imshow('img3',img3)
cv.imshow('img4',img4)
cv.imshow('img5',img5)
cv.imshow('img6',img6)
cv.imshow('img7',img7)
cv.imshow('img8',img8)
cv.imshow('img9',img9)
cv.imshow('img10',img10)
cv.imshow('img11',img11)
cv.imshow('img12',img11)
cv.waitKey(0)
cv.destroyAllWindows()


```