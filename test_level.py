from unittest import TestCase, main
import copy

from level import Level
from point import Point
from bomberman import BomberMan
from wall import Wall
from monster import Monster
from bomb import Bomb


class TestLevel(TestCase):

    def test_put_bomb_and_get_bomb_power(self):
        level = Level('level1.txt')
        bomb_power = level.put_bomb_and_get_bomb_power()
        self.assertEqual(Point(1, 1), level.Bomb.position)
        self.assertEqual(1, bomb_power)
        self.assertTrue(level.Bomb.is_active)

    def test_put_bomb_in_backpack_and_get_bomb_power(self):
        level = Level('level1.txt')
        for b in level.BomberMan:
            bm = b
        bm.backpack.append(Bomb(bm, power=2))
        bomb_power = level.put_bomb_and_get_bomb_power()
        self.assertEqual(Point(1, 1), level.Bomb.position)
        self.assertEqual(2, bomb_power)
        self.assertEqual(0, len(bm.backpack))
        self.assertTrue(level.Bomb.is_active)

    def test_get_explode_area(self):
        level = Level('level1.txt')
        level.put_bomb_and_get_bomb_power()
        explode_area = level.get_explode_area()
        self.assertEqual(set([Point(2, 1), Point(1, 2), Point(1, 1)]), explode_area)

    def test_add_available_point_on_Y(self):
        level = Level('level1.txt')
        level.put_bomb_and_get_bomb_power()
        not_destroyed_walls = [w.position for w in level.Wall if not w.is_destroyed]
        points = set()
        range_list = [range(-1, -level.bomb_power - 1, -1), range(level.bomb_power + 1)]
        for p in range_list:
            level.add_available_point_on_Y(not_destroyed_walls, points, p)
        self.assertEqual(set([Point(1, 2), Point(1, 1)]), points)

    def test_add_available_point_on_X(self):
        level = Level('level1.txt')
        level.put_bomb_and_get_bomb_power()
        not_destroyed_walls = [w.position for w in level.Wall if not w.is_destroyed]
        points = set()
        range_list = [range(-1, -level.bomb_power - 1, -1), range(level.bomb_power + 1)]
        for p in range_list:
            level.add_available_point_on_X(not_destroyed_walls, points, p)
        self.assertEqual(set([Point(1, 1), Point(2, 1)]), points)

    def test_explode_bomb(self):
        level = Level('level1.txt')
        for b in level.BomberMan:
            bm = b
        walls = copy.deepcopy(level.Wall)
        monsters = copy.deepcopy(level.Monster)
        previous_monsters_positions = [monster.position for monster in monsters]
        previous_walls_positions = [wall.position for wall in walls if wall.is_destroyed]
        for i in range(4):
            level.moving('r', bm)
        level.put_bomb_and_get_bomb_power()
        level.moving('l', bm)
        level.explode_bomb()
        monsters_positions = [monster.position for monster in level.Monster]
        walls_positions = [wall.position for wall in level.Wall if wall.is_destroyed]
        self.assertFalse(level.Bomb.is_active)
        destroyed_walls = set()
        for w in previous_walls_positions:
            if w not in walls_positions:
                destroyed_walls.add(w)
        killed_monsters = set()
        for m in previous_monsters_positions:
            if m not in monsters_positions:
                killed_monsters.add(m)
        self.assertEqual(set([Point(6, 1), Point(5, 2)]), destroyed_walls)
        self.assertEqual(set([Point(5, 1)]), killed_monsters)
        self.assertEqual(0, len(level.BomberMan))

    def test_delete_character_in_all_sets_and_scoring(self):
        level = Level('level1.txt')
        walls = copy.deepcopy(level.Wall)
        monsters = copy.deepcopy(level.Monster)
        previous_monsters_positions = [monster.position for monster in monsters]
        previous_walls_positions = [wall.position for wall in walls if wall.is_destroyed]
        list_of_characters = [level.BomberMan, level.Monster, level.Wall]
        explode_area = set([Point(6, 1), Point(5, 1), Point(4, 1), Point(5, 2)])
        for point in explode_area:
            level.delete_character_in_all_sets_and_scoring(list_of_characters, point)
        monsters_positions = [monster.position for monster in level.Monster]
        walls_positions = [wall.position for wall in level.Wall if wall.is_destroyed]
        destroyed_walls = set()
        for w in previous_walls_positions:
            if w not in walls_positions:
                destroyed_walls.add(w)
        killed_monsters = set()
        for m in previous_monsters_positions:
            if m not in monsters_positions:
                killed_monsters.add(m)
        self.assertEqual(set([Point(6, 1), Point(5, 2)]), destroyed_walls)
        self.assertEqual(set([Point(5, 1)]), killed_monsters)

    def test_remove_characters_and_scoring_or_gameover(self):
        level = Level('level1.txt')
        destroyed_walls = []
        for w in level.Wall:
            if w.position in [Point(6, 1), Point(5, 2)]:
                destroyed_walls.append(w)
        level.remove_characters_and_scoring_or_gameover(destroyed_walls, level.Wall)
        self.assertEqual(10, level.points)
        killed_monsters = []
        for m in level.Monster:
            if m.position in [Point(5, 1)]:
                killed_monsters.append(m)
        level.remove_characters_and_scoring_or_gameover(killed_monsters, level.Monster)
        self.assertEqual(110, level.points)
        level.remove_characters_and_scoring_or_gameover([bm for bm in level.BomberMan], level.BomberMan)
        self.assertTrue(level.is_over)

    def test_check_on_destroyed(self):
        level = Level('level1.txt')
        not_destroyed_walls = [w for w in level.Wall if not w.is_destroyed]
        for w in not_destroyed_walls:
            self.assertFalse(level.check_on_destroyed(w))
        destroyed_walls = [w for w in level.Wall if w.is_destroyed]
        for w in destroyed_walls:
            self.assertTrue(level.check_on_destroyed(w))
        for m in level.Monster:
            self.assertTrue(level.check_on_destroyed(m))
        for bm in level.BomberMan:
            self.assertTrue(level.check_on_destroyed(bm))

    def test_moving(self):
        level = Level('level1.txt')
        for b in level.BomberMan:
            bm = b
        level.moving('r', bm)
        self.assertEqual(Point(2, 1), bm.position)
        level.moving('u', bm)
        self.assertEqual(Point(2, 1), bm.position)
        level.moving('l', bm)
        self.assertEqual(Point(1, 1), bm.position)
        level.moving('d', bm)
        self.assertEqual(Point(1, 2), bm.position)

    def test_is_inside_field(self):
        level = Level('level3.txt')
        for b in level.BomberMan:
            bm = b
        self.assertFalse(level.is_inside_field('r', bm))
        self.assertFalse(level.is_inside_field('d', bm))
        self.assertTrue(level.is_inside_field('u', bm))
        self.assertTrue(level.is_inside_field('l', bm))

    def test_get_future_step(self):
        level = Level('level3.txt')
        for b in level.BomberMan:
            bm = b
        self.assertEqual(Point(10, 6), level.get_future_step('r', bm))
        self.assertEqual(Point(8, 6), level.get_future_step('l', bm))
        self.assertEqual(Point(9, 5), level.get_future_step('u', bm))
        self.assertEqual(Point(9, 7), level.get_future_step('d', bm))

    def test_get_count_of_steps(self):
        level = Level("level2.txt")
        for b in level.BomberMan:
            bm = b
        self.assertEqual(2, level.get_count_of_steps('l', bm))
        self.assertEqual(2, level.get_count_of_steps('u', bm))
        self.assertEqual(1, level.get_count_of_steps('r', bm))
        self.assertEqual(1, level.get_count_of_steps('d', bm))

    def test_do_step(self):
        level = Level("level2.txt")
        for b in level.BomberMan:
            bm = b
        level.do_step('l', bm, 2)
        self.assertEqual(Point(6, 5), bm.position)
        level.do_step('u', bm, 1)
        self.assertEqual(Point(6, 4), bm.position)
        level.do_step('r', bm, 1)
        self.assertEqual(Point(7, 4), bm.position)
        level.do_step('d', bm, 2)
        self.assertEqual(Point(7, 6), bm.position)

    def test_bm_intersect_with_monster(self):
        level = Level("level1.txt")
        for b in level.BomberMan:
            bm = b
        for i in range(4):
            level.moving('r', bm)
        level.bm_intersect_with_monster()
        self.assertEqual(2, bm.count_of_lives)
        level.bm_intersect_with_monster()
        self.assertEqual(1, bm.count_of_lives)
        level.bm_intersect_with_monster()
        self.assertEqual(0, bm.count_of_lives)
        self.assertTrue(level.is_over)

    def test_check_and_take_prizes(self):
        level = Level("level4.txt")
        for b in level.BomberMan:
            bm = b
        level.moving('u', bm)
        level.check_and_take_prizes(bm)
        self.assertEqual(4, bm.count_of_lives)
        level.moving('l', bm)
        level.check_and_take_prizes(bm)
        self.assertEqual(1, len(bm.backpack))
        self.assertEqual(3, bm.backpack[0].power)
        level.moving('d', bm)
        level.check_and_take_prizes(bm)
        self.assertEqual(2, len(bm.backpack))
        self.assertEqual(2, bm.backpack[1].power)

    def test_is_win(self):
        level = Level("level4.txt")
        for b in level.BomberMan:
            bm = b
        level.moving('l', bm)
        level.moving('u', bm)
        level.put_bomb_and_get_bomb_power()
        level.moving('r', bm)
        level.moving('d', bm)
        level.explode_bomb()
        self.assertTrue(level.is_win())


if __name__ == '__main__':
    main()
