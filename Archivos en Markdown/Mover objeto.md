# Mover objeto.py

Usa la cámara para rastrear puntos con flujo óptico y mover una pelota según el movimiento.
Reinicia la malla si los puntos se pierden o se dispersan.

```python
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

def create_grid_points(step=50, width=640, height=480):
    points = np.array([(x, y) for y in range(step, height - step, step) for x in range(step, width - step, step)], dtype=np.float32)
    return points.reshape(-1, 1, 2)

ret, frameantiguo = cap.read()
if not ret:
    print("Error al capturar el frame inicial")
    cap.release()
    exit()

old_gray = cv.cvtColor(frameantiguo, cv.COLOR_BGR2GRAY)

h, w = old_gray.shape
p0 = create_grid_points(step=50, width=w, height=h)

pocisionp = np.array([200, 200], dtype=np.float32)
radiop = 15

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None and st is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        if len(good_new) > 0:
            movimiento = good_new - good_old
            distancia_media = np.linalg.norm(movimiento, axis=1).mean()

            for new_pt in good_new:
                a, b = new_pt.ravel()
                frame = cv.circle(frame, (int(a), int(b)), 3, (0, 200, 0), -1)

            if distancia_media < 15:
                pocisionp += movimiento.mean(axis=0)
                p0 = good_new.reshape(-1, 1, 2)
            else:
                p0 = good_old.reshape(-1, 1, 2)

            if len(p0) < 10:
                p0 = create_grid_points(step=50, width=w, height=h)

        else:
            p0 = create_grid_points(step=50, width=w, height=h)
    else:
        p0 = create_grid_points(step=50, width=w, height=h)

    pocisionp = np.clip(pocisionp, [radiop, radiop], [frame.shape[1] - radiop, frame.shape[0] - radiop])
    frame = cv.circle(frame, tuple(pocisionp.astype(int)), radiop, (0, 0, 255), -1)

    cv.imshow("Pelota Controlada por Malla", frame)

    old_gray = frame_gray.copy()

    if cv.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv.destroyAllWindows()

```