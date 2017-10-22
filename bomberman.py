from bomb import Bomb


class BomberMan:
    def __init__(self, point):
        self.count_of_lives = 3
        self.position = point
        self.backpack = []
        self.action_with_prize = {Bomb: self.take_bomb, 'life': self.add_life}

    def take_prize(self, prize):
        if self.position == prize.position:
            self.action_with_prize[prize.kind](prize.power)

    def take_bomb(self, power):
        self.backpack.append(Bomb(self, power=power))

    def add_life(self, power):
        self.count_of_lives += power