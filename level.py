import json
import copy
import os

from bomberman import BomberMan
from wall import Wall
from monster import Monster
from readfieldfromfile import Reader
from point import Point
from bomb import Bomb


class Level:
    def __init__(self, file_name, count_of_active_bomb=2):
        r = Reader(file_name)
        self.__dict__ = r.objects
        self.Bombs = []
        for b in self.BomberMan:
            for i in range(count_of_active_bomb):
                self.Bombs.append(Bomb(b))

        self.monster_speed = r.monster_speed

        self.height = r.height
        self.width = r.width

        self.is_over = False
        self.points = 0
        self.scoring = {'Monster': 100, 'Wall': 5}

        self.is_BM_lives_changed = False

        self.bombs_power = []
        for bomb in self.Bombs:
            self.bombs_power.append(bomb.power)
        self.direc = {'r': 1, 'l': -1, 'u': -1, 'd': 1}

    def put_bomb_and_get_bomb_index(self):
        index_of_not_active_bomb = self.get_index_of_not_active_bomb()
        if index_of_not_active_bomb is None:
            return None
        for b in self.BomberMan:
            if not b.backpack:
                self.Bombs[index_of_not_active_bomb] = Bomb(b)
                self.points -= 10
            else:
                self.Bombs[index_of_not_active_bomb] = b.backpack.pop()
            self.Bombs[index_of_not_active_bomb].position = copy.deepcopy(b.position)
        self.Bombs[index_of_not_active_bomb].is_active = True
        self.bombs_power[index_of_not_active_bomb] = self.Bombs[index_of_not_active_bomb].power
        return index_of_not_active_bomb

    def get_index_of_not_active_bomb(self):
        for i in range(len(self.Bombs)):
            if not self.Bombs[i].is_active:
                return i
        return None

    def get_explode_area(self, index_of_bomb):
        not_destroyed_walls = [f.position
                               for f in self.Wall if not f.is_destroyed]
        points = set()
        range_list = [range(-1, -self.bombs_power[index_of_bomb] - 1, -1),
                      range(self.bombs_power[index_of_bomb] + 1)]
        for p in range_list:
            self.add_available_point_on_Y(not_destroyed_walls, points, p, index_of_bomb)
            self.add_available_point_on_X(not_destroyed_walls, points, p, index_of_bomb)
        return points

    def add_available_point_on_Y(self, not_destroyed_walls,
                                 points, range_list, index_of_bomb):
        for i in range_list:
            if 0 <= self.Bombs[index_of_bomb].position.y + i <= self.height - 1:
                point = Point(self.Bombs[index_of_bomb].position.x, self.Bombs[index_of_bomb].position.y + i)
                if point in not_destroyed_walls:
                    continue
                points.add(point)

    def add_available_point_on_X(self, not_destroyed_walls,
                                 points, range_list, index_of_bomb):
        for i in range_list:
            if 0 <= self.Bombs[index_of_bomb].position.x + i <= self.width - 1:
                point = Point(self.Bombs[index_of_bomb].position.x + i, self.Bombs[index_of_bomb].position.y)
                if point in not_destroyed_walls:
                    continue
                points.add(point)

    def explode_bomb(self, index_of_bomb):
        list_of_characters = [self.BomberMan, self.Monster, self.Wall]
        if self.Bombs[index_of_bomb].is_active:
            explode_area = self.get_explode_area(index_of_bomb)
            for point in explode_area:
                self.delete_character_in_all_sets_and_scoring(
                    list_of_characters, point)
            self.Bombs[index_of_bomb].is_active = False

    def delete_character_in_all_sets_and_scoring(self, list_of_characters,
                                                 coordinate):
        for one_of_set in list_of_characters:
            removed = []
            for character in one_of_set:
                if self.check_on_destroyed(character) and\
                                character.position == coordinate:
                    removed.append(character)
            self.remove_characters_and_scoring_or_gameover(removed, one_of_set)

    def remove_characters_and_scoring_or_gameover(self, removed_characters,
                                                  original_set):
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
        future_coordinate = self.get_future_step(direction, character)
        is_inside_field = (
            0 <= future_coordinate.x <= self.width - 1 and
            0 <= future_coordinate.y <= self.height - 1
        )
        return is_inside_field

    def get_future_step(self, direction, character):
        new_coordinate = copy.deepcopy(character.position)
        if direction == 'r' or direction == 'l':
            new_coordinate.x += self.direc[direction]
        else:
            new_coordinate.y += self.direc[direction]
        return new_coordinate

    def get_count_of_steps(self, direction, character):
        future_coordinate = self.get_future_step(direction, character)
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

    def bm_intersect_with_monster(self):
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
