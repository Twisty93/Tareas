# Ajedrez piezas.py

Este programa muestra piezas de ajedrez en 3D con OpenGL.
Las piezas se dibujan sobre un tablero con texturas y formas básicas.
Puedes mover la cámara con W, A, S, D, ↑ y ↓.

```python
import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere
import sys

camera_pos = [4.0, 3.0, 8.0]
camera_target = [0.0, 1.0, 0.0]
camera_up = [0.0, 1.0, 0.0]
camera_speed = 0.2
keys = {}

def init():
        glClearColor(0.5, 0.8, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60, 1.0, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

def draw_tablero():
        
        size = 1.0
        glPushMatrix()
        glTranslatef(-4, 0, -4)  
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    glColor3f(1.0, 1.0, 1.0)  # Blanco
                else:
                    glColor3f(0.2, 0.2, 0.2)  # Negro
                glBegin(GL_QUADS)
                glVertex3f(i * size, 0, j * size)
                glVertex3f((i + 1) * size, 0, j * size)
                glVertex3f((i + 1) * size, 0, (j + 1) * size)
                glVertex3f(i * size, 0, (j + 1) * size)
                glEnd()
        glPopMatrix()

def draw_peon():

        quad = gluNewQuadric()
        glPushMatrix()

   
        glColor3f(0.2, 0.2, 0.8)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.3, 0.3, 1.0, 40, 40) 
        glPopMatrix()

      
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0)  
        gluSphere(quad, 0.4, 32, 32)
        glPopMatrix()

        glPopMatrix()

def draw_rey():
        
        quad = gluNewQuadric()
        glPushMatrix()


        glColor3f(0.2, 0.2, 0.8)  # color azul oscuro
        glPushMatrix()
        glTranslatef(0.0, 0.4, 0.0)
        gluSphere(quad, 0.4, 32, 32)
        glPopMatrix()

        
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0)
        gluSphere(quad, 0.3, 32, 32)
        glPopMatrix()

        
        glPushMatrix()
        glTranslatef(0.0, 1.5, 0.0)
        gluSphere(quad, 0.25, 32, 32)
        glPopMatrix()

        
        glColor3f(1.0, 1.0, 0.0)  # amarillo
        crown_radius = 0.25
        crown_height = 1.75
        for i in range(6):
            angle = i * (360 / 6)
            x = crown_radius * math.cos(math.radians(angle))
            z = crown_radius * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, crown_height, z)
            gluSphere(quad, 0.05, 16, 16)
            glPopMatrix()

        glPopMatrix()

def draw_reina():
       
        quad = gluNewQuadric()
        glPushMatrix()

        
        glColor3f(0.0, 0.5, 1)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.4, 0.4, 1.0, 16, 16)
        glPopMatrix()

    
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.3, 0.3, 0.4, 16, 16)
        glPopMatrix()

    
        glPushMatrix()
        glTranslatef(0.0, 1.4, 0.0)
        gluSphere(quad, 0.35, 16, 16)
        glPopMatrix()

       
        glColor3f(1.0, 1.0, 0.0)
        crown_radius = 0.25
        crown_height = 1.7
        for i in range(6):
            angle = i * (360 / 6)
            x = crown_radius * math.cos(math.radians(angle))
            z = crown_radius * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, crown_height, z)
            gluSphere(quad, 0.05, 16, 16)
            glPopMatrix()

        glPopMatrix()

def draw_alfil():
        quad = gluNewQuadric()
        glPushMatrix()

        
        glColor3f(0.2, 0.5, 0.2)  
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)   

        gluCylinder(quad, 0.35, 0.25, 1.0, 40, 40)
        glPopMatrix()

        
        glPushMatrix()
        glTranslatef(0.0, 1.0, 0.0)
        gluSphere(quad, 0.3, 32, 32)
        glPopMatrix()

        
        glColor3f(0.1, 0.4, 0.1) 
        glPushMatrix()
        glTranslatef(0.0, 1.05, 0.15)
        glRotatef(45, 0, 0, 1)
        gluCylinder(quad, 0.1, 0.1, 0.4, 20, 20)
        glPopMatrix()

        glPopMatrix()

def draw_caballo():

        quad = gluNewQuadric()
        glPushMatrix()

        glColor3f(0.5, 0.35, 0.1)  # color marrón
        glPushMatrix()
        glTranslatef(0.0, 0.4, 0.0)
        glRotatef(-90, 1, 0, 0)  # orientar cilindro vertical
        gluCylinder(quad, 0.2, 0.2, 0.8, 40, 40)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 1.15, 0.0)
        glRotatef(-60, 1, 0, 0)
        gluCylinder(quad, 0.12, 0.1, 0.5, 32, 32)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 1.4, 0.25)
        gluSphere(quad, 0.18, 32, 32)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.1, 1.55, 0.2)
        gluSphere(quad, 0.05, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.1, 1.55, 0.2)
        gluSphere(quad, 0.05, 16, 16)
        glPopMatrix()

        glPopMatrix()

def draw_rook():
        quad = gluNewQuadric()
        glPushMatrix()

        
        glColor3f(0.4, 0.4, 0.4) 
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(quad, 0.4, 0.4, 1.2, 40, 40)
        glPopMatrix()

       
        glPushMatrix()
        glTranslatef(0.0, 1.2, 0.0)
        gluSphere(quad, 0.35, 32, 32)
        glPopMatrix()

        
        glColor3f(0.2, 0.2, 0.2)
        for i in range(4):
            angle = i * 90
            x = 0.3 * math.cos(math.radians(angle))
            z = 0.3 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, 1.35, z)
            glScalef(0.1, 0.1, 0.1)
            
            glPopMatrix()

        glPopMatrix()


def draw_scene():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                camera_target[0], camera_target[1], camera_target[2],
                camera_up[0], camera_up[1], camera_up[2])

        draw_tablero()

        
        glPushMatrix()
        glTranslatef(-2 + 1.0, 0.0, -2 + 1.0) 
        draw_peon()
        glPopMatrix()

        
        glPushMatrix()
        glTranslatef(2 + 1.0, 0.0, 2 + 1.0)
        draw_reina()
        glPopMatrix()


        glPushMatrix()
        glTranslatef(1 , 0.0, 2 )
        draw_rook()
        glPopMatrix()


        glPushMatrix()
        glTranslatef(0 , 0.0, 2 )
        draw_rey()
        glPopMatrix()


        glPushMatrix()
        glTranslatef(-2 , 0, 2 )
        draw_alfil()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-1 , 0, 2 )
        draw_caballo()
        glPopMatrix()
        glfw.swap_buffers(window)


def process_input():
        global camera_pos

        if keys.get(glfw.KEY_W, False): camera_pos[2] -= camera_speed
        if keys.get(glfw.KEY_S, False): camera_pos[2] += camera_speed
        if keys.get(glfw.KEY_A, False): camera_pos[0] -= camera_speed
        if keys.get(glfw.KEY_D, False): camera_pos[0] += camera_speed
        if keys.get(glfw.KEY_UP, False): camera_pos[1] += camera_speed
        if keys.get(glfw.KEY_DOWN, False): camera_pos[1] -= camera_speed

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
        window = glfw.create_window(width, height, "Peón en Tablero de Ajedrez", None, None)
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