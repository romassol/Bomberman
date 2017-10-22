class Bomb:
    def __init__(self, player, is_active=False, power=1):
        self.position = player.position
        self.is_active = is_active
        self.power = power
