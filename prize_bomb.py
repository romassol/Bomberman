from prize import Prize
from bomb import Bomb


class Prize_bomb(Prize):
    def __init__(self, power, position):
        super().__init__(position)
        self.power = power

    def activate(self, bm):
        if bm.position == self.position:
            bm.backpack.append(Bomb(self, power=self.power))
            return True
        return False

    def __str__(self):
        return 'position: {}, power: {}'.format(self.position, self.power)
