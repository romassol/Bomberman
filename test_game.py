from unittest import TestCase, main
import copy

from game import Game


class TestGame(TestCase):

    def test_get_scoring(self):
        game = Game(["level1.txt", "level2.txt"])

    def test_get_current_level(self):
        pass

    def test_try_go_to_the_next_level(self):
        pass

    def test_is_current_level_last(self):
        pass

    def test_is_over(self):
        pass

    def test_is_win(self):
        pass


if __name__ == '__main__':
    main()