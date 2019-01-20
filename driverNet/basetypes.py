import math

class Vector2():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)


    def normalize(self):
        magnitude = self.magnitude(self);
        return Vector2(self.x / magnitude, self.y / magnitude);

    def rotate(self, angle):
        angle *= math.pi / 180
        x = self.x
        y = self.y
        cos = math.cos(angle)
        sin = math.sin(angle)
        self.x = x * cos + y * sin
        self.y = y * cos - x * sin

    def getRotated(self, angle):
        angle *= math.pi / 180
        return Vector2(
            self.x * math.cos(angle) + self.y * math.sin(angle),
            self.y * math.cos(angle) - self.x * math.sin(angle)
        )

    @classmethod
    def magnitude(self, v):
        return math.sqrt(v.x**2 + v.y**2)

    @classmethod
    def dot(self, v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @classmethod
    def angle(self, v1, v2):
        return math.acos(self.dot(v1, v2) / (self.magnitude(v1) * self.magnitude(v2)))

    @classmethod
    def distance(self, v1, v2):
        return math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2)
