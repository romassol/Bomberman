import json
import copy
import os

from bomberman import BomberMan
from wall import Wall
from monster import Monster
from read_field_from_file import Reader
from point import Point
from bomb import Bomb


class Level:
    def __init__(self, file_name):
        r = Reader(file_name)
        self.__dict__ = r.objects
        for b in self.BomberMan:
            self.Bomb = Bomb(b)

        self.monster_speed = r.monster_speed
        self.height = r.height
        self.width = r.width
        self.is_gameover = False
        self.is_BM_lifes_changed = False
        self.is_BM_lifes_increased = False
        self.explode_area = self.Bomb.power
        self.direc = {'r': 1, 'l': -1, 'u': -1, 'd': 1}

    def put_bomb(self):
        for b in self.BomberMan:
            if not b.backpack:
                self.Bomb = Bomb(b)
            else:
                self.Bomb = b.backpack.pop()
            self.Bomb.position = copy.deepcopy(b.position)
        self.Bomb.is_active = True
        self.explode_area = self.Bomb.power
        return self.explode_area

    def get_explode_area(self):
        not_destroyed_walls = {f.position for f in self.Wall if not f.is_destroyed}
        points = set()
        range_lists = [range(-1, -self.explode_area-1, -1), range(self.explode_area + 1)]
        for p in range_lists:
            self.add_available_point_on_Y(not_destroyed_walls, points, p)
            self.add_available_point_on_X(not_destroyed_walls, points, p)
        return points

    def add_available_point_on_Y(self, not_destroyed_walls, points, range_list):
        for i in range_list:
            if (self.Bomb.position.y + i >= 0 and
                    self.Bomb.position.y + i <= self.height - 1):
                point = Point(self.Bomb.position.x, self.Bomb.position.y + i)
                if point in not_destroyed_walls:
                    break
                points.add(point)

    def add_available_point_on_X(self, not_destroyed_walls, points, range_list):
        for i in range_list:
            if (self.Bomb.position.x + i >= 0 and
                    self.Bomb.position.x + i <= self.width - 1):
                point = Point(self.Bomb.position.x + i, self.Bomb.position.y)
                if point in not_destroyed_walls:
                    break
                points.add(point)

    def explode_bomb(self):
        list_of_characters = [self.BomberMan, self.Monster, self.Wall]
        if self.Bomb.is_active:
            explode_area = self.get_explode_area()
            for point in explode_area:
                self.delete_character_in_all_sets(list_of_characters, point)
            self.Bomb.is_active = False

    def delete_character_in_all_sets(self, list_of_characters, coordinate):
        for one_of_set in list_of_characters:
            removed = []
            for character in one_of_set:
                if (self.check_on_destroyed(character) and
                    character.position == coordinate):
                    removed.append(character)
            for b in removed:
                one_of_set.remove(b)

    def check_on_destroyed(self, character):
        if isinstance(character, Wall):
            return character.is_destroyed
        return True

    def moving(self, direction, character):
        if self.is_inside_field(direction, character):
            count_of_steps = self.get_count_of_steps_which_available_throw_wall(direction, character)
            for i in range(count_of_steps):
                self.do_step(direction, character)
                self.check_and_take_prizes(character)

    def is_inside_field(self, direction, character):
        future_coordinate = self.future_step(direction, character)
        is_inside_field = (
            future_coordinate.x >= 0 and
            future_coordinate.x <= self.width - 1 and
            future_coordinate.y >= 0 and
            future_coordinate.y <= self.height - 1
        )
        return is_inside_field

    def future_step(self, direction, character):
        new_coordinate = copy.deepcopy(character.position)
        if direction == 'r' or direction == 'l':
            new_coordinate.x += self.direc[direction]
        else:
            new_coordinate.y += self.direc[direction]
        return new_coordinate

    def get_count_of_steps_which_available_throw_wall(self, direction, character):
        future_coordinate = self.future_step(direction, character)
        passable_wall = []
        all_impassable_wall = []
        for w in self.Wall:
            if w.passability != None or w.passability != direction:
                all_impassable_wall.append(w.position)
            if w.passability == direction:
                passable_wall.append(w.position)
        if future_coordinate in passable_wall:
            return 2
        if future_coordinate not in all_impassable_wall:
            return 1
        return 0

    def do_step(self, direction, character):
        if direction == 'r' or direction == 'l':
            character.position.x += self.direc[direction]
        else:
            character.position.y += self.direc[direction]

    def is_monster_kill_BM(self):
        all_coordinates = {f.position for f in self.Monster}
        for b in self.BomberMan:
            if b.position in all_coordinates:
                b.count_of_lives -= 1
                self.is_BM_lifes_changed = True
                if b.count_of_lives < 1:
                    self.is_gameover = True

    def check_and_take_prizes(self, character):
        if isinstance(character, BomberMan):
            removed = []
            for p in self.Prizes:
                if p.activate(character):
                    removed.append(p)
            for b in removed:
                self.Prizes.remove(b)

    # def set_immutable()


if __name__ == '__main__':
    g = Level("input_test.txt")
    # print()
    # k = copy.deepcopy(g.Wall)
    # for p in g.Wall:
    #     print(p.position, p.is_destroyed)
    # print()
    print(g.Prizes)
    for b in g.BomberMan:
        bm = b
    g.moving('d', bm)
    print(len(g.Wall))
    g.put_bomb()
    g.moving('u', bm)
    g.moving('r', bm)
    g.explode_bomb()
    print(len(g.Wall))
    g.moving('d', bm)
    for l in b.backpack:
        print(l, l.power)
    g.moving('d', bm)
    g.put_bomb()
    g.moving('u', bm)
    g.moving('l', bm)
    g.explode_bomb()
    print(len(g.Wall))
    print(b.backpack)
    g.moving('r', bm)
    g.moving('d', bm)
    g.moving('d', bm)
    print(bm.count_of_lives)
    print(b.backpack)
    print(g.Prizes)
    print()
