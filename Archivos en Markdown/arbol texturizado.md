# arbol texturizado.py

Este programa renderiza un árbol 3D utilizando OpenGL y GLFW en Python.
- El tronco del árbol es un cilindro texturizado.
- Las hojas están representadas por esferas texturizadas distribuidas en dos niveles.
- Se utiliza iluminación básica y un suelo plano.
- La cámara puede moverse usando las teclas W, A, S, D, ↑ y ↓.
- Las texturas se cargan desde archivos JPG usando la librería Pillow porque se me hizo un poco mas sencillo de usar.

```python
from PIL import Image
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.2
keys = {}

texture_tronco = None
texture_hoja = None

def init():
    global texture_tronco, texture_hoja

    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [10, 10, 10, 1.0]
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

    texture_tronco = load_texture("tronco.jpg")
    texture_hoja = load_texture("hoja.jpg")

def load_texture(filename):
    img = Image.open(filename).convert("RGB")
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture_id

def draw_trunk():
    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_tronco)
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def draw_foliage():
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_hoja)

    positions = [
        (0.0, 2.0, 0.0), (0.6, 2.2, 0.0), (-0.6, 2.2, 0.0),
        (0.0, 2.2, 0.6), (0.0, 2.2, -0.6), (0.0, 2.8, 0.0)
    ]

    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, 0.7, 32, 32)
        glPopMatrix()

    glDisable(GL_TEXTURE_2D)

def draw_foliage2():
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_hoja)

    positions = [
        (0.0, 1.0, 0.0), (0.6, 1.2, 0.0), (-0.6, 1.2, 0.0),
        (0.0, 1.2, 0.6), (0.0, 1.2, -0.6), (0.0, 1.8, 0.0)
    ]

    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, 0.7, 32, 32)
        glPopMatrix()

    glDisable(GL_TEXTURE_2D)

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

    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_target[0], camera_target[1], camera_target[2],
              camera_up[0], camera_up[1], camera_up[2])

    draw_ground()
    draw_trunk()
    draw_foliage()
    draw_foliage2()

    glfw.swap_buffers(window)

def process_input():
    global camera_pos
    if keys.get(glfw.KEY_W): camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S): camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A): camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D): camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP): camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN): camera_pos[1] -= camera_speed

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False

def main():
    global window

    if not glfw.init():
        sys.exit()

    width, height = 800, 600
    window = glfw.create_window(width, height, "Árbol con Texturas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        process_input()
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

```