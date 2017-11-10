import sys
import copy

from level import Level
from game import Game


def get_command():
    return input()


def do_step_and_print_information(game, BM, direction):
    game.get_current_level().moving(direction, BM)
    print("BM position is " + str(BM.position))


def put_bomb_and_print_information(game):
    game.get_current_level().put_bomb_and_get_bomb_power()
    print("Bomb was put in " + str(game.get_current_level().Bomb.position))


def explode_bomb_and_print_information(game, previous_monsters_positions, previous_walls_positions):
    game.get_current_level().explode_bomb()
    monsters_positions = [monster.position for monster in game.get_current_level().Monster]
    walls_positions = [wall.position for wall in game.get_current_level().Wall if wall.is_destroyed]
    for m in previous_monsters_positions:
        if m not in monsters_positions:
            print("Monster in " + str(m) + " position was killed")
    for w in previous_walls_positions:
        if w not in walls_positions:
            print("Wall in " + str(w) + " position was destroyed")


def print_if_current_level_is_win(game):
    if game.try_go_to_the_next_level():
        print("Current level is win. Go to the next level")


def print_if_is_over_and_exit(game):
    if game.is_over():
        print("Game is over")
        sys.exit()


def print_BM_lives_changed(game):
    game.get_current_level().bm_intersect_with_monster()
    if game.get_current_level().is_BM_lives_changed:
        print("BM lost one life. Now BM has " + str(BM.count_of_lives) + " lives")
        game.get_current_level().is_BM_lives_changed = False


if __name__ == '__main__':
    command = get_command().split()
    actions = {'exit': sys.exit, 'step': do_step_and_print_information, 'put': put_bomb_and_print_information,
               'explode': explode_bomb_and_print_information}
    game = Game(['level1.txt', 'level2.txt'], 5, "game1")
    monsters = copy.deepcopy(game.get_current_level().Monster)
    walls = copy.deepcopy(game.get_current_level().Wall)

    while True:
        for b in game.get_current_level().BomberMan:
            BM = b
        action = actions[command[0]]
        if command[0] == 'exit':
            action()
        if command[0] == 'step':
            action(game, BM, command[1])
        if command[0] == 'put':
            action(game)
        if command[0] == 'explode':
            monsters_positions = [monster.position for monster in monsters]
            walls_positions = [wall.position for wall in walls if wall.is_destroyed]
            action(game, monsters_positions, walls_positions)
            monsters = copy.deepcopy(game.get_current_level().Monster)
            walls = copy.deepcopy(game.get_current_level().Wall)
        print_if_current_level_is_win(game)
        print_BM_lives_changed(game)
        print_if_is_over_and_exit(game)
        command = get_command().split()
