import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

# Wartosci dla zrodla swiatla GL_LIGHT1
light1_ambient = [0.0, 0.0, 0.1, 1.0]
light1_diffuse = [0.0, 0.0, 0.8, 1.0]
light1_specular = [0.5, 0.5, 1.0, 1.0]
light1_position = [0.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

N = 30
matrixVectors = np.zeros((N + 1, N + 1, 3))

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)


    glEnable(GL_LIGHT0)

    # Drugie zrodlo swiatla
    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glEnable(GL_LIGHT1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)


def shutdown():
    pass


def generate_egg(n):
    tab = np.zeros((n+1, n+1, 3))

    # Równomierne rozłożenie wartości dla parametrów u i v
    u_values = np.linspace(0.0, 1.0, n+1)
    v_values = np.linspace(0.0, 1.0, n+1)

    # Wypełnianie tablicy współrzędnymi x, y, z dla każdej pary (u, v)
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)
            tab[i, j] = [x, y, z]

    return tab


def calculateNormalVectors():
    global N

    for i in range(0, N + 1):
        for j in range(0, N + 1):
            u = i / N
            v = j / N

            xu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * np.cos(np.pi * v)
            xv = np.pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * np.sin(np.pi * v)
            yu = 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u
            yv = 0
            zu = (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * np.sin(np.pi * v)
            zv = (-np.pi) * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * np.cos(np.pi * v)

            x = yu * zv - zu * yv
            y = zu * xv - xu * zv
            z = xu * yv - yu * xv

            sum = pow(x, 2) + pow(y, 2) + pow(z, 2)
            length = np.sqrt(sum)

            if length > 0:
                x = x / length
                y = y / length
                z = z / length

            matrixVectors[i][j][0] = x
            matrixVectors[i][j][1] = y
            matrixVectors[i][j][2] = z



def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    tab = generate_egg(N)

    glBegin(GL_TRIANGLES)
    for i in range(N):
        for j in range(N):
            # Trójkąt między punktami (i, j), (i+1, j), (i, j+1)
            glNormal3f(matrixVectors[i][j][0], matrixVectors[i][j][1], matrixVectors[i][j][2])
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glNormal3f(matrixVectors[i + 1][j][0], matrixVectors[i + 1][j][1], matrixVectors[i + 1][j][2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])
            glNormal3f(matrixVectors[i][j + 1][0], matrixVectors[i][j + 1][1], matrixVectors[i][j + 1][2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

            # Trójkąt dopełniający - między punktami (i+1, j), (i+1, j+1), (i, j+1)
            glNormal3f(matrixVectors[i + 1][j][0], matrixVectors[i + 1][j][1], matrixVectors[i + 1][j][2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])
            glNormal3f(matrixVectors[i + 1][j + 1][0], matrixVectors[i + 1][j + 1][1], matrixVectors[i + 1][j + 1][2])
            glVertex3f(tab[i + 1, j + 1, 0], tab[i + 1, j + 1, 1], tab[i + 1, j + 1, 2])
            glNormal3f(matrixVectors[i][j + 1][0], matrixVectors[i][j + 1][1], matrixVectors[i][j + 1][2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    calculateNormalVectors()

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
