import cv2
import numpy as np

# Captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Permitir que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo
ret, background = cap.read()
if not ret:
    print("Error al capturar el fondo.")
    cap.release()
    exit()

# Crear una imagen negra para almacenar el rastro
trail = np.zeros_like(background)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir los rangos de color rojo en HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Crear máscaras para ambos rangos de rojo
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combinar ambas máscaras
    mask = cv2.bitwise_or(mask1, mask2)

    # Refinar la máscara con operaciones morfológicas
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    # Crear una imagen en color para el rastro
    color_trail = np.zeros_like(frame)
    color_trail[np.where(mask != 0)] = (0, 0, 255)  # Pintar en rojo

    # Acumular el rastro en la imagen de fondo
    trail = cv2.addWeighted(trail, 0.7, color_trail, 0.3, 0)

    # Invertir la máscara para obtener las áreas que no son rojas
    mask_inv = cv2.bitwise_not(mask)

    # Aplicar la máscara a la imagen original para mostrar solo las partes no rojas
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Aplicar la máscara al fondo para cubrir las partes rojas
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar ambas imágenes
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Agregar el rastro a la imagen final
    final_output = cv2.add(final_output, trail)

    # Mostrar el resultado final
    cv2.imshow("Capa de Invisibilidad con Rastro", final_output)
    cv2.imshow("Mascara Roja", mask)
    cv2.imshow("Rastro", trail)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
