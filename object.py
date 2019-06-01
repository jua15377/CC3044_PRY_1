import struct

def try_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val


class Obj(object):
    def __init__(self, filename):
        print('reading obj')
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices  = []
        self.vfaces = []
        self.vnomals = []
        self.read()


    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.vfaces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])
                elif prefix == 'vt':
                    self.tvertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.vnomals.append(list(map(float, value.split(' '))))


class Texture(object):
    def __init__(self, path):
        self.path = path
        self.pixels = []
        print('loading texture...')
        self.read()

    def read(self):
        image = open(self.path, "rb")
        # ignore header
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)
        # get bmp dimmensions
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        image.seek(header_size)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(bytes([b, g, r]))
        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        # print(self.pixels[y][x])
        try:
            return bytes(map(lambda b: int(b * intensity) if b * intensity > 0 else 0, self.pixels[y][x]))
        except:
            pass