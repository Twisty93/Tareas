# Imagen python.py

Código que carga una imagen en color, separa sus canales RGB,
realiza manipulaciones para mostrar cada canal por separado

```python
import cv2 as cv   #importa openCv
import numpy as np  # Importa Numpy
print (cv.__version__)

img = cv.imread('1a.jpg',1)   # Carga la imagen 1a.png en color (1 para color,0 para escala de grises)

img2=np.zeros((img.shape[:2]),dtype=np.uint8)   
print(img.shape[:2])

#separa los canales RGB de la imagen utilizando la funcion
r, g, b =cv.split(img)
img3=cv.merge([g,r,b])

#Recombina los canales,pero los reorganiza como rojoazul y verde (RGB)
r2 = cv.merge([img2,img2,r])
g2= cv.merge([img2,g,img2])
b2= cv.merge([b,img2,img2])


print(img.shape)
cv.imshow('r2 ',r2)
cv.imshow('b2 ',b2)
cv.imshow('g2 ',g2)
cv.imshow('img2',img3)
cv.waitKey (0)
cv.destoyAllWindows()
```