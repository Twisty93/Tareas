# haardcascade lentes.py

Detección de rostros con cámara en tiempo real  usando harcascade y dibujo de lentes y sombrero sobre cada rostro detectado

```python
import cv2 as cv
import numpy as np

rostro = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break

    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in rostros:
        
        radio_ojo = int(w * 0.18)  
        grosor = 3  

        ojo_izq = (x + int(w * 0.3), y + int(h * 0.4))
        ojo_der = (x + int(w * 0.7), y + int(h * 0.4))

        
        cv.circle(img, ojo_izq, radio_ojo, (0, 0, 0), grosor)
        cv.circle(img, ojo_der, radio_ojo, (0, 0, 0), grosor)

        
        puente_x1 = x + int(w * 0.42)
        puente_x2 = x + int(w * 0.58)
        puente_y = y + int(h * 0.4)
        cv.line(img, (puente_x1, puente_y), (puente_x2, puente_y), (0, 0, 0), grosor)

        
        cv.line(img, (x + int(w * 0.1), y + int(h * 0.35)), (x + int(w * 0.3), y + int(h * 0.4)), (0, 0, 0), grosor)
        cv.line(img, (x + int(w * 0.9), y + int(h * 0.35)), (x + int(w * 0.7), y + int(h * 0.4)), (0, 0, 0), grosor)

       
        sombrero_ancho = int(w * 1.2)  
        sombrero_alto = int(h * 0.4)  
        borde_alto = int(h * 0.1) 

        sombrero_x1 = x - int(w * 0.1)
        sombrero_x2 = x + w + int(w * 0.1)
        sombrero_y1 = y - sombrero_alto
        sombrero_y2 = y

      
        cv.rectangle(img, (sombrero_x1 + int(w * 0.3), sombrero_y1), (sombrero_x2 - int(w * 0.3), sombrero_y2 - borde_alto), (0, 0, 0), -1)

        cv.rectangle(img, (sombrero_x1, sombrero_y2 - borde_alto), (sombrero_x2, sombrero_y2), (0, 0, 0), -1)

    cv.imshow('Lentes', img)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()


```