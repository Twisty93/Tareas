# Parte 1 del proyecto 2 lograr accercar y alejar camara, esqueleto rana.py

Código que usa OpenCV y MediaPipe para controlar la cámara 3D con gestos de la mano,
renderizando una escena 3D con OpenGL y GLFW, es una version inicial del proyecto 2.

```python
import cv2
import mediapipe as mp
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import time
import math
from math import pi, sin, cos


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 0.0, 0.0]
camera_up = [0.0, 1.0, 0.0]

zoom_min = 3.0
zoom_max = 15.0

ref_pos = None  # referencia inicial mano
ref_pixel_pos = None  # posición en píxeles para dibujar el puntito

last_zoom_action_time = 0
zoom_cooldown = 0.3

cap = cv2.VideoCapture(0)

def init_opengl():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def draw_variable_flatten_sphere(radius=1, slices=30, stacks=30):
    glBegin(GL_QUADS)
    for i in range(stacks):
        lat0 = pi * (-0.5 + float(i) / stacks)
        lat1 = pi * (-0.5 + float(i + 1) / stacks)
        y0, y1 = sin(lat0), sin(lat1)
        r0, r1 = cos(lat0), cos(lat1)

        def flatten_factor(y): return 0.4 + 0.6 * ((y + 1) / 2)
        f0, f1 = flatten_factor(y0), flatten_factor(y1)

        for j in range(slices):
            lng0 = 2 * pi * float(j) / slices
            lng1 = 2 * pi * float(j + 1) / slices
            x0, z0 = cos(lng0), sin(lng0)
            x1, z1 = cos(lng1), sin(lng1)

            for nx, ny, nz, ff in [
                (x0 * r0, y0, z0 * r0, f0),
                (x0 * r1, y1, z0 * r1, f1),
                (x1 * r1, y1, z1 * r1, f1),
                (x1 * r0, y0, z1 * r0, f0),
            ]:
                glNormal3f(nx, ny, nz)
                glVertex3f(radius * nx, radius * ny * ff, radius * nz)
    glEnd()

def draw_body():
    glColor3f(0.6, 1.0, 0.5)
    glPushMatrix()
    draw_variable_flatten_sphere(1.0, 40, 40)
    glPopMatrix()

def draw_eyes():
    glColor3f(0.9, 1.0, 0.7)
    for x in (-0.4, 0.4):
        glPushMatrix()
        glTranslatef(x, 0.6, 0.5)
        quad = gluNewQuadric()
        gluSphere(quad, 0.2, 20, 20)
        glPopMatrix()
    glColor3f(0.0, 0.0, 0.0)
    for x in (-0.4, 0.4):
        glPushMatrix()
        glTranslatef(x, 0.65, 0.6)
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 20, 20)
        glPopMatrix()

def draw_legs():
    glColor3f(0.6, 1.0, 0.5)
    for x in (-0.6, 0.6):
        glPushMatrix()
        glTranslatef(x, -0.2, 0.6)
        glRotatef(-30 if x < 0 else 30, 1, 0, 0)
        glScalef(1.2, 0.8, 0.8)
        quad = gluNewQuadric()
        gluSphere(quad, 0.3, 20, 20)
        glPopMatrix()
    for x in (-0.3, 0.3):
        glPushMatrix()
        glTranslatef(x, -0.4, 0.3)
        glRotatef(-60 if x < 0 else 60, 1, 0, 0)
        glScalef(0.8, 0.4, 0.4)
        quad = gluNewQuadric()
        gluSphere(quad, 0.2, 20, 20)
        glPopMatrix()

def draw_frog():
    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    draw_body()
    draw_eyes()
    draw_legs()
    
    glPopMatrix()






def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_sphere():
    glPushMatrix()
    glColor3f(0.2, 0.6, 1.0)
    glTranslatef(0.0, 0.0, 0.0)
    quad = gluNewQuadric()
    gluSphere(quad, 1.0, 32, 32)
    glPopMatrix()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*camera_pos, *camera_target, *camera_up)
    draw_ground()
    draw_sphere()
    draw_frog()



def mano_en_puno(hand_landmarks):
    lm = hand_landmarks.landmark
    dedos_cerrados = 0
    dedos = [(8,6), (12,10), (16,14), (20,18)]
    for tip, pip in dedos:
        if lm[tip].y > lm[pip].y:
            dedos_cerrados +=1
    return dedos_cerrados == 4

def mano_en_pinza(hand_landmarks):
    lm = hand_landmarks.landmark
    distancia = np.linalg.norm(np.array([lm[4].x, lm[4].y]) - np.array([lm[8].x, lm[8].y]))
    return distancia < 0.04

def controlar_camara(hand_landmarks, frame):
    global camera_pos, ref_pos, ref_pixel_pos, last_zoom_action_time

    lm = hand_landmarks.landmark
    palm_x = lm[0].x
    palm_y = lm[0].y

    h, w, _ = frame.shape
    pixel_x = int(palm_x * w)
    pixel_y = int(palm_y * h)

    if ref_pos is None:
        ref_pos = (palm_x, palm_y)
        ref_pixel_pos = (pixel_x, pixel_y)

    dx = palm_x - ref_pos[0]
    dy = palm_y - ref_pos[1]

    # Movimiento lateral y vertical suave
    camera_pos[0] += dx * 0.7
    camera_pos[1] -= dy * 0.7

    camera_pos[0] = max(-5, min(5, camera_pos[0]))
    camera_pos[1] = max(1, min(6, camera_pos[1]))

    ahora = time.time()
    if ahora - last_zoom_action_time > 0.3:
        if mano_en_pinza(hand_landmarks):
            camera_pos[2] -= 0.05
            last_zoom_action_time = ahora
        elif mano_en_puno(hand_landmarks):
            camera_pos[2] += 0.05
            last_zoom_action_time = ahora

    camera_pos[2] = max(zoom_min, min(zoom_max, camera_pos[2]))

def main():
    global cap, ref_pos, ref_pixel_pos

    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Control cámara con mano", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init_opengl()

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                controlar_camara(hand_landmarks, frame)
                # dibujar landmarks Mediapipe
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if ref_pixel_pos is not None:
                cv2.circle(frame, ref_pixel_pos, 10, (0, 0, 255), -1)  # puntito rojo de referencia
        else:
            ref_pos = None
            ref_pixel_pos = None

        draw_scene()
        glfw.swap_buffers(window)
        glfw.poll_events()

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__ == "__main__":
    main()

```