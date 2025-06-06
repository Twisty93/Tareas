# Deteccion de manos.py

muestra la deteccion de ambas manos marcandolas por puntos

```python
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar manos
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx,landmark in enumerate (hand_landmarks.landmark):
                h,w,_=frame.shape
                x,y=int(landmark.x*w),int (landmark.y*h)
                cv2.circle(frame,(x,y),2,(12,233,4),-1)

    cv2.imshow("Salida", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```