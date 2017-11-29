from unittest import TestCase, main
from point import Point


class TestPoint(TestCase):

    def test_init_with_arguments(self):
        p = Point(2, -8236)
        self.assertEqual(p.x, 2)
        self.assertEqual(p.y, -8236)

    def test_init_without_arguments(self):
        p = Point()
        self.assertEqual(p.x, 0)
        self.assertEqual(p.y, 0)

    def test_equal(self):
        p1 = Point(0, 0)
        p2 = Point(4, 3)
        p3 = Point(0, 0)
        self.assertFalse(p1 == p2)
        self.assertTrue(p1 == p1)
        self.assertTrue(p1 == p3)

    def test_str(self):
        p1 = Point(42, -77)
        self.assertEqual(str(p1), '42 -77')


if __name__ == '__main__':
    main()
