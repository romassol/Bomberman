from abc import ABCMeta, abstractmethod


class Prize:
    __metaclass__ = ABCMeta

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return '{}'.format(self.position)

    @abstractmethod
    def intersection_with_bm(self, bm):
        """Intersection of a prize with BomberMan"""
