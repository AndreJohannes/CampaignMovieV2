import math

def fromAngles(a, b, length):
    a = math.pi * a / 180.
    b = math.pi * b / 180.
    return (length * math.sin(a) * math.sin(b), length * math.sin(a) * math.cos(b), length * math.cos(a))

def getAngles():
    pass

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

