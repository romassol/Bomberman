import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other):
        self.x += other.x
        self.y += other.y

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Point):
            return other.x == self.x and other.y == self.y
        return False

    def __str__(self):
        return '{} {}'.format(self.x, self.y)
