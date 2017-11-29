from unittest import TestCase, main

from game import Game


class TestGame(TestCase):

    def test_get_scoring(self):
        game = Game(["level4.txt", "level3.txt"])
        for b in game.get_current_level().BomberMan:
            bm = b
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        self.assertEqual(20, game.get_scoring())
        game.try_go_to_the_next_level()
        for b in game.get_current_level().BomberMan:
            bm = b
        for i in range(2):
            game.get_current_level().moving('l', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('u', bm)
        game.get_current_level().explode_bomb(index)
        self.assertEqual(110, game.get_scoring())

    def test_get_current_level(self):
        game = Game(["level4.txt", "level3.txt"])
        for b in game.get_current_level().BomberMan:
            bm = b
        self.assertEqual(game.levels[0], game.get_current_level())
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        game.try_go_to_the_next_level()
        self.assertEqual(game.levels[1], game.get_current_level())

    def test_try_go_to_the_next_level(self):
        game = Game(["level4.txt", "level3.txt"])
        for b in game.get_current_level().BomberMan:
            bm = b
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        self.assertFalse(game.try_go_to_the_next_level())
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        self.assertTrue(game.try_go_to_the_next_level())

    def test_is_current_level_last(self):
        game = Game(["level4.txt", "level3.txt"])
        for b in game.get_current_level().BomberMan:
            bm = b
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        self.assertFalse(game.is_current_level_last())
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        game.try_go_to_the_next_level()
        self.assertTrue(game.is_current_level_last())

    def test_is_over(self):
        game = Game(["level4.txt", "level3.txt"])
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().explode_bomb(index)
        self.assertTrue(game.is_over())

    def test_is_win(self):
        game = Game(["level4.txt", "level4.txt"])
        for b in game.get_current_level().BomberMan:
            bm = b
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        game.try_go_to_the_next_level()
        for b in game.get_current_level().BomberMan:
            bm = b
        game.get_current_level().moving('l', bm)
        game.get_current_level().moving('u', bm)
        index = game.get_current_level().put_bomb_and_get_bomb_index()
        game.get_current_level().moving('r', bm)
        game.get_current_level().moving('d', bm)
        game.get_current_level().explode_bomb(index)
        self.assertTrue(game.is_win())


if __name__ == '__main__':
    main()
