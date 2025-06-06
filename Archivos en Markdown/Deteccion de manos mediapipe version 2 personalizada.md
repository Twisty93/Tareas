# Deteccion de manos mediapipe version 2 personalizada.py

Script para detección de hasta dos manos en tiempo real usando MediaPipe y OpenCV.
Dibuja puntos clave y conexiones con colores personalizados (cyan para landmarks y naranja para conexiones).
Muestra la cantidad de manos detectadas en pantalla y permite salir con la tecla 'q'.

```python
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.6, 
    min_tracking_confidence=0.6,
    max_num_hands=2
)

drawing_spec_landmarks = mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=5)  
drawing_spec_connections = mp_drawing.DrawingSpec(color=(0, 165, 255), thickness=2)  # Naranja conexiones

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara.")
        break

    frame = cv2.flip(frame, 1)

    # Convertir imagen a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar manos
    results = hands.process(frame_rgb)

    # Dibujar puntos clave y conexiones con colores personalizados
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                drawing_spec_landmarks, drawing_spec_connections
            )
        # Mostrar número de manos detectadas
        cv2.putText(frame, f"Manos detectadas: {len(results.multi_hand_landmarks)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Manos detectadas: 0", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Mostrar la imagen
    cv2.imshow("Deteccion de Manos - MediaPipe", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

```