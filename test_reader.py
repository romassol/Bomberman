import json
from unittest import TestCase, main

from readfieldfromfile import Reader
from point import Point
from bomberman import BomberMan
from wall import Wall
from monster import Monster
from prizelife import PrizeLife
from prizebomb import PrizeBomb


class TestReader(TestCase):

    def test_process_file_and_get_new_file_name(self):
        reader = Reader("level1.txt")
        self.assertEqual(
            "tmp_level1.txt",
            reader.process_file_and_get_new_file_name("level1.txt"))
        with open("tmp_level1.txt", 'r') as data_file:
            data = json.load(data_file)
        field = [["#", "#", "#", "#", "#", "#", "*"],
                 ["#", "B", ".", ".", ".", "M", "*"],
                 ["#", ".", "*", ".", "U", "*", "#"],
                 ["#", "D", ".", "#", ".", ".", "#"],
                 ["#", ".", "r", ".", "d", "*", "#"],
                 ["#", ".", "M", ".", ".", ".", "#"],
                 ["#", "#", "#", "#", "#", "#", "#"]]
        self.assertEqual(field, data["field"])
        prizes = [[".", ".", ".", ".", ".", ".", "."],
                  [".", ".", ".", ".", ".", ".", "."],
                  [".", ".", "2", ".", ".", ".", "."],
                  [".", ".", ".", ".", ".", ".", "."],
                  [".", ".", "1", ".", "3", "2", "."],
                  [".", ".", ".", ".", ".", ".", "."],
                  [".", ".", ".", ".", ".", ".", "."]]
        self.assertEqual(prizes, data["prizes"])

    def test_check_on_starting_of_array(self):
        reader = Reader("level1.txt")
        lines = ['field 1 2 3', 'prizes 1 2 3', 'fkdsjfsl']
        print(reader.file)
        self.assertTrue(reader.check_on_starting_of_array('field', lines[0]))
        self.assertTrue(reader.is_reading_field)
        self.assertTrue(reader.check_on_starting_of_array('prizes', lines[1]))
        self.assertTrue(reader.is_reading_prizes)
        self.assertFalse(reader.check_on_starting_of_array('prizes', lines[2]))
        self.assertEqual('field 1 2 3prizes 1 2 3', reader.file)

    def test_check_on_ending_of_array(self):
        reader = Reader("level1.txt")
        reader.is_reading_field = True
        reader.check_on_ending_of_array('}', ['1 2 3'], ['4 5 6'])
        self.assertFalse(reader.is_reading_field)
        self.assertEqual('["1 2 3"]', reader.file)
        reader.is_reading_prizes = True
        reader.check_on_ending_of_array('}', ['1 2 3'], ['4 5 6'])
        self.assertFalse(reader.is_reading_prizes)
        self.assertEqual('["1 2 3"]["4 5 6"]', reader.file)

    def test_get_part_of_field(self):
        reader = Reader("level1.txt")
        self.assertEqual(['field', '123', '56578'],
                         reader.get_part_of_field('  field 123 56578'))

    def test_check_added_parameters(self):
        reader = Reader("level1.txt")
        with open("tmp_level1.txt", 'r') as data_file:
            data = json.load(data_file)
        with self.assertRaises(KeyError):
            reader.check_added_parameters('fi', data)
        field = [["#", "#", "#", "#", "#", "#", "*"],
                 ["#", "B", ".", ".", ".", "M", "*"],
                 ["#", ".", "*", ".", "U", "*", "#"],
                 ["#", "D", ".", "#", ".", ".", "#"],
                 ["#", ".", "r", ".", "d", "*", "#"],
                 ["#", ".", "M", ".", ".", ".", "#"],
                 ["#", "#", "#", "#", "#", "#", "#"]]
        self.assertEqual(field, reader.check_added_parameters('field', data))

    def test_create_and_populate_set_objects(self):
        reader = Reader("level5.txt")
        with open("tmp_level5.txt", 'r') as data_file:
            data = json.load(data_file)
        reader.objects = {}
        reader.create_and_populate_set_objects(data['field'])
        self.assertEqual(1, len(list(reader.objects['BomberMan'])))
        self.assertEqual(BomberMan,
                         type(list(reader.objects['BomberMan'])[0]))
        self.assertEqual(Point(2, 1),
                         list(reader.objects['BomberMan'])[0].position)
        self.assertEqual(1, len(list(reader.objects['Monster'])))
        self.assertEqual(Monster, type(list(reader.objects['Monster'])[0]))
        self.assertEqual(Point(3, 2),
                         list(reader.objects['Monster'])[0].position)
        self.assertEqual(2, len(reader.objects['Wall']))
        for w in reader.objects['Wall']:
            self.assertEqual(Wall, type(w))
        self.assertEqual(2, len(list(reader.objects['Wall'])))

    def test_create_and_populate_set_prizes(self):
        reader = Reader("level5.txt")
        with open("tmp_level5.txt", 'r') as data_file:
            data = json.load(data_file)
        reader.objects = {}
        reader.create_and_populate_set_prizes(data['prizes'])
        self.assertEqual(2, len(reader.objects['Prizes']))
        self.assertEqual(
            1, list(reader.objects['Prizes'])[1].count_of_added_lives)
        self.assertEqual(Point(0, 0),
                         list(reader.objects['Prizes'])[1].position)
        self.assertEqual(2, list(reader.objects['Prizes'])[0].power)
        self.assertEqual(Point(1, 2),
                         list(reader.objects['Prizes'])[0].position)


if __name__ == '__main__':
    main()
