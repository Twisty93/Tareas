# Flujo optico malla.py

Este programa genera una malla sobre una imagen de la cámara en tiempo real. Dibuja líneas entre puntos vecinos para formar una malla.

```python
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

p0 = []
for y in range(50, 650, 75):
    for x in range(50, 850, 100):
        p0.append((x, y))

p0 = np.float32(p0).reshape(-1, 1, 2)
mask = np.zeros_like(vframe)

while True:
    _, frame = cap.read()
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]

        num_cols = 8  # columnas reales en la malla (ajustado a espaciado)

        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())

            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)  # punto anterior
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)  # punto actual

            if (i + 1) % num_cols != 0:
                next_idx = i + 1
                if next_idx < len(bp1):
                    x2, y2 = (int(x) for x in bp1[next_idx].ravel())
                    frame = cv.line(frame, (a, b), (x2, y2), (0, 255, 255), 1)

            down_idx = i + num_cols
            if down_idx < len(bp1):
                x3, y3 = (int(x) for x in bp1[down_idx].ravel())
                frame = cv.line(frame, (a, b), (x3, y3), (255, 0, 255), 1)

        cv.imshow('ventana', frame)
        vgris = fgris.copy()

        if (cv.waitKey(1) & 0xff) == 27:  # ESC para salir
            break

cap.release()
cv.destroyAllWindows()

```