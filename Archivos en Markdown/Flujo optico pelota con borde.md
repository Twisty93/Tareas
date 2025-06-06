# Flujo optico pelota con borde.py

Seguimiento de una pelota usando flujo óptico y reinicio si sale de un marco definido , tambien muestra la pocision de la pelota en la escena

```python
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

ret, first_frame = cap.read()
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

ball_original_pos = np.array([[200, 200]], dtype=np.float32)
ball_pos = ball_original_pos[:, np.newaxis, :]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Obtener dimensiones del frame
    x, y = frame.shape[:2]
    frame = cv.flip(frame, 1)

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico para mover la pelotita
    new_ball_pos, st, err = cv.calcOpticalFlowPyrLK(prev_gray, gray_frame, ball_pos, None, **lk_params)

    margin = 20
    left, right = margin, y - margin
    top, bottom = margin, x - margin

    if new_ball_pos is not None:
        a, b = new_ball_pos.ravel()

        # Verificar si la pelota salió del marco
        if a < left or a > right or b < top or b > bottom:
            ball_pos = np.array([[200, 200]], dtype=np.float32)  # Resetear posición
        else:
            ball_pos = new_ball_pos  # Mantener movimiento

    cv.rectangle(frame, (left, top), (right, bottom), (200, 43, 34), 5)

    # Dibujar la pelota en su posición
    a, b = ball_pos.ravel()
    frame = cv.circle(frame, (int(a), int(b)), 20, (0, 255, 0), -1)

    # Mostrar la posición de la pelota en la pantalla
    posicion = f"Pos: ({int(a)}, {int(b)})"
    cv.putText(frame, posicion, (30, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)

    cv.imshow('Pelota en movimiento', frame)

    prev_gray = gray_frame.copy()

    # Presionar 'Esc' para salir
    if cv.waitKey(30) & 0xFF == 27:
        break

# Liberar la captura y destruir todas las ventanas
cap.release()
cv.destroyAllWindows()

```