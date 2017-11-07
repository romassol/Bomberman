import json
import copy
import os

from bomberman import BomberMan
from wall import Wall
from monster import Monster
from readfieldfromfile import Reader
from point import Point
from bomb import Bomb
from door import Door


class Level:
    def __init__(self, file_name):
        r = Reader(file_name)
        self.__dict__ = r.objects

        for b in self.BomberMan:
            self.Bomb = Bomb(b)

        self.set_speed_all_monsters(r)

        self.height = r.height
        self.width = r.width

        self.is_over = False
        # self.is_win = False
        self.points = 0
        self.scoring = {'Monster': 100, 'Wall': 5}

        self.is_BM_lives_changed = False
        # self.is_BM_lives_increased = False

        self.explode_area = self.Bomb.power
        self.direc = {'r': 1, 'l': -1, 'u': -1, 'd': 1}

    def set_speed_all_monsters(self, r):
        for m in self.Monster:
            m.set_speed(r.monster_speed)

    def put_bomb(self):
        for b in self.BomberMan:
            if not b.backpack:
                self.Bomb = Bomb(b)
                self.points -= 10
            else:
                self.Bomb = b.backpack.pop()
            self.Bomb.position = copy.deepcopy(b.position)
        self.Bomb.is_active = True
        self.explode_area = self.Bomb.power
        return self.explode_area

    def get_explode_area(self):
        not_destroyed_walls = {f.position for f in self.Wall if not f.is_destroyed}
        points = set()
        range_lists = [range(-1, -self.explode_area - 1, -1), range(self.explode_area + 1)]
        for p in range_lists:
            self.add_available_point_on_Y(not_destroyed_walls, points, p)
            self.add_available_point_on_X(not_destroyed_walls, points, p)
        return points

    def add_available_point_on_Y(self, not_destroyed_walls, points, range_list):
        for i in range_list:
            if 0 <= self.Bomb.position.y + i <= self.height - 1:
                point = Point(self.Bomb.position.x, self.Bomb.position.y + i)
                if point in not_destroyed_walls:
                    break
                points.add(point)

    def add_available_point_on_X(self, not_destroyed_walls, points, range_list):
        for i in range_list:
            if 0 <= self.Bomb.position.x + i <= self.width - 1:
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
                if self.check_on_destroyed(character) and character.position == coordinate:
                    removed.append(character)
            self.scoring_or_gameover(removed, one_of_set)

    def scoring_or_gameover(self, removed_characters, original_set):
        for removed_character in removed_characters:
            original_set.remove(removed_character)
            if isinstance(removed_character, BomberMan):
                self.is_over = True
                return
            self.points += self.scoring[removed_character.__class__.__name__]

    def check_on_destroyed(self, character):
        if isinstance(character, Wall):
            return character.is_destroyed
        return True

    def moving(self, direction, character):
        if self.is_inside_field(direction, character):
            count_of_steps = self.get_count_of_steps(direction, character)
            self.do_step(direction, character, count_of_steps)
            self.check_and_take_prizes(character)

    def is_inside_field(self, direction, character):
        future_coordinate = self.future_step(direction, character)
        is_inside_field = (
            0 <= future_coordinate.x <= self.width - 1 and
            0 <= future_coordinate.y <= self.height - 1
        )
        return is_inside_field

    def future_step(self, direction, character):
        new_coordinate = copy.deepcopy(character.position)
        if direction == 'r' or direction == 'l':
            new_coordinate.x += self.direc[direction]
        else:
            new_coordinate.y += self.direc[direction]
        return new_coordinate

    def get_count_of_steps(self, direction, character):
        future_coordinate = self.future_step(direction, character)
        passable_wall = []
        all_impassable_wall = []
        for w in self.Wall:
            if w.passability is not None or w.passability != direction:
                all_impassable_wall.append(w.position)
            if w.passability == direction:
                passable_wall.append(w.position)
        if future_coordinate in passable_wall:
            return 2
        if future_coordinate not in all_impassable_wall:
            return 1
        return 0

    def do_step(self, direction, character, count_of_steps):
        if direction == 'r' or direction == 'l':
            character.position.x += count_of_steps * self.direc[direction]
        else:
            character.position.y += count_of_steps * self.direc[direction]

    def is_monster_kill_BM(self):
        all_coordinates = {f.position for f in self.Monster}
        for b in self.BomberMan:
            if b.position in all_coordinates:
                b.count_of_lives -= 1
                self.is_BM_lives_changed = True
                if b.count_of_lives < 1:
                    self.is_over = True

    def check_and_take_prizes(self, character):
        if isinstance(character, BomberMan):
            removed = []
            for p in self.Prizes:
                if p.intersection_with_bm(character):
                    removed.append(p)
            for b in removed:
                self.points += 5
                self.Prizes.remove(b)

    def is_win(self):
        if self.is_over:
            return False
        for w in self.Wall:
            if w.is_destroyed:
                return False
        return True


if __name__ == '__main__':
    g = Level("level1.txt")
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
