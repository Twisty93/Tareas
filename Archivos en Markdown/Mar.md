# Mar.py



```python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw
import sys
from PIL import Image
import math
import time
from math import sin, cos, pi, sqrt
from math import radians
import random
import threading
import cv2
import mediapipe as mp
import numpy as np

glfw.init()


display_list_pasto = None

# Inicialización de MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables de cámara
camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 0.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
zoom_min, zoom_max = 3.0, 15.0

ref_pos = None
ref_pixel_pos = None
last_zoom_action_time = 0

cap = cv2.VideoCapture(0)



def mano_en_puno(hand_landmarks):
    lm = hand_landmarks.landmark
    dedos = [(8,6), (12,10), (16,14), (20,18)]
    return sum(lm[tip].y > lm[pip].y for tip, pip in dedos) == 4

def mano_en_pinza(hand_landmarks):
    lm = hand_landmarks.landmark
    dist = np.linalg.norm(np.array([lm[4].x, lm[4].y]) - np.array([lm[8].x, lm[8].y]))
    return dist < 0.04

def controlar_camara(hand_landmarks, frame):
    global camera_pos, ref_pos, ref_pixel_pos, last_zoom_action_time

    lm = hand_landmarks.landmark
    palm_x = lm[0].x
    palm_y = lm[0].y
    h, w, _ = frame.shape
    pixel_x, pixel_y = int(palm_x * w), int(palm_y * h)

    if ref_pos is None:
        ref_pos = (palm_x, palm_y)
        ref_pixel_pos = (pixel_x, pixel_y)

    dx = palm_x - ref_pos[0]
    dy = palm_y - ref_pos[1]

    camera_pos[0] += dx * 0.7
    camera_pos[1] -= dy * 0.7
    camera_pos[0] = max(-5, min(5, camera_pos[0]))
    camera_pos[1] = max(1, min(6, camera_pos[1]))

    ahora = time.time()
    if ahora - last_zoom_action_time > 0.3:
        if mano_en_pinza(hand_landmarks):
            camera_pos[2] -= 0.3
            last_zoom_action_time = ahora
        elif mano_en_puno(hand_landmarks):
            camera_pos[2] += 0.3
            last_zoom_action_time = ahora

    camera_pos[2] = max(zoom_min, min(zoom_max, camera_pos[2]))


def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGB").tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture_id







def draw_variable_flatten_sphere(radius=1, slices=30, stacks=30):
    glBegin(GL_QUADS)
    for i in range(stacks):
        lat0 = pi * (-0.5 + float(i) / stacks)
        lat1 = pi * (-0.5 + float(i + 1) / stacks)

        y0 = sin(lat0)    # Altura del stack i
        y1 = sin(lat1)    # Altura del stack i+1

        r0 = cos(lat0)    # Radio del círculo en ese stack
        r1 = cos(lat1)

        # Factor de aplastamiento según altura (y), aquí lineal:
        # Más aplastado abajo (y cerca de -1) y normal arriba (y cerca de 1)
        def flatten_factor(y):
            # Por ejemplo, mapea -1 -> 0.4 y 1 -> 1.0
            return 0.4 + 0.6* ((y + 1.4) / 2)

        f0 = flatten_factor(y0)
        f1 = flatten_factor(y1)

        for j in range(slices):
            lng0 = 2 * pi * float(j) / slices
            lng1 = 2 * pi * float(j + 1) / slices

            x0 = cos(lng0)
            z0 = sin(lng0)
            x1 = cos(lng1)
            z1 = sin(lng1)

            # Primer vértice
            nx = x0 * r0
            ny = y0
            nz = z0 * r0
            glNormal3f(nx, ny, nz)
            glVertex3f(radius * nx, radius * ny * f0, radius * nz)

            # Segundo vértice
            nx = x0 * r1
            ny = y1
            nz = z0 * r1
            glNormal3f(nx, ny, nz)
            glVertex3f(radius * nx, radius * ny * f1, radius * nz)

            # Tercer vértice
            nx = x1 * r1
            ny = y1
            nz = z1 * r1
            glNormal3f(nx, ny, nz)
            glVertex3f(radius * nx, radius * ny * f1, radius * nz)

            # Cuarto vértice
            nx = x1 * r0
            ny = y0
            nz = z1 * r0
            glNormal3f(nx, ny, nz)
            glVertex3f(radius * nx, radius * ny * f0, radius * nz)

    glEnd()




def draw_body():
    global textura_cuerpo
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)  # Blanco = sin alterar textura

    glBindTexture(GL_TEXTURE_2D, textura_cuerpo)
      # Verde claro (cuerpo)
    glPushMatrix()
    

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)

    draw_variable_flatten_sphere(1.0, 50, 50)
    gluDeleteQuadric(quad)
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)
    # Panza de la rana 


def draw_panza(): 
    global textura_panza
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)  # Blanco = sin alterar textura

    glBindTexture(GL_TEXTURE_2D, textura_panza)

    glPushMatrix()
    glTranslatef(0.0, 0.12, 0.40)
    glScalef(1.0, 0.9, 1.0)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 0.65, 30, 50)
    gluDeleteQuadric(quad)

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)





def draw_cejas():

    
    global textura_cuerpo

    glEnable(GL_TEXTURE_2D)
    glColor3f(0.8, 0.8, 0.8)  # Oscurece un poco la textura (15%)
    glBindTexture(GL_TEXTURE_2D, textura_cuerpo)

    for i, x in enumerate((-0.32, 0.32)):
        glPushMatrix()
        glTranslatef(x, 0.78, 0.35)
        angle = 35 if i == 0 else -35
        glRotatef(angle, 0, 0, 1)
        glScalef(1.0, 0.65, 1.0)

        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, 0.3, 40, 40)
        gluDeleteQuadric(quad)

        glPopMatrix()

    glDisable(GL_TEXTURE_2D)



def draw_grass_blade_triple(x, z, height, width, color_variation):
    glPushMatrix()
    glTranslatef(x, -1.0, z)

    # Color base con ligera variación
    base_color = (0.3 + color_variation, 0.6 + color_variation, 0.3 + color_variation)
    glColor3f(*base_color)

    for angle in [0, 60, 120]:
        glPushMatrix()
        glRotatef(angle + random.uniform(-15, 15), 0, 1, 0)  # Variación de orientación
        glBegin(GL_QUADS)
        glVertex3f(-width / 2, 0, 0)
        glVertex3f(width / 2, 0, 0)
        glVertex3f(width / 2, height, 0)
        glVertex3f(-width / 2, height, 0)
        glEnd()
        glPopMatrix()

    glPopMatrix()


def crear_display_list_pasto():
    lista = glGenLists(1)
    glNewList(lista, GL_COMPILE)
    draw_grass_blade_triple(0, 0, 1.5, 0.1, 0.1)  # <-- ¡Ahora con color_variation!
    glEndList()
    return lista



def draw_terreno():
    global display_list_pasto
    global textura_terreno
    glPushMatrix()

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_terreno)

    glColor3f(1.0, 1.0, 1.0)  # Color blanco para que textura se vea bien

    size = 100
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-size, -1.0, -size)

    glTexCoord2f(1, 0)
    glVertex3f(size, -1.0, -size)

    glTexCoord2f(1, 1)
    glVertex3f(size, -1.0, size)

    glTexCoord2f(0, 1)
    glVertex3f(-size, -1.0, size)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    # Dibuja pasto sin textura
    random.seed(42)
    paso = 4
    exclusion_radio = 9.0

    for x in range(-size + 2, size, paso):
        for z in range(-size + 2, size, paso):
            distancia = math.sqrt(x ** 2 + z ** 2)
            if distancia > exclusion_radio:
                glPushMatrix()
                glTranslatef(x + random.uniform(-1, 1), 0.0, z + random.uniform(-1, 1))
                glRotatef(random.uniform(0, 360), 0, 1, 0)
                escala = random.uniform(2.0, 4.0)
                glScalef(1.0, escala, 1.0)

                glCallList(display_list_pasto)
                glPopMatrix()

    glPopMatrix()




def draw_agua():
    glPushMatrix()
    

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_LIGHTING)
    
    glColor4f(0.4, 0.9, 1.0, 0.75)


    num_rings = 100
    num_segments = 100
    max_radius = 9.0
    tiempo = glfw.get_time()

    glDepthMask(GL_FALSE)

    for r in range(num_rings):
        inner_radius = r * max_radius / num_rings
        outer_radius = (r + 1) * max_radius / num_rings
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(num_segments + 1):
            angle = 2 * pi * i / num_segments
            wave = 0.15 * sin(4 * angle + tiempo * 2.5 + r * 0.3)
            for radius in (inner_radius, outer_radius):
                mod_radius = radius + wave
                x = mod_radius * cos(angle)
                z = mod_radius * sin(angle)
                glVertex3f(x, 0.0, z)
        glEnd()

    glDepthMask(GL_TRUE)
    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glPopMatrix()


def draw_ground():
    draw_terreno()
   



def draw_boca():
    glPushMatrix()
    glTranslatef(0.0, 0.58, 0.8)
    glScalef(0.6, 0.08, 0.5)  # Más aplastada en Y

    glColor3f(0.1, 0.0, 0.0)  # Casi negro
    glLineWidth(4.0)  # Grosor de línea

    # Triángulo frontal sin línea base (solo lados)
    glBegin(GL_LINES)
    # Lado izquierdo
    glVertex3f(0.0, 1.0, 0.0)      # Punta
    glVertex3f(-0.3, 0.0, 0.0)     # Base izquierda
    
    # Lado derecho
    glVertex3f(0.0, 1.0, 0.0)      # Punta
    glVertex3f(0.3, 0.0, 0.0)      # Base derecha
    glEnd()

    # Triángulo trasero completo (contorno)
    glBegin(GL_LINE_LOOP)
    glVertex3f(0.0, 1.0, -1.0)
    glVertex3f(0.3, 0.0, -1.0)
    glVertex3f(-0.3, 0.0, -1.0)
    glEnd()

    # Líneas verticales conectando front y back
    glBegin(GL_LINES)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 1.0, -1.0)

    glVertex3f(-0.3, 0.0, 0.0)
    glVertex3f(-0.3, 0.0, -1.0)

    glVertex3f(0.3, 0.0, 0.0)
    glVertex3f(0.3, 0.0, -1.0)
    glEnd()

    glPopMatrix()





def draw_eyes():
    glColor3f(0.9, 1.0, 0.6)
    for i, x in enumerate((-0.4, 0.4)):
        glPushMatrix()
        glTranslatef(x, 0.7, 0.5)
        angle = 35 if i == 0 else -35  # espejo: izq +45, der -45
        glRotatef(angle, 0, 0, 1)
        glScalef(1.0, 0.65, 1.0)  # aplastado vertical suave
        glutSolidSphere(0.3, 20, 20)
        glPopMatrix()

    glColor3f(0.1, 0.0, 0.0)
    for i, x in enumerate((-0.45, 0.45)):
        glPushMatrix()
        glTranslatef(x, 0.73, 0.74)
        angle = 38 if i == 0 else -38
        glRotatef(angle, 0, 0, 1)
        glScalef(1.0, 0.20, 1.0)
        glutSolidSphere(0.15, 30, 30)
        glPopMatrix()

def draw_legs():
    global textura_cuerpo

    glEnable(GL_TEXTURE_2D)
    glColor3f(0.8, 0.8, 0.8)  # Oscurece un poco la textura
    glBindTexture(GL_TEXTURE_2D, textura_cuerpo)

    # === Patas traseras (más grandes y visibles) ===
    for i, x in enumerate([-0.6, 0.6]):
        glPushMatrix()
        glTranslatef(x, -0.25, 0.1)
        angle = 25 if i == 0 else 25  # izquierda / derecha
        glRotatef(angle, 1, 0, 0)

        glPushMatrix()
        glScalef(1.2, 0.5, 1.5)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, 0.4, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()

        glPopMatrix()

    # === Patas delanteras (más pequeñas y al frente) ===
    for i, x in enumerate([-0.4, 0.4]):
        glPushMatrix()
        glTranslatef(x, -0.4, 0.7)
        angle = 60 if i == 0 else 60
        glRotatef(angle, 1, 0, 0)

        glPushMatrix()
        glScalef(1.0, 0.4, 1.0)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, 0.22, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()

        glPopMatrix()

    glDisable(GL_TEXTURE_2D)


def draw_nenufar():
    glPushMatrix()
    glTranslatef(0.0, -1.0, 0.0)  # Posición justo debajo de la rana
    glRotatef(-90, 1, 0, 0)       # Acostado en el plano XZ

    inner_radius = 0.0
    outer_radius = 1.9
    height = 0.15  # altura del borde

    num_segments = 100
    # Parte superior del nenúfar (base circular)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.5, 1.0, 0.5)  # verde claro
    glVertex3f(0.0, 0.0, 0.0)  # centro
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x = outer_radius * math.cos(angle)
        y = outer_radius * math.sin(angle)
        glVertex3f(x, y, 0.0)
    glEnd()

    # Parte vertical (como la tubería alrededor)
    glBegin(GL_QUAD_STRIP)
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x = outer_radius * math.cos(angle)
        y = outer_radius * math.sin(angle)

        # Interior del borde
        glColor3f(0.4, 0.9, 0.4)
        glVertex3f(x, y, 0.0)
        # Exterior del borde
        glColor3f(0.3, 0.8, 0.3)
        glVertex3f(x, y, height)
    glEnd()

    glPopMatrix()


def draw_hongo():
    # === Tallo ===
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.9)  # Blanco hueso
    glTranslatef(0.0, 1.3, 0.0)  # Altura del tallo aumentada
    glScalef(0.9, 1.5, 0.9)  # Más grueso y alto
    glutSolidSphere(1.0, 30, 30)
    glPopMatrix()

    # === Sombrero: semiesfera roja ===
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Rojo intenso
    glTranslatef(0.0, 2.7, 0.0)  # Posición del sombrero
    glRotatef(-90, 1, 0, 0)  # Semiesfera mirando hacia abajo
    quad = gluNewQuadric()
    gluPartialDisk(quad, 0, 1.2, 30, 1, 0, 180)  # Base semiesfera un poco más grande
    gluDeleteQuadric(quad)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(0.0, 2.7, 0.0)
    glScalef(1.4, 0.7, 1.4)  # Esfera más pequeña y aplastada
    glutSolidSphere(1.0, 30, 30)
    glPopMatrix()

    # === Puntitos blancos sobre el sombrero ===
    glColor3f(1.0, 1.0, 1.0)
    puntos = [
        (0.0, 3.05, 0.0),
        (0.35, 3.0, 0.2),
        (-0.25, 2.95, -0.25),
        (0.2, 2.95, -0.3),
        (-0.4, 3.0, 0.1),
    ]
    for x, y, z in puntos:
        glPushMatrix()
        glTranslatef(x, y, z)
        glutSolidSphere(0.07, 10, 10)
        glPopMatrix()






def draw_mushroom_field(num_mushrooms=75, terreno_size=30, exclusion_radius=8.0):
    random.seed(42)
    mushrooms_drawn = 0
    intentos = 0
    max_intentos = num_mushrooms * 10

    while mushrooms_drawn < num_mushrooms and intentos < max_intentos:
        intentos += 1
        x = random.uniform(-terreno_size, terreno_size)
        z = random.uniform(-terreno_size, terreno_size)
        distancia = (x**2 + z**2)**0.5

        if distancia > exclusion_radius:
            y = -1.0
            scale = random.uniform(0.7, 1.3)

            glPushMatrix()
            glTranslatef(x, y, z)

            # === SOMBRA FALSA ===
            glPushMatrix()
            glDisable(GL_LIGHTING)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(0.0, 0.0, 0.0, 0.3)
            glTranslatef(0.0, 0.01 + 0.72, 0.0)
            glScalef(1.4, 1.0, 1.4)
            glRotatef(-90, 1, 0, 0)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0.0, 0.0, 0.0)
            for angle in range(0, 361, 10):
                rad = math.radians(angle)
                glVertex3f(math.cos(rad), math.sin(rad), 0.0)
            glEnd()
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glPopMatrix()
            # ====================

            glScalef(scale, scale, scale)
            draw_hongo()
            glPopMatrix()

            mushrooms_drawn += 1

def draw_nube():
    glColor3f(1.0, 1.0, 1.0)
    for offset in [
        (-2, 0, 0), (0, 0, 0), (2, 0, 0),
        (-1, 1, 0), (1, 1, 0)
    ]:
        glPushMatrix()
        glTranslatef(offset[0], offset[1], offset[2])
        glutSolidSphere(2.0, 16, 16)
        glPopMatrix()

def draw_nubes_en_el_cielo():
    glPushMatrix()
    posiciones = [
        (-30, 10, -20),
        (0, 12, -40),
        (40, 11, -10),
        (-45, 9, 30),
    ]
    for pos in posiciones:
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(1.5, 1.0, 1.0)
        draw_nube()
        glPopMatrix()
    glPopMatrix()



def draw_frog():
    draw_body()
    draw_panza()
    draw_eyes()
    draw_legs()
    draw_cejas()
    draw_boca()


def draw_sol():
    glPushMatrix()
    # Material con emisión amarilla para que parezca brillante
    emission = [1.0, 1.0, 0.0, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emission)
    glColor3f(1.0, 1.0, 0.0)
    glutSolidSphere(5.0, 32, 32)
    # Quitar emisión para otros objetos después
    no_emission = [0.0, 0.0, 0.0, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, no_emission)
    glPopMatrix()


# ---------- Callbacks de GLUT ----------
def display():
    tiempo = time.time()
    angulo_rotacion = (tiempo * 5) % 360  # Rota lento (5 grados por segundo)
    angulo_sol = (tiempo * 10) % 360 




    global cap, ref_pos, ref_pixel_pos

    ret, frame = cap.read()
    if not ret:
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            controlar_camara(hand_landmarks, frame)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        if ref_pixel_pos is not None:
            cv2.circle(frame, ref_pixel_pos, 10, (0, 0, 255), -1)
    else:
        ref_pos = None
        ref_pixel_pos = None

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Prueba cámara fija para asegurar que se vean las nubes (ajusta si quieres cámara dinámica)
    # gluLookAt(0, 35, 60, 0, 0, 0, 0, 1, 0)
    # O usa tu cámara controlada:
    gluLookAt(*camera_pos, *camera_target, *camera_up)


   # Dibuja el sol en movimiento
        # Dibuja el sol en movimiento
    glPushMatrix()
    radio_orbita = 50
    x_sol = radio_orbita * math.cos(math.radians(angulo_sol))
    y_sol = 11  # Bajamos el sol para que esté a la altura de las nubes
    z_sol = radio_orbita * math.sin(math.radians(angulo_sol))
    glTranslatef(x_sol, y_sol, z_sol)
    light_pos = [x_sol, y_sol, z_sol, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    draw_sol()
    glPopMatrix()




    
    # Dibuja el suelo
    glPushMatrix()
    glTranslatef(0.0, 0.7, 0.0)
    draw_ground()
    glPopMatrix()

    # Dibuja hongos
    draw_mushroom_field()

    # Dibuja nubes
    draw_nubes_en_el_cielo()

    # Nenúfar, rana y agua rotando juntos
    glPushMatrix()
    glTranslatef(0.0, 0.85, 0.0)
    glRotatef(-angulo_rotacion, 0, 1, 0)

    glPushMatrix()
    glTranslatef(0.0, -0.91, 0.0)  # Agua justo debajo del nenúfar
    draw_agua()
    glPopMatrix()

    draw_nenufar()

    glPushMatrix()
    glTranslatef(0.0, -0.35, 0.0)
    draw_frog()
    glPopMatrix()

    glPopMatrix()
 




    glutSwapBuffers()

    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w)/h if h else 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    if key == b'\x1b' or key == b'q':  # ESC o 'q' para salir
        sys.exit()


# ---------- Inicialización ----------

def init_glut():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Rana 3D Cartoon - PyOpenGL")

    
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    # Activar iluminación y permitir uso de colores
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    ambient_color = [0.05, 0.05, 0.15, 1.0]  # luz ambiental azulada tenue
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_color)


    #desactivar o activar luz ambiental 
    light_color = [1.0, 1.0, 0.9, 1.0]  # Luz difusa blanca cálida, tipo luz solar
    light_pos = [10.0, 20.0, 10.0, 1.0]  # Luz desde arriba, simulando el sol
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    ambient_light = [0.3, 0.3, 0.35, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)
    



    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Fondo
    glClearColor(0.53, 0.81, 0.98, 1.0)  # Azul celeste claro para el cielo de día



    # Callbacks
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)


if __name__ == "__main__":
    init_glut()
    # Al final de init_glut(), antes de los callbacks
global textura_panza
glEnable(GL_TEXTURE_2D)
textura_cuerpo = load_texture("cuerpo.png")
textura_panza = load_texture("Textura_amarilla.bmp")
textura_ceja = load_texture("ceja.png")
img = cv2.imread("a6f4e21f350bce6cb610412175317ee8.jpg")
img2 = cv2.resize(img, (512, 512))
cv2.imwrite("temp_textura.jpg", img2)

textura_terreno = load_texture("temp_textura.jpg")  # aquí sí funciona bien
 # el archivo que tengas de pasto/textura para terreno


display_list_pasto = crear_display_list_pasto()

glutMainLoop()

```