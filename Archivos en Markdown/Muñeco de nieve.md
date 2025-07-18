# Muñeco de nieve.py

Genera un muñeco de nieve en Glfw

```python
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluNewQuadric, gluSphere, gluPerspective, gluCylinder
import sys

def init():
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Fondo de cielo
    glEnable(GL_DEPTH_TEST)

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_sphere(radius=1, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    glPopMatrix()

def draw_cone(base=0.1, height=0.5, x=0, y=0, z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)  # Orientar el cono hacia adelante
    quadric = gluNewQuadric()
    gluCylinder(quadric, base, 0, height, 32, 32)
    glPopMatrix()

def draw_snowman():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, -1.5, -8)  # Alejar al muñeco de nieve

    # Cuerpo
    glColor3f(1, 1, 1)
    draw_sphere(1.0, 0, 0, 0)     # Base
    draw_sphere(0.75, 0, 1.2, 0)  # Cuerpo medio
    draw_sphere(0.5, 0, 2.2, 0)   # Cabeza

    # Ojos
    glColor3f(0, 0, 0)
    draw_sphere(0.05, -0.15, 2.3, 0.4)  # Ojo izquierdo
    draw_sphere(0.05, 0.15, 2.3, 0.4)   # Ojo derecho

    # Nariz (cono)
    glColor3f(1, 0.5, 0)  # Color naranja
    draw_cone(0.05, 0.2, 0, 2.2, 0.5)  # Nariz

    glfw.swap_buffers(window)

def main():
    if not glfw.init():
        sys.exit()
    
    global window
    window = glfw.create_window(500, 500, "Muñeco de Nieve en OpenGL", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    init()

    while not glfw.window_should_close(window):
        draw_snowman()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
```