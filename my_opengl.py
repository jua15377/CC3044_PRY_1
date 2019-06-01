import copy
import struct
import math
from collections import namedtuple

from filler import polygon
from object import *
from transform import *

#math functions

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
class vp(object):
    def __init__(self,x, y, width, height):
        self.vp_x = x
        self.vp_y = y
        self.width = width
        self.height = height


def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  # print ('dentro de norm',v0)
  v0length = length(v0)
  if not v0length:
    return V3(0, 0, 0)
  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()
  return V2(int(xs[0]), int(ys[0])), V2(int(xs[-1]), int(ys[-1]))

def barycentric(A, B, C, P):
  bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x),
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(bary[2]) < 1:
    return -1, -1, -1   # this triangle is degenerate, return anything outside

  return (
    1 - (bary[0] + bary[1]) / bary[2],
    bary[1] / bary[2],
    bary[0] / bary[2]
  )



def char(c):
    return struct.pack("=c",c.encode('ascii'))


def word(w):
    return struct.pack("=h",w)


def dword(d):
    return struct.pack("=l",d)


def color(r, g, b):
    # return bytes([r, g, b]) verde
    return bytes([b, g, r])
    # return bytes([g, r, b])


my_scene = None
vp_x = None
vp_y = None
vp_height = None
vp_width = None
the_vp = None
COLOR = 255
FILENAME = "out.bmp"


def set_filename(name):
    global FILENAME
    FILENAME = name


def glInit():
    pass


# la imagen resultante va a ser de este size
def glCreateWindow(width, height):
    global my_scene
    my_scene = Bitmap(width, height)


def glViewPort(x, y, width, height):
    global vp_x, vp_y, vp_width, vp_height, the_vp
    vp_x = x
    vp_y = y
    vp_width = width
    vp_height = height
    the_vp = vp(x, y, width, height)


def glClearColor(r, g, b):
    global my_scene
    newR = int(math.ceil(r * 255))
    newG = int(math.ceil(g * 255))
    newB = int(math.ceil(b * 255))
    # print("debug color RGB: %d, %d, %d" % (newR, newG, newB))
    my_scene.clear_color = color(newR, newG, newB)


def glClear():
    global my_scene
    my_scene.clear()


def glVertex(x, y):
    global my_scene, vp_x, vp_y, vp_width, vp_height
    xwin = int((x + 1) * vp_width * 0.5 + vp_x)
    ywin = int((y + 1) * vp_height * 0.5 + vp_y)
    # print("debug glVertex x: %d, y: %d" % (xwin, ywin))

    my_scene.point(xwin, ywin)

def glColor(r, g, b):
    global my_scene
    newR = int(math.ceil(r * 255))
    newG = int(math.ceil(g * 255))
    newB = int(math.ceil(b * 255))
    # print("debug vertex color RGB: %d, %d, %d" % (newR, newG, newB))
    my_scene.vertex_color = color(newR, newG, newB)


