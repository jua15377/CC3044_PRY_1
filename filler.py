# adaptado de: http://alienryderflex.com/polygon/
# como saber si un punto esta dentro del poligono
from copy import deepcopy

class polygon:
    def __init__(self,list):
        self.list = deepcopy(list)
        self.polucourners = len(list)
        self.polyX = []
        self.polyY = []
        self.set_values()

    def set_values(self):
        for cord in self.list:
            self.polyX.append(cord[0])
            self.polyY.append(cord[1])

    def point_in_poly(self,x,y):
        j = self.polucourners - 1
        oddNodes = False
        for i in range(self.polucourners):
            if self.polyY[i] < y and self.polyY[j]>= y or  self.polyY[j]< y and self.polyY[i] >= y:
                if self.polyX[i] + (y - self.polyY[i])/(self.polyY[j] - self.polyY[i])*(self.polyX[j] - self.polyX[i])< x:
                    oddNodes = not oddNodes
            j = i
        return oddNodes

