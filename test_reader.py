from unittest import TestCase, main

from read_field_from_file import Reader
from point import Point
from bomberman import BomberMan
from wall import Wall
from monster import Monster


class TestPoint(TestCase):

    def test_read_file_simple(self):
        r = Reader('input_test.txt')
        self.assertEqual(r.height, 5)
        self.assertEqual(r.width, 5)

        self.assertEqual(len(r.objects), 3)
        self.assertEqual(len(r.objects['BomberMan']), 1)
        self.assertEqual(len(r.objects['Wall']), 7)
        self.assertEqual(len(r.objects['Monster']), 3)

        for b in r.objects['BomberMan']:
            self.assertEqual(b.position, Point(0, 0))

        monster_position = {Point(4, 0), Point(1, 2), Point(0, 4)}
        self.assertEqual(len(monster_position), len(r.objects['Monster']))
        position = {f.position for f in r.objects['Monster']}
        self.assertTrue(monster_position == position)

        wall_position = {
            Point(3, 0),
            Point(0, 1),
            Point(1, 1),
            Point(3, 1),
            Point(1, 3),
            Point(4, 3),
            Point(2, 4)
        }
        self.assertEqual(len(wall_position), len(r.objects['Wall']))
        position = {f.position for f in r.objects['Wall']}
        self.assertTrue(wall_position == position)

    def test_read_file_empty(self):
        r = Reader('empty.txt')
        self.assertEqual(r.height, 0)
        self.assertEqual(r.width, 0)
        self.assertEqual(len(r.objects), 0)


if __name__ == '__main__':
    main()
