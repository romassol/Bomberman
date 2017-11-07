from prize import Prize


class PrizeLife(Prize):
    def intersection_with_bm(self, bm):
        if bm.position == self.position:
            bm.count_of_lives += self.count_of_added_lives
            return True
        return False

    def __init__(self, count_of_added_lives, position):
        super().__init__(position)
        self.count_of_added_lives = count_of_added_lives

    # def activate(self, bm):
    #     if bm.position == self.position:
    #         bm.count_of_lives += self.count_of_added_lives
    #         return True
    #     return False

    def __str__(self):
        return 'position: {}, count_of_added_lives: {}'.format(
            self.position, self.count_of_added_lives)