import sys
import json
from shutil import copyfileobj
import re

from point import Point
from bomb import Bomb
from bomberman import BomberMan
from wall import Wall
from monster import Monster
from prizebomb import PrizeBomb
from prizelife import PrizeLife


class Reader:
    def __init__(self, file_name):
        self.classes = {"B": BomberMan, "#": Wall, "*": Wall, "U": Wall, "D": Wall, "R": Wall, "L": Wall, "u": Wall,
                        "d": Wall, "r": Wall, "l": Wall, "M": Monster}
        self.walls = {"#": [False, None], "*": [True, None], "U": [False, 'u'], "D": [False, 'd'], "R": [False, 'r'],
                      "L": [False, 'l'], "u": [True, 'u'], "d": [True, 'd'], "r": [True, 'r'], "l": [True, 'l']}
        self.prize = {"2": PrizeBomb, "3": PrizeBomb, "1": PrizeLife}
        self.objects = {}
        self.height = 0
        self.width = 0
        self.monster_speed = 0
        self.door_position = Point(0, 0)
        self.is_reading_field = False
        self.is_reading_prizes = False
        self.file = ''
        new_file_name = self.process_file_and_get_new_file_name(file_name)
        self.read_file(new_file_name)

    def process_file_and_get_new_file_name(self, file_name):
        new_name = 'tmp_' + file_name
        end_key = False
        field = []
        prizes = []
        with open(file_name, 'r') as data_file:
            data = data_file.readlines()
        for line in data:
            self.check_on_ending_of_array(line, field, prizes)
            if line.find('"') != -1:
                if end_key:
                    self.file += ',' + '\n'
                    end_key = False
                end_key = True
            is_reading_field = self.check_on_starting_of_array('field', line)
            if is_reading_field:
                continue
            is_reading_prizes = self.check_on_starting_of_array('prizes', line)
            if is_reading_prizes:
                continue
            part_of_array = self.get_part_of_field(line)
            if not self.is_reading_field and not self.is_reading_prizes:
                self.file += line.rstrip()
            else:
                if self.is_reading_field:
                    field.append(part_of_array)
                if self.is_reading_prizes:
                    prizes.append(part_of_array)
        with open(new_name, 'w') as tmp_file:
            tmp_file.writelines(self.file)
        self.file = ''
        return new_name

    def check_on_starting_of_array(self, word, line):
        if line.find(word) != -1:
            if word == 'field':
                self.is_reading_field = True
            elif word == 'prizes':
                self.is_reading_prizes = True
            self.file += line
            return True
        return False

    def check_on_ending_of_array(self, line, field, prizes):
        if self.is_reading_field:
            if (line.find('"') != -1 or line.find('}') != -1) and self.is_reading_field:
                self.is_reading_field = False
                self.file += str(field).replace('\'', '"', len(str(field)))
        elif self.is_reading_prizes:
            if (line.find('"') != -1 or line.find('}') != -1) and self.is_reading_prizes:
                self.is_reading_prizes = False
                self.file += str(prizes).replace('\'', '"', len(str(prizes)))

    def get_part_of_field(self, line):
        result = re.split(r' ', line)
        result = [f.rstrip() for f in result if f != '']
        return result

    def check_added_parameters(self, parameter, data):
        try:
            return data[parameter]
        except KeyError:
            sys.exit("you need to specify a " + parameter)

    def create_and_populate_set_objects(self, input_map):
        for i in range(len(input_map)):
            for j in range(len(input_map[i])):
                self.width = max(len(input_map[i]), self.width)
                code = input_map[i][j]
                if code != ".":
                    if self.classes[code].__name__ not in self.objects.keys():
                        self.objects[self.classes[code].__name__] = set()
                    if self.classes[code].__name__ == 'Wall':
                        self.objects[self.classes[code].__name__].add(
                        self.classes[code](Point(j, i), *self.walls[code])
                        )
                    else:
                        self.objects[self.classes[code].__name__].add(
                        self.classes[code](Point(j, i))
                        )

    def create_and_populate_set_prizes(self, input_prizes):
        for i in range(len(input_prizes)):
            for j in range(len(input_prizes[i])):
                code = input_prizes[i][j]
                if code != ".":
                    if 'Prizes' not in self.objects.keys():
                        self.objects['Prizes'] = set()
                    self.objects['Prizes'].add(self.prize[code](int(code), Point(j,i)))

    def read_file(self, file_name):
        with open(file_name, 'r') as data_file:
            data = json.load(data_file)

        input_prizes = self.check_added_parameters('prizes', data)
        input_map = self.check_added_parameters('field', data)
        self.monster_speed = self.check_added_parameters('monster speed', data)
        self.height = len(input_map)

        self.create_and_populate_set_objects(input_map)
        self.create_and_populate_set_prizes(input_prizes)


if __name__ == '__main__':
    r = Reader('level1.txt')
