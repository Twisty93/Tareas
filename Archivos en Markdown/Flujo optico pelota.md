# Flujo optico pelota.py

Seguimiento de una pelotita usando flujo óptico para simular su movimiento en tiempo real con la cámara

```python
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)

lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

ball_pos = np.array([[200, 200]], dtype=np.float32)
ball_pos = ball_pos[:, np.newaxis, :]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    x, y =frame.shape[:2]
    frame= cv.flip(frame,1)
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico para mover la pelotita
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    # Si se detecta el nuevo movimiento, actualizar la posición de la pelotita
    if new_ball_pos is not None:
        ball_pos = new_ball_pos

        # Dibujar la pelotita en su nueva posición
        a, b = ball_pos.ravel()
        frame = cv.circle(frame, (int(a), int(b)), 20, (0, 255, 0), -1)
    cv.rectangle(frame, (20,20), (y-20, x-20), (234,43 ,34) ,5)    
    # Mostrar solo una ventana con la pelotita en movimiento
    cv.imshow('Pelota en movimiento', frame)

    prev_gray = gray_frame.copy()

    
    # Presionar 'Esc' para salir
    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()

```