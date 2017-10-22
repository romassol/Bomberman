class Wall:
    def __init__(self, point, is_destroyed, passability, prizes=[]):
        self.is_destroyed = is_destroyed
        self.position = point
        self.passability = passability
        self.prizes = prizes

    def __str__(self):
        return '{} {}'.format(self.is_destroyed, self.passability)
