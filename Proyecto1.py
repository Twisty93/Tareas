import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def reconocer_letra(hand_landmarks, frame):
    h, w, _ = frame.shape
    dedos = [(int(hand_landmarks.landmark[i].x * w), int(hand_landmarks.landmark[i].y * h)) for i in range(21)]

    pulgar = dedos[4]
    indice = dedos[8]
    medio = dedos[12]
    anular = dedos[16]
    meñique = dedos[20]

    base_indice = dedos[5]
    base_medio = dedos[9]
    base_anular = dedos[13]
    base_meñique = dedos[17]
    base_pulgar = dedos[2]

    def dedo_estirado(punta, base):
        return punta[1] < base[1]

    indice_ext = dedo_estirado(indice, base_indice)
    medio_ext = dedo_estirado(medio, base_medio)
    anular_ext = dedo_estirado(anular, base_anular)
    meñique_ext = dedo_estirado(meñique, base_meñique)
    pulgar_ext = dedo_estirado(pulgar, base_pulgar)

    dist_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))

    # Letra I: solo meñique estirado, resto pegados a la palma
    if meñique_ext and not indice_ext and not medio_ext and not anular_ext:
        return "I"

    # Letra P: todos pegados a la palma (no estirados) excepto pulgar, que puede estar estirado o no,
    # y pulgar e índice cerca
    if (indice_ext and not medio_ext and not anular_ext and not meñique_ext) and dist_pulgar_indice < 100:
        return "P"

    # Letra Z: índice estirado y recto, resto pegados a la palma
    indice_punta = np.array(dedos[8])
    indice_medio = np.array(dedos[7])
    indice_base = np.array(dedos[5])

    desv_punta_medio = abs(indice_punta[0] - indice_medio[0])
    desv_medio_base = abs(indice_medio[0] - indice_base[0])
    umbral_recto = 15

    if indice_ext and not medio_ext and not anular_ext and not meñique_ext and desv_punta_medio < umbral_recto and desv_medio_base < umbral_recto:
        return "Z"

    return "Desconocido"



def detectar_numero_50(manos, frame):
    if len(manos) != 1:
        return False
    mano = manos[0]
    dedos = [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in mano.landmark]

    # Todos los dedos extendidos (palma abierta)
    def estirado(punta, base): return punta[1] < base[1]
    return all([
        estirado(dedos[8], dedos[5]),   # índice
        estirado(dedos[12], dedos[9]),  # medio
        estirado(dedos[16], dedos[13]), # anular
        estirado(dedos[20], dedos[17]), # meñique
        estirado(dedos[4], dedos[2])    # pulgar
    ])

def dedo_estirado(punta, base):
    return punta[1] < base[1]

def detectar_numero_25(manos, frame):
    if len(manos) != 2:
        return False

    # Comprobar si la primera mano está haciendo la "pinza" (pulgar e índice extendidos)
    mano_1 = manos[0]
    dedos_1 = [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in mano_1.landmark]
    pulgar_1 = dedos_1[4]
    indice_1 = dedos_1[8]
    medio_1 = dedos_1[12]
    anular_1 = dedos_1[16]
    meñique_1 = dedos_1[20]

    # Verificar la "pinza" (pulgar e índice juntos, el resto doblado)
    dist_pulgar_indice = np.linalg.norm(np.array(pulgar_1) - np.array(indice_1))
    if dist_pulgar_indice > 40:  # Si la distancia es mayor, no es pinza
        return False

    # Verificar que los otros dedos estén doblados
    if dedo_estirado(medio_1, dedos_1[9]) or dedo_estirado(anular_1, dedos_1[13]) or dedo_estirado(meñique_1, dedos_1[17]):
        return False

    # Comprobar si la segunda mano está completamente extendida (palma abierta)
    mano_2 = manos[1]
    dedos_2 = [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in mano_2.landmark]

    def es_extendido(coords):
        return all(coords[i][1] < coords[i - 2][1] for i in [8, 12, 16, 20])

    if not es_extendido(dedos_2):
        return False

    return True

def detectar_numero_15(manos, frame):
    if len(manos) != 2:
        return False

    def dedos_estirados(landmarks):
        dedos = [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in landmarks.landmark]
        def estirado(punta, base): return punta[1] < base[1]
        return all([
            estirado(dedos[8], dedos[5]),    # Índice
            estirado(dedos[12], dedos[9]),   # Medio
            estirado(dedos[16], dedos[13]),  # Anular
            estirado(dedos[20], dedos[17]),  # Meñique
            estirado(dedos[4], dedos[2])     # Pulgar
        ])

    def dedos_flexionados(landmarks):
        dedos = [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in landmarks.landmark]
        def doblado(punta, base): return punta[1] > base[1]
        return all([
            doblado(dedos[8], dedos[5]),
            doblado(dedos[12], dedos[9]),
            doblado(dedos[16], dedos[13]),
            doblado(dedos[20], dedos[17]),
            doblado(dedos[4], dedos[2])
        ])

    mano1 = manos[0]
    mano2 = manos[1]

    # Caso 1: ambas abiertas acostadas
    ambas_abiertas = dedos_estirados(mano1) and dedos_estirados(mano2)

    # Caso 2: una abierta, otra en puño (acostadas)
    una_abierta_una_cerrada = (
        (dedos_estirados(mano1) and dedos_flexionados(mano2)) or
        (dedos_estirados(mano2) and dedos_flexionados(mano1))
    )

    return ambas_abiertas or una_abierta_una_cerrada


def mesota(manos, frame):
    if len(manos) != 2:
        return False

    def extraer_info(mano):
        return [(int(p.x * frame.shape[1]), int(p.y * frame.shape[0])) for p in mano.landmark]

    coords1 = extraer_info(manos[0])
    coords2 = extraer_info(manos[1])

    def es_like(coords):
        pulgar_ext = coords[4][1] < coords[3][1]
        otros_dedos_abajo = all(coords[i][1] > coords[i - 2][1] for i in [8, 12, 16, 20])
        return pulgar_ext and otros_dedos_abajo

    def es_plana(coords):
        y_vals = [coords[i][1] for i in [8, 12, 16, 20]]
        return max(y_vals) - min(y_vals) < 30

    return (es_like(coords1) and es_plana(coords2)) or (es_like(coords2) and es_plana(coords1))

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        manos = results.multi_hand_landmarks
        for hand_landmarks in manos:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            letra_detectada = reconocer_letra(hand_landmarks, frame)
            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        if mesota(manos, frame):
            cv2.putText(frame, "Palabra: MESA", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        elif detectar_numero_50(manos, frame):
            cv2.putText(frame, "Numero: 50", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        elif detectar_numero_15(manos, frame):
            cv2.putText(frame, "Numero: 15", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 100, 0), 3)
        elif detectar_numero_25(manos, frame):
            cv2.putText(frame, "Numero: 25", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    cv2.imshow("Reconocimiento de Letras y Palabras", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
