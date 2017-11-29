from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QBasicTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QFont
import random

from characterimage import CharacterImage
from iconimage import IconImage
from bomberman import BomberMan
from point import Point
from prizelife import PrizeLife
from prizebomb import PrizeBomb


class CentralWidget(QWidget):
    def __init__(self, parent, game, height, width, score_window, scoreboard):
        super().__init__(parent)

        self.scoreboard = scoreboard
        self.score_window = score_window

        self.parent = parent
        self.height = height
        self.width = width

        self.images_folder = 'images/'
        self.name_of_image_monster = None
        self.name_of_image_BM = None
        self.names_of_images_walls = None
        self.names_of_images_prizes = None
        self.names_of_images_bombs = None
        self.set_names_of_images()

        self.game = game
        self.level = game.get_current_level()

        self.size_square = self.calculate_size_square()
        self.size_window = self.calculate_size_window()

        self.background = QLabel(self)
        self.putted_bombs = []
        self.bombs = []
        self.bomberman_image = None
        self.queue_moving_BM = None
        self.prizes = []
        self.walls = []
        self.monsters = []
        self.lives = []

        self.set_graphical_parameters()
        self.scoring = QLabel(self)
        self.set_scoring()

        self.timers_bomb = []
        for i in range(len(self.level.Bombs)):
            self.timers_bomb.append(0)
        self.timer_immortality = 0
        self.timer_BM = 0
        self.timer_monster = 0
        self.timer = 0
        self.timer = QBasicTimer()
        self.timer_starting()

        self.time_to_bomb = 30
        self.time_to_monster = max(
            round(10 / self.game.get_current_level().monster_speed), 1)
        self.time_to_remove_immortality = 17
        self.setGeometry(0, 25, self.size_window[0], self.size_window[1])

    def set_scoring(self):
        self.scoring = QLabel(str(self.game.get_scoring()), self)
        self.scoring.setGeometry(self.size_window[0] - 120, 0, 100, 50)
        self.scoring.setStyleSheet("QLabel {color : white; font: 20pt;}")
        self.scoring.setAlignment(Qt.AlignRight)

    def set_graphical_parameters(self):
        self.set_background(self.images_folder + "grass.png")
        self.putted_bombs = []
        for i in range(len(self.level.Bombs)):
            self.putted_bombs.append(CharacterImage(self, self.level.Bombs[i],
                                   self.size_square,
                                   self.images_folder + "bomb.png"))
            self.putted_bombs[i].hide()
        self.bombs = []
        for b in self.level.BomberMan:
            self.bomberman_image = CharacterImage(self, b,
                                                  self.size_square,
                                                  self.name_of_image_BM)
        self.queue_moving_BM = []
        self.prizes = []
        self.create_and_append_prizes()
        self.walls = []
        self.create_and_append_walls()
        self.monsters = []
        self.create_and_append_character(self.level.Monster,
                                         self.name_of_image_monster,
                                         self.monsters)
        self.lives = []
        self.draw_lives()

    def set_names_of_images(self):
        self.name_of_image_monster = self.images_folder + "monster.png"
        self.name_of_image_BM = self.images_folder + "person.png"
        self.names_of_images_walls = {
            'False None': self.images_folder + 'metal_wall.png',
            'True None': self.images_folder + 'wall.png',
            'False u': self.images_folder + 'up_metal_wall.png',
            'False d': self.images_folder + 'down_metal_wall.png',
            'False l': self.images_folder + 'left_metal_wall.png',
            'False r': self.images_folder + 'right_metal_wall.png',
            'True u': self.images_folder + 'up_wall.png',
            'True d': self.images_folder + 'down_wall.png',
            'True l': self.images_folder + 'left_wall.png',
            'True r': self.images_folder + 'right_wall.png'}
        self.names_of_images_prizes = {'1': self.images_folder + 'heart.png',
                                       '2': self.images_folder + 'bomb_2.png',
                                       '3': self.images_folder + 'bomb_3.png'}
        self.names_of_images_bombs = {1: self.images_folder + "bomb.png",
                                      2: self.images_folder + 'bomb_2.png',
                                      3: self.images_folder + 'bomb_3.png'}

    def calculate_size_square(self):
        return int(min(self.height/self.level.height,
                       self.width/self.level.width))

    def calculate_size_window(self):
        return self.level.width * self.size_square,\
               self.level.height * self.size_square

    def create_and_append_walls(self):
        for w in self.level.Wall:
            self.walls.append(
                CharacterImage(self, w, self.size_square,
                               self.names_of_images_walls[str(w)]))

    def create_and_append_prizes(self):
        for p in self.level.Prizes:
            self.prizes.append(
                CharacterImage(self, p, self.size_square,
                               self.names_of_images_prizes[
                                   str(p).split(',')[1].split()[1]]))

    def create_and_append_character(self, input_characters_list,
                                    image, finaly_characters_list):
        for character in input_characters_list:
            finaly_characters_list.append(
                CharacterImage(self, character, self.size_square, image))

    def draw_lives(self):
        self.lives.clear()
        for i in range(self.bomberman_image.character.count_of_lives):
            position = Point(i, 0)
            icon = IconImage(self, position,
                             self.size_square / 3,
                             self.images_folder + 'heart.png')
            self.lives.append(icon)

    def set_background(self, image):
        pixmap = QPixmap(image)
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0,
                                    self.size_window[0], self.size_window[1])

    def timer_starting(self):
        self.timer.start(100, self)

    def show_game_over(self):
        go = QPushButton(self)
        icon = QIcon(self.images_folder + "Game_Over.png")
        go.setIcon(icon)
        go.setIconSize(QSize(self.size_window[0], self.size_window[1]))
        go.setStyleSheet("QPushButton {border:none;"
                         "background-color:transparent;}")
        go.setGeometry(0, 0, self.size_window[0], self.size_window[1])
        go.show()

    def show_win(self):
        win = QPushButton(self)
        icon = QIcon(self.images_folder + "Win.png")
        win.setIcon(icon)
        win.setIconSize(QSize(self.size_window[0], self.size_window[1]))
        win.setStyleSheet("QPushButton {border:none;"
                          "background-color:transparent;}")
        win.setGeometry(0, 0, self.size_window[0], self.size_window[1])
        win.show()

    def show_scoring(self):
        self.scoring.setText(str(self.game.get_scoring()))

    def hide_graphical_parameters(self, list_of_buttons):
        for button in list_of_buttons:
            button.hide()

    def hide_all_graphical_parameters(self, graphacal_parameters):
        for parameter in graphacal_parameters:
            self.hide_graphical_parameters(parameter)
        self.bomberman_image.hide()

    def try_change_level(self):
        if not self.game.try_go_to_the_next_level():
            return
        self.level = self.game.get_current_level()
        self.time_to_monster = max(
            round(10 / self.game.get_current_level().monster_speed), 1)
        self.size_square = self.calculate_size_square()
        self.size_window = self.calculate_size_window()
        self.hide_all_graphical_parameters([self.bombs, self.prizes,
                                            self.walls, self.monsters,
                                            self.lives])
        self.set_graphical_parameters()
        self.scoring.hide()
        self.scoring = None
        self.set_scoring()
        self.scoring.show()

    def timerEvent(self, e):
        direction = ['r', 'l', 'u', 'd']

        self.try_change_level()

        self.timer_monster = self.zeroize_timer(self.timer_monster)
        self.timer_BM = self.zeroize_timer(self.timer_BM)
        self.timer_immortality = self.zeroize_timer(self.timer_immortality)
        for i in range(len(self.timers_bomb)):
            self.timers_bomb[i] = self.zeroize_timer(self.timers_bomb[i])

        if not self.level.is_BM_lives_changed:
            self.level.bm_intersect_with_monster()
            self.timer_immortality = 1
            self.bomberman_image.set_picture(self.size_square,
                                             self.images_folder + "person.png")
        else:
            self.bomberman_image.set_picture(
                self.size_square,
                self.images_folder + "person_hurt.png")
        for i in range(len(self.level.Bombs)):
            if not self.level.Bombs[i].is_active:
                self.timers_bomb[i] = 1
            else:
                if self.timers_bomb[i] % self.time_to_bomb == 0:
                    self.boom(i)

        if self.timer_immortality % self.time_to_remove_immortality == 0:
            self.level.is_BM_lives_changed = False
            self.lives.pop().hide()

        if len(self.queue_moving_BM) > 0:
            self.moving(
                self.queue_moving_BM.pop(0),
                self.bomberman_image.character,
                self.bomberman_image
            )

        if self.game.is_win():
            self.show_win()
            player_name = QInputDialog.getText(self.parent, 'win',
                                               'enter your name')
            if player_name[1]:
                self.scoreboard.add_score(player_name[0],
                                          float(self.game.get_scoring()))
                self.score_window.show_current(player_name[0],
                                               float(self.game.get_scoring()))
            self.timer.stop()

        if self.game.is_over():
            self.show_game_over()
            self.bomberman_image.hide()
            self.timer.stop()

        if self.timer_monster % self.time_to_monster == 0:
            for m in self.monsters:
                r = random.randint(0, 3)
                self.moving(direction[r], m.character, m)
        self.show_scoring()

        self.timer_BM += 1
        self.timer_monster += 1
        self.timer_immortality += 1
        for t in range(len(self.timers_bomb)):
            self.timers_bomb[t] += 1

    def zeroize_timer(self, timer):
        if timer > 1000:
            return 0
        return timer

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_D or key_event.key() == 1042:
            self.queue_moving_BM.append('r')
        if key_event.key() == Qt.Key_A or key_event.key() == 1060:
            self.queue_moving_BM.append('l')
        if key_event.key() == Qt.Key_W or key_event.key() == 1062:
            self.queue_moving_BM.append('u')
        if key_event.key() == Qt.Key_S or key_event.key() == 1067:
            self.queue_moving_BM.append('d')
        if key_event.key() == Qt.Key_Z or key_event.key() == 1071:
            self.set_bomb()
        self.repaint()

    def set_bomb(self):
        index = self.level.put_bomb_and_get_bomb_index()
        if index is None:
            return
        power = self.level.bombs_power[index]
        if power > 1:
            self.bombs.pop().hide()
        self.putted_bombs[index].move(
            self.putted_bombs[index].position.x * self.size_square,
            self.putted_bombs[index].position.y * self.size_square
        )
        pixmap = QIcon(self.names_of_images_bombs[power])
        self.putted_bombs[index].setIcon(pixmap)
        self.putted_bombs[index].show()

    def update_field(self):
        self.update_character(self.walls, self.level.Wall)
        self.update_character(self.monsters, self.level.Monster)

    def update_character(self, list_of_butten, obj):
        removed = []
        for b in list_of_butten:
            if b.character not in obj:
                b.hide()
                removed.append(b)
        for b in removed:
            list_of_butten.remove(b)

    def boom(self, index_of_bomb):
        self.level.explode_bomb(index_of_bomb)
        self.putted_bombs[index_of_bomb].hide()
        self.update_field()

    def moving(self, direction, level_character, button):
        self.level.moving(direction, level_character)
        button.move(
            button.position.x * self.size_square,
            button.position.y * self.size_square
        )
        if isinstance(level_character, BomberMan):
            self.add_prizes_and_paint_icons()

    def add_prizes_and_paint_icons(self):
        removed = []
        for p in self.prizes:
            if self.bomberman_image.position == p.position:
                p.hide()
                removed.append(p)
                if isinstance(p.character, PrizeLife):
                    self.paint_icon_and_add_prize(
                        Point(len(self.lives), 0), self.lives,
                        self.size_square/3, 'images/heart.png')
                if isinstance(p.character, PrizeBomb):
                    power = self.bomberman_image.character.backpack[
                        len(self.bomberman_image.character.backpack) - 1].power

                    self.paint_icon_and_add_prize(
                        Point(len(self.bombs), 1),
                        self.bombs, self.size_square/3,
                        self.names_of_images_bombs[power])
        for b in removed:
            self.prizes.remove(b)

    def paint_icon_and_add_prize(self, icon_position, prizes, size, image):
        icon = IconImage(self, icon_position, size, image)
        prizes.append(icon)
