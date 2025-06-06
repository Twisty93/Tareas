# escalar imagen y convolucion un noveno.py

Código que carga una imagen en escala de grises, la escala manualmente duplicando su tamaño,
y luego aplica un filtro de suavizado para suavizar la imagen escalada.

```python
import cv2 as cv
import numpy as np

img = cv.imread('1a.jpg', 0)
import numpy as np
x, y = img.shape


scale_x, scale_y = 2, 2

scaled_x, scaled_y = int(x * scale_x), int(y * scale_y)
scaled_img = np.zeros((scaled_x, scaled_y), dtype=np.uint8)


for i in range(x):
    for j in range(y):
     
        scaled_img[i*2,j*2] = img[i, j]  

cv.imshow('Imagen Escalada', scaled_img)

kernel = np.ones((3, 3), np.float32) / 9


convolved_img = np.zeros((scaled_x, scaled_y), dtype=np.uint8)


for i in range(scaled_x):
    for j in range(scaled_y):
        suma = 0
        for k in range(-1, 2):
            for l in range(-1, 2):
           
                new_x = min(max(i + k, 0), scaled_x - 1)  
                new_y = min(max(j + l, 0), scaled_y - 1)
                suma += scaled_img[new_x, new_y] * kernel[k + 1, l + 1]

  
        convolved_img[i, j] = np.clip(suma, 0, 255)


cv.imshow('Imagen Original', img)

cv.imshow('Imagen Convolucionada', convolved_img)
cv.waitKey(0)
cv.destroyAllWindows()


```