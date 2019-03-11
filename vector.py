import math


class Vector:
    def __init__(self, x, y, z): self.__x, self.__y, self.__z = x, y, z

    @classmethod
    def create(cls, pta, ptb):       # create a Vector from pta to ptb
        x = ptb.x - pta.x
        y = ptb.y - pta.y
        z = ptb.z - pta.z
        return cls(x, y, z)

    def __str__(self): return 'Vector(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'

    def getx(self): return self.__x

    def gety(self): return self.__y

    def getz(self): return self.__z

    def setx(self, x): self.__x = x

    def sety(self, y): self.__y = y

    def setz(self, z): self.__z = z

    x = property(getx, setx)

    y = property(gety, sety)

    z = property(getz, setz)

    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k: float): return Vector(k * self.x, k * self.y, k * self.z)

    def __rmul__(self, k: float): return self.__mul__(k)

    def __neg__(self): return Vector(-self.x, -self.y, -self.z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __imul__(self, k: float):
        self.x *= k
        self.y *= k
        self.z *= k
        return self

    def dot(self, other): return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def magnitudeSquared(self):
        return self.x**2 + self.y**2 + self.z**2

    def toTuple(self):
        return (self.x, self.y)
