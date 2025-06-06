# tetera.py

Renderiza una tetera utilizando OpenGL

```python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glBegin(GL_LINES)
    # Eje X - Rojo
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(2.0, 0.0, 0.0)

    # Eje Y - Verde
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 2.0, 0.0)

    # Eje Z - Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 2.0)
    glEnd()

    glColor3f(0.5, 0.5, 0.5)  # Gris
    glutWireTeapot(0.5)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OpenGL Tetera y Ejes")
    
    glEnable(GL_DEPTH_TEST)
    
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()

```