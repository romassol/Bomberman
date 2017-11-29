from level import Level


class Game:
    def __init__(self, levels_name):
        self.levels = []
        for level_name in levels_name:
            self.levels.append(Level(level_name))
        self.current_level_index = 0
        self.points = 0

    def get_scoring(self):
        return self.points + self.get_current_level().points

    def get_current_level(self):
        return self.levels[self.current_level_index]

    def try_go_to_the_next_level(self):
        if self.levels[self.current_level_index].is_win() and\
                not self.is_current_level_last():
            self.points += self.get_current_level().points
            self.current_level_index += 1
            return True
        return False

    def is_current_level_last(self):
        return self.current_level_index == len(self.levels) - 1

    def is_over(self):
        return self.levels[self.current_level_index].is_over

    def is_win(self):
        return self.is_current_level_last() and\
               self.levels[self.current_level_index].is_win()
