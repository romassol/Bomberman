from unittest import TestCase, main
import copy
from game import Game
from point import Point
from bomberman import BomberMan
from wall import Wall
from monster import Monster


class TestGame(TestCase):

    def test_moving_bm_forbidden(self):
        g = Game('level1.txt')
        for b in g.BomberMan:
            bm = b
        old_position = copy.deepcopy(bm.position)
        g.moving('d', bm)
        self.assertEqual(bm.position, old_position)
        g.moving('l', bm)
        self.assertEqual(bm.position, old_position)
        g.moving('u', bm)
        self.assertEqual(bm.position, old_position)
        g.moving('r', bm)
        g.moving('r', bm)
        g.moving('d', bm)
        g.moving('d', bm)
        g.moving('r', bm)
        g.moving('r', bm)
        self.assertEqual(bm.position, Point(4, 2))
        old_position = copy.deepcopy(bm.position)
        g.moving('r', bm)
        self.assertEqual(bm.position, old_position)

    def test_moving_bm_allowed(self):
        g = Game('level1.txt')
        for b in g.BomberMan:
            bm = b
        g.moving('r', bm)
        self.assertEqual(bm.position, Point(1, 0))
        g.moving('r', bm)
        self.assertEqual(bm.position, Point(2, 0))
        g.moving('d', bm)
        self.assertEqual(bm.position, Point(2, 1))
        g.moving('d', bm)
        self.assertEqual(bm.position, Point(2, 2))
        g.moving('r', bm)
        self.assertEqual(bm.position, Point(3, 2))
        g.moving('l', bm)
        self.assertEqual(bm.position, Point(2, 2))
        g.moving('u', bm)
        self.assertEqual(bm.position, Point(2, 1))

    def test_bm_is_dead(self):
        g = Game('level1.txt')
        for b in g.BomberMan:
            bm = b
        old_lives = copy.deepcopy(bm.count_of_lives)
        g.moving('r', bm)
        g.moving('r', bm)
        g.moving('d', bm)
        g.moving('d', bm)
        g.moving('l', bm)
        g.is_monster_kill_BM()
        self.assertEqual(bm.count_of_lives, old_lives - 1)
        g.moving('r', bm)
        g.moving('l', bm)
        g.is_monster_kill_BM()
        self.assertEqual(bm.count_of_lives, old_lives - 2)
        g.moving('r', bm)
        g.moving('l', bm)
        g.is_monster_kill_BM()
        self.assertEqual(bm.count_of_lives, old_lives - 3)
        self.assertTrue(g.is_game_over)

    def test_bomb(self):
        g = Game('level1.txt')
        for b in g.BomberMan:
            bm = b
        g.moving('r', bm)
        g.put_bomb()
        g.explode_bomb(3)
        self.assertEqual(len(g.BomberMan), 0)
        m = {Point(0, 4)}
        w = {Point(0, 1), Point(3, 1), Point(2, 4), Point(4, 3)}
        monster = {f.position for f in g.Monster}
        wall = {f.position for f in g.Wall}
        self.assertTrue(m == monster)
        self.assertTrue(w == wall)


if __name__ == '__main__':
    main()
