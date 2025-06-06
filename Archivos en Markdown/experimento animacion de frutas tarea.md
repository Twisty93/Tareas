# experimento animacion de frutas tarea.py

Este programa anima varias frutas (manzana, naranja y sandía) que se mueven dentro de una ventana
con fondo personalizado. Las frutas rebotan en los bordes y entre sí, y el sol también gira
en una órbita circular. Se utiliza OpenCV para el renderizado y movimiento cuadro a cuadro.

```python
import cv2 as cv
import numpy as np
import math


fondo = cv.imread("dibujopaint.jpg")




width, height = 1000, 600
fondo = cv.resize(fondo, (width, height))


x, y, vx, vy, radio = 100, 100, 5, 4, 40   # Manzana
z, w, vz, vw, radionaranja = 300, 300, -6, 3, 60  # Naranja
s, t, vs, vt, radiosandia = 500, 200, 4, -5, 70  # Sandía


sol_x, sol_y = width // 2, 80
radio_orbita = 50
angulo = 0


def distancia(px1, py1, px2, py2):
    return math.sqrt((px2 - px1) ** 2 + (py2 - py1) ** 2)

while True:
    img = fondo.copy()

    
    sol_x_actual = sol_x + int(radio_orbita * math.cos(angulo))
    sol_y_actual = sol_y + int(radio_orbita * math.sin(angulo))
    angulo += 0.05
    cv.circle(img, (sol_x_actual, sol_y_actual), 50, (0, 255, 255), -1)  # Sol amarillo
    cv.circle(img, (sol_x_actual, sol_y_actual), 52, (255, 255, 0), 2)  # Borde brillante
    for i in range(0, 360, 30):  # Rayos de luz
        x_rayo = sol_x_actual + int(70 * math.cos(math.radians(i)))
        y_rayo = sol_y_actual + int(70 * math.sin(math.radians(i)))
        cv.line(img, (sol_x_actual, sol_y_actual), (x_rayo, y_rayo), (0, 255, 255), 2)

    
    for i in range(100, 0, -5):
        color = (0, 0, 255 - i)
        cv.ellipse(img, (x, y), (radio + i//5, int(radio * 1.2) + i//10), 0, 0, 360, color, -1)
    cv.circle(img, (x - 10, y - 20), 10, (255, 255, 255), -1)  # Brillo
    cv.line(img, (x, y - radio - 10), (x, y - radio + 10), (50, 25, 0), 5)  # Tallo

    
    cv.circle(img, (z, w), radionaranja, (0, 140, 255), -1)
    for i in range(10):
        cx = z + np.random.randint(-radionaranja + 10, radionaranja - 10)
        cy = w + np.random.randint(-radionaranja + 10, radionaranja - 10)
        cv.circle(img, (cx, cy), 3, (0, 100, 200), -1)
    cv.circle(img, (z, w - 30), 8, (255, 255, 255), -1)  # Brillo


    cv.circle(img, (s, t), radiosandia, (0, 255, 0), -1)
    for j in range(-30, 31, 10):  # Rayas de la sandía
        cv.ellipse(img, (s, t), (radiosandia - 10, int(radiosandia * 1.2) - 10), j, 0, 30, (0, 150, 0), 5)


    x += vx
    y += vy
    z += vz
    w += vw
    s += vs
    t += vt

    
    if x - radio <= 0 or x + radio >= width: vx = -vx
    if y - radio <= 0 or y + radio >= height: vy = -vy
    if z - radionaranja <= 0 or z + radionaranja >= width: vz = -vz
    if w - radionaranja <= 0 or w + radionaranja >= height: vw = -vw
    if s - radiosandia <= 0 or s + radiosandia >= width: vs = -vs
    if t - radiosandia <= 0 or t + radiosandia >= height: vt = -vt

    # ⚡ Colisiones entre frutas
    frutas = [(x, y, radio, vx, vy), (z, w, radionaranja, vz, vw), (s, t, radiosandia, vs, vt)]
    for i in range(len(frutas)):
        for j in range(i + 1, len(frutas)):
            x1, y1, r1, v1x, v1y = frutas[i]
            x2, y2, r2, v2x, v2y = frutas[j]

            if distancia(x1, y1, x2, y2) <= r1 + r2:  # Si hay colisión, intercambian velocidades
                frutas[i] = (x1, y1, r1, v2x, v2y)
                frutas[j] = (x2, y2, r2, v1x, v1y)

    (x, y, radio, vx, vy), (z, w, radionaranja, vz, vw), (s, t, radiosandia, vs, vt) = frutas

    # 🎬 Mostrar la imagen
    cv.imshow('Frutas en Movimiento', img)
    if cv.waitKey(20) & 0xFF == 27: 
        break

cv.destroyAllWindows()




```