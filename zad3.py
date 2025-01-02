import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

R = 5.0

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

# Wybor skladowej swiatla do zmiany
element_to_change = 1


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


def render(time):
    global theta, phi, R, light_position

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    x_s = R * np.cos(theta * np.pi / 180) * np.cos(phi * np.pi / 180)
    y_s = R * np.sin(phi * np.pi / 180)
    z_s = R * np.sin(theta * np.pi / 180) * np.cos(phi * np.pi / 180)

    glTranslate(x_s, y_s, z_s)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    light_position[0] = x_s
    light_position[1] = y_s
    light_position[2] = z_s
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

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


def increase_element(element_to_change):
    global light_ambient, light_diffuse, light_specular

    if element_to_change == 1:
        light_ambient[0] = light_ambient[0] + 0.1
        light_ambient[0] = min(light_ambient[0], 1.0)
        print(light_ambient)
    elif element_to_change == 2:
        light_ambient[1] = light_ambient[1] + 0.1
        light_ambient[1] = min(light_ambient[1], 1.0)
        print(light_ambient)
    elif element_to_change == 3:
        light_ambient[2] = light_ambient[2] + 0.1
        light_ambient[2] = min(light_ambient[2], 1.0)
        print(light_ambient)
    if element_to_change == 4:
        light_diffuse[0] = light_diffuse[0] + 0.1
        light_diffuse[0] = min(light_diffuse[0], 1.0)
        print(light_diffuse)
    elif element_to_change == 5:
        light_diffuse[1] = light_diffuse[1] + 0.1
        light_diffuse[1] = min(light_diffuse[1], 1.0)
        print(light_diffuse)
    elif element_to_change == 6:
        light_diffuse[2] = light_diffuse[2] + 0.1
        light_diffuse[2] = min(light_diffuse[2], 1.0)
        print(light_diffuse)
    if element_to_change == 7:
        light_specular[0] = light_specular[0] + 0.1
        light_specular[0] = min(light_specular[0], 1.0)
        print(light_specular)
    elif element_to_change == 8:
        light_specular[1] = light_specular[1] + 0.1
        light_specular[1] = min(light_specular[1], 1.0)
        print(light_specular)
    elif element_to_change == 9:
        light_specular[2] = light_specular[2] + 0.1
        light_specular[2] = min(light_specular[2], 1.0)
        print(light_specular)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def decrease_element(element_to_change):
    global light_ambient, light_diffuse, light_specular

    if element_to_change == 1:
        light_ambient[0] = light_ambient[0] - 0.1
        light_ambient[0] = max(light_ambient[0], 0.0)
        print(light_ambient)
    elif element_to_change == 2:
        light_ambient[1] = light_ambient[1] - 0.1
        light_ambient[1] = max(light_ambient[1], 0.0)
        print(light_ambient)
    elif element_to_change == 3:
        light_ambient[2] = light_ambient[2] - 0.1
        light_ambient[2] = max(light_ambient[2], 0.0)
        print(light_ambient)
    if element_to_change == 4:
        light_diffuse[0] = light_diffuse[0] - 0.1
        light_diffuse[0] = max(light_diffuse[0], 0.0)
        print(light_diffuse)
    elif element_to_change == 5:
        light_diffuse[1] = light_diffuse[1] - 0.1
        light_diffuse[1] = max(light_diffuse[1], 0.0)
        print(light_diffuse)
    elif element_to_change == 6:
        light_diffuse[2] = light_diffuse[2] - 0.1
        light_diffuse[2] = max(light_diffuse[2], 0.0)
        print(light_diffuse)
    if element_to_change == 7:
        light_specular[0] = light_specular[0] - 0.1
        light_specular[0] = max(light_specular[0], 0.0)
        print(light_specular)
    elif element_to_change == 8:
        light_specular[1] = light_specular[1] - 0.1
        light_specular[1] = max(light_specular[1], 0.0)
        print(light_specular)
    elif element_to_change == 9:
        light_specular[2] = light_specular[2] - 0.1
        light_specular[2] = max(light_specular[2], 0.0)
        print(light_specular)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)



def keyboard_key_callback(window, key, scancode, action, mods):
    global element_to_change

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_1 and action == GLFW_PRESS: # ambient, R
        element_to_change = 1
    elif key == GLFW_KEY_2 and action == GLFW_PRESS: # ambient, G
        element_to_change = 2
    elif key == GLFW_KEY_3 and action == GLFW_PRESS: # ambient, B
        element_to_change = 3
    elif key == GLFW_KEY_4 and action == GLFW_PRESS: # diffuse, R
        element_to_change = 4
    elif key == GLFW_KEY_5 and action == GLFW_PRESS: # diffuse, G
        element_to_change = 5
    elif key == GLFW_KEY_6 and action == GLFW_PRESS: # diffuse, B
        element_to_change = 6
    elif key == GLFW_KEY_7 and action == GLFW_PRESS: # specular, R
        element_to_change = 7
    elif key == GLFW_KEY_8 and action == GLFW_PRESS: # specular, G
        element_to_change = 8
    elif key == GLFW_KEY_9 and action == GLFW_PRESS: # specular, B
        element_to_change = 9
    elif key == GLFW_KEY_UP and action == GLFW_PRESS: # zwiekszenie
        increase_element(element_to_change)
    elif key == GLFW_KEY_DOWN and action == GLFW_PRESS: # zmniejszenie
        decrease_element(element_to_change)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old, delta_y, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


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
