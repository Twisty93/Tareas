import cv2
import mediapipe as mp
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)


camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.1


cap = cv2.VideoCapture(0)

def init_opengl():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_trunk():
    glPushMatrix()
    glColor3f(0.6, 0.3, 0.1)
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)
    glPopMatrix()

def draw_foliage():
    glPushMatrix()
    glColor3f(0.1, 0.8, 0.1)
    glTranslatef(0.0, 2.0, 0.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)
    glPopMatrix()

def draw_ground():
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-10, 0, 10)
    glVertex3f(10, 0, 10)
    glVertex3f(10, 0, -10)
    glVertex3f(-10, 0, -10)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*camera_pos, *camera_target, *camera_up)
    draw_ground()
    draw_trunk()
    draw_foliage()

def mover_camara_por_mano(frame, hand_landmarks):
    global camera_pos

    h, w, _ = frame.shape
    dedos = [(int(landmark.x * w), int(landmark.y * h)) for landmark in hand_landmarks.landmark]

    indice = dedos[8]
    pulgar = dedos[4]

    distancia = np.linalg.norm(np.array(indice) - np.array(pulgar))

    zoom_intensidad = np.interp(distancia, [20, 200], [0.2, -0.2])

    camera_pos[2] += zoom_intensidad  


def main():
    global cap

    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover cámara con mano", None, None)
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
                mover_camara_por_mano(frame, hand_landmarks)

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
