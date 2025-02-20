import cv2 as cv
import numpy as np
import math

# Dimensiones de la ventana
width, height = 600, 400

# Propiedades de la manzana
x, y = 100, 300  # Posición inicial
vx, vy = 5, 0  # Velocidad inicial
radio = 40  # Tamaño de la manzana
angulo = 0  # Ángulo de rotación

# Gravedad y fricción
gravedad = 0.5
rebote = -0.7
friccion = 0.98

while True:
    # Crear imagen en blanco
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Dibujar la manzana con rotación
    for i in range(100, 0, -5):
        color = (0, 0, 255 - i)  # Degradado rojo oscuro al centro
        cv.ellipse(img, (x, y), (radio + i//5, int(radio * 1.2) + i//10), int(math.degrees(angulo)), 0, 360, color, -1)

    # Dibujar el brillo
    bx = x + int(math.cos(angulo) * 15) - 15
    by = y - int(math.sin(angulo) * 15) - 15
    cv.circle(img, (bx, by), 10, (255, 255, 255), -1)

    # Dibujar el tallo (gira con la manzana)
    tx = x + int(math.cos(angulo) * 20) - 5
    ty = y - int(math.sin(angulo) * 40) - radio - 5
    cv.line(img, (tx, ty), (tx + 5, ty - 10), (50, 25, 0), 5)

    # Dibujar la hoja (también rota)
    hx = x + int(math.cos(angulo) * 30)
    hy = y - int(math.sin(angulo) * 40) - radio - 20
    leaf_pts = np.array([[hx, hy], [hx + 15, hy - 25], [hx + 30, hy - 10]], np.int32)
    leaf_pts = leaf_pts.reshape((-1, 1, 2))
    cv.fillPoly(img, [leaf_pts], (0, 180, 0))
    cv.polylines(img, [leaf_pts], True, (0, 100, 0), 2)

    # Actualizar posición y velocidad
    x += vx
    y += vy
    vy += gravedad  # Aplicar gravedad
    vx *= friccion  # Aplicar fricción

    # Rebote en el suelo
    if y + radio >= height:
        y = height - radio
        vy *= rebote
        vx *= 0.9  # Reducir velocidad en cada rebote

    # Rebote en las paredes
    if x - radio <= 0 or x + radio >= width:
        vx = -vx
        angulo += math.pi  # Invertir dirección de giro

    # Girar la manzana
    angulo += vx * 0.05

    # Mostrar la imagen
    cv.imshow('Manzana Rodando', img)
    if cv.waitKey(20) & 0xFF == 27:  # Presiona ESC para salir
        break

cv.destroyAllWindows()
