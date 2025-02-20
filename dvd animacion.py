import cv2 as cv
import numpy as np

# Definir dimensiones de la ventana
width, height = 600, 200
img = np.ones((height, width, 3), dtype=np.uint8) * 255

# Posición inicial y velocidad del círculo
x, y = 50, 50
vx, vy = 5, 4  # Velocidad en x y y
radio = 20
color = (50, 400, 10)

while True:
    # Limpiar pantalla
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar círculo
    cv.circle(img, (x, y), radio, color, -1)
    
    x += vx
    y += vy
    
    # Rebotar en los bordes
    if x - radio <= 0 or x + radio >= width:
        vx = -vx
    if y - radio <= 0 or y + radio >= height:
        vy = -vy
    
    # Mostrar imagen
    cv.imshow('img', img)
    if cv.waitKey(20) & 0xFF == 27:  
        break

cv.destroyAllWindows()