def line(x1, y1, x2, y2):
    global my_scene
    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if (x1 > x2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx
    y = y1
    inc = 1 if y2 > y1 else -1
    for x in range(x1, x2 + 1):
        if steep:
            my_scene.point(y, x)
        else:
            my_scene.point(x, y)

        offset += dy * 2
        if offset >= threshold:
            y += inc
            threshold += 2 * dx


def glLine(x1, y1, x2, y2):
    global my_scene, vp_x, vp_y, vp_width, vp_height
    xwin1 = int((x1 + 1) * vp_width * 0.5 + vp_x)
    ywin1 = int((y1 + 1) * vp_height * 0.5 + vp_y)
    xwin2 = int((x2 + 1) * vp_width * 0.5 + vp_x)
    ywin2 = int((y2 + 1) * vp_height * 0.5 + vp_y)
    line(xwin1, ywin1, xwin2, ywin2)

def glFinish():
    global my_scene
    my_scene.write(FILENAME)

def glFinish_z():
    global my_scene
    print('rendering z-buffer..')
    my_scene.write('zbuffer.bmp')

def glFinish_texure():
    global my_scene
    print('rendering vertext over texure..')
    my_scene.write('text_vertex.bmp')

def glLoad(name, texture_name=None, move=(0,0,0), rotation=0, axis='x', rescale=(100,100,100), camara=(0,0,200), where_to_look=(0,0,0)):
    global my_scene
    if texture_name is not None:
        texture = Texture(texture_name)
        my_scene.load(name, move, rotation, axis, rescale, camara, where_to_look, texture=texture)
    else:
        my_scene.load(name, move, rotation, axis, rescale, camara, where_to_look)


def gl_paint():
    global my_scene
    for x in range(my_scene.height):
        can_paint = False
        for y in range(my_scene.width):
            if my_scene.pixels[x][y] == my_scene.vertex_color:
                can_paint = not can_paint
            if can_paint:
                my_scene.pixels[x][y] = my_scene.vertex_color

def gl_paint_v2(list):
    global my_scene
    my_poly = polygon(list)
    for x in range(my_scene.height):
        for y in range(my_scene.width):
            if my_poly.point_in_poly(x, y):
                my_scene.point(x, y)

class Bitmap(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pixels = []
        self.texture = None
        self.clear_color = color(51,102,0)
        self.vertex_color = color(0,0,0)
        self.clear()

    def clear(self):
        self.pixels = [
            [self.clear_color for x in range(self.width+1)]
            for y in range(self.height+1)
        ]
        self.zbuffer = [
            [-float('inf') for x in range(self.width+1 )]
            for y in range(self.height+1)
        ]
        self.zbuffer_color = [
            [color(0,0,0) for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self,filename="out.bmp"):
        f = open(filename,'bw')
        #file header (14)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header (40)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))

        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])
        f.close()
        print("Finish!")



    def point(self, x, y):
        try:
            self.pixels[y][x]= self.vertex_color
        except IndexError:
            print('IndexError', x, y)


    def triangle(self, A, B, C, color=None, texture=None, texture_coords=(), normal_cord=(), intensity=1):
        bbox_min, bbox_max = bbox(A, B, C)
        # print('x',bbox_min.x, bbox_max.x)
        # print('y',bbox_min.y, bbox_max.y)

        for x in range(bbox_min.x, bbox_max.x + 1):
            for y in range(bbox_min.y, bbox_max.y + 1):
                w, v, u = barycentric(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue

                if texture:
                    tA, tB, tC = texture_coords
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u

                    color = texture.get_color(tx, ty, intensity)

                z = A.z * w + B.z * v + C.z * u

                if x < self.width and y < self.height and x >=0 and y >=0:
                    if z > self.zbuffer[x][y]:
                        self.vertex_color = color
                        self.point(x, y)
                        self.zbuffer[x][y] = z

    def load(self, file, move, rotation, axis, rescale, camara, where_to_look, texture=None):

        global the_vp
        model = Obj(file)
        light = V3(0, 0, 1)
        for face in model.vfaces:
            vcount = len(face)
            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                a = model.vertices[f1]
                b = model.vertices[f2]
                c = model.vertices[f3]
                A = transform(a, the_vp, move, rotation, axis, rescale, camara, where_to_look)
                B = transform(b, the_vp, move, rotation, axis, rescale, camara, where_to_look)
                C = transform(c, the_vp, move, rotation, axis, rescale, camara, where_to_look)
                # print('new_abc',A,B,C)
                normal = norm(cross(sub(B, A), sub(C, A)))
                intensity = dot(light, normal)
                if not texture:
                    grey = int(255 * intensity)
                    if grey < 0:
                        continue
                #     should call triangle here
                    self.triangle(A, B, C, color(grey, grey, grey))

                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    if len(model.tvertices[t1])==3:
                        tA = V3(*model.tvertices[t1])
                        tB = V3(*model.tvertices[t2])
                        tC = V3(*model.tvertices[t3])
                    else:
                        tA = V2(*model.tvertices[t1])
                        tB = V2(*model.tvertices[t2])
                        tC = V2(*model.tvertices[t3])
                    n1 = face[0][2] - 1
                    n2 = face[1][2] - 1
                    n3 = face[2][2] - 1
                    nA = V3(*model.vnomals[n1])
                    nB = V3(*model.vnomals[n2])
                    nC = V3(*model.vnomals[n3])
                    self.triangle(A, B, C, texture=texture,
                                  texture_coords=(tA, tB, tC),
                                  normal_cord=(nA, nB, nC),
                                  intensity=intensity)




    def load_texture_vertex(self, file,  texture=None):
        print('painting vertex over the texture file...')
        model = Obj(file)
        self.pixels = copy.deepcopy(texture.pixels)
        self.height = texture.height
        self.width = texture.width
        for face in model.vfaces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.tvertices[f1 - 1]
                v2 = model.tvertices[f2 - 1]

                x1, y1 = v1[0], v1[1]
                x2, y2 = v2[0], v2[1]
                glLine(x1, y1, x2, y2)