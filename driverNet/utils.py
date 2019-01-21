from basetypes import Vector2
import config as c
import math

def get_line_intersection(p1, p2, p3, p4):
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        x3 = p3.x
        y3 = p3.y
        x4 = p4.x
        y4 = p4.y

        n1 = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
        n2 = det(x1 - x2, x3 - x4, y1 - y2, y3 - y4)

        if(n1 == 0 or n2 == 0):
            return None

        t = det(x1 - x3, x3 - x4, y1 - y3, y3 - y4) / n1
        u = -det(x1 - x2, x1 - x3, y1 - y2, y1 - y3) / n2
        x = x1 + t*(x2 - x1)
        y = y1 + t*(y2 - y1)

        if(t < 0 or t > 1 or u < 0 or u > 1):
            return None

        return Vector2(x, y)

def det(a, b, c, d):
    return a * d - b * c

def clamp(a, b, x):
    return max(a, min(b, x))

def sigmoid(x):
    return 1 / (1 + math.pow(math.e, -x))