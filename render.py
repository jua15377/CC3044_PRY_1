from my_opengl import *

def draw_line(start_axis, end_axis, step, fix, horientation):
    if horientation == "h":
        while start_axis < end_axis:
            start_axis = start_axis + step
            glVertex(start_axis, fix)
    else:
        while start_axis < end_axis:
            start_axis = start_axis + step
            glVertex(fix, start_axis)


# only works on squares
def draw_diagonal(start_x, end_x, start_y, end_y, step_x, step_y, direction):
    if direction == "up":
        while start_x <= end_x and start_y <= end_y :
            start_x = start_x + step_x
            start_y = start_y + step_y
            glVertex(start_x, start_y)
    else:
        while start_x <= end_x and start_y >= end_y :
            start_x = start_x + step_x
            start_y = start_y - step_y
            glVertex(start_x, start_y)


def normalize_cord(cord, base):
    return (cord - (base*0.5)) /(base*0.5)


def normalize_tuple(tuple, x_value, y_value):
    return normalize_cord(tuple[0], x_value), normalize_cord(tuple[1], y_value)


def normalize_list_of_cords(list, x_value, y_value):
    norm_cord = []
    for tuple in list:
        norm_cord.append(normalize_tuple(tuple, x_value, y_value))
    return norm_cord

def draw_polygon(list):
    for index in range(len(list)):
        if index + 1 != len(list):
            glLine(list[index][0], list[index][1], list[index + 1][0], list[index + 1][1])
        else:
            glLine(list[index][0], list[index][1], list[0][0], list[0][1])

# test load obj
def medium_shot(obj_name):
    # easy filename change
    set_filename("medium_shotDutch Angle.bmp")
    # start
    glInit()
    x = 400
    y = 400
    glCreateWindow(x, y)
    glViewPort(0, 0, x, y)
    glClearColor(0.5, 0.5, 0.5)
    glClear()
    glColor(1, 1, 1)
    glLoad(obj_name, 'fur.bmp', move=(0,-300,150), rescale=(350, 350, 350))
    glFinish()

def run(obj_name):
    # easy filename change
    set_filename("pry_1.bmp")
    # start
    glInit()
    x = 1600
    y = 1600
    glCreateWindow(x, y)
    glViewPort(0, 0, x, y)
    glClearColor(0.5, 0.5, 0.5)
    glClear()
    glColor(1, 1, 1)
    print('object#1, a simple square with the texture of a living room')
    glLoad('back.obj',
           'living.bmp',
           move=(0, 0, -300),
           axis='z',
           rotation=-90,
           rescale=(700, 700, 700)
           )
    print('object#2, a beautiful table with wood texture')
    glLoad('the_table.obj',
           'Wood.bmp',
           move=(0, -300, 600),
           rescale=(90, 90, 90),
           rotation=45,
           axis='y'
           )
    print('object#3, a mounted elephant\'s head with texture')
    glLoad('ele.obj',
           'elefante.bmp',
           move=(0, 250, 600),
           rescale=(190, 190, 190),
           )
    print('object#4, a nice dog with texture')
    glLoad('dog.obj',
           'fur.bmp',
           move=(-400, -400, 500),
           rotation=45,
           axis='y',
           rescale=(180,180,180)
           )
    print('object#5, a confortable leather sofa')
    glLoad('sofa.obj',
           'leather.bmp',
           move=(300, -330, 600),
           rotation=280,
           axis='y',
           rescale=(360, 360, 360)
           )
    glFinish()

# work
file = 'dog.obj'
run(file)

