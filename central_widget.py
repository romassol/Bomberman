from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QBasicTimer, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QFont
import random

from character_image import Character_image
from icon_image import Icon_image
from bomberman import BomberMan
from point import Point
from prize_life import Prize_life
from prize_bomb import Prize_bomb


class Central_widget(QWidget):
    def __init__(self, parent, level, height, width):
        super().__init__(parent)
        self.height = height
        self.width = width
        self.level = level

        self.name_of_image_monster = "images/monster.png"
        self.name_of_image_BM = "images/person.png"
        self.names_of_images_walls = {'False None': 'images/metal_wall.png',
                                        'True None': 'images/wall.png',
                                        'False u': 'images/up_metal_wall.png',
                                        'False d': 'images/down_metal_wall.png',
                                        'False l': 'images/left_metal_wall.png',
                                        'False r': 'images/right_metal_wall.png',
                                        'True u': 'images/up_wall.png',
                                        'True d': 'images/down_wall.png',
                                        'True l': 'images/left_wall.png',
                                        'True r': 'images/right_wall.png'}
        self.names_of_images_prizes = {'1': 'images/heart.png',
                                        '2':'images/bomb_2.png',
                                        '3':'images/bomb_3.png'}
        self.names_of_images_bombs = {1: "images/bomb.png",
                                        2:'images/bomb_2.png',
                                        3:'images/bomb_3.png'}
        self.size_square = self.calculate_size_square()
        self.size_window = self.calculate_size_window()

        self.set_background("images/grass.png")
        self.bomb = Character_image(
                            self, self.level.Bomb, self.size_square,
                            "images/bomb.png")
        self.bomb.hide()

        for b in self.level.BomberMan:
            self.bomberman_image = Character_image(
                                        self, b, self.size_square,
                                        self.name_of_image_BM)

        self.prizes = []
        self.create_and_append_prizes()

        self.walls = []
        self.create_and_append_walls()

        self.monsters = []
        self.create_and_append_character(
                                        self.level.Monster,
                                        self.name_of_image_monster,
                                        self.monsters)

        self.lives = []
        self.draw_lives()

        self.bombs = []

        self.queue_moving_BM = []
        self.initUI()

    def calculate_size_square(self):
        return int(
            min(
                self.height/self.level.height,
                self.width/self.level.width
                )
            )

    def calculate_size_window(self):
        return (
            self.level.width * self.size_square,
            self.level.height * self.size_square
        )

    def create_and_append_walls(self):
        for w in self.level.Wall:
            self.walls.append(Character_image(
                self, w, self.size_square, self.names_of_images_walls[str(w)]))

    def create_and_append_prizes(self):
        for p in self.level.Prizes:
            self.prizes.append(Character_image(
                self, p, self.size_square, self.names_of_images_prizes[str(p).split(',')[1].split()[1]]))

    def create_and_append_character(
                    self, input_characters_list, image, finaly_characters_list):
        for character in input_characters_list:
            finaly_characters_list.append(Character_image(
                                    self, character, self.size_square, image))

    def draw_lives(self):
        self.lives.clear()
        for i in range(self.bomberman_image.character.count_of_lives):
            position = Point(i, 0)
            icon = Icon_image(self, position, self.size_square/3, 'images/heart.png')
            self.lives.append(icon)

    def set_background(self, image):
        self.background = QLabel(self)
        self.pixmap = QPixmap(image)
        self.background.setPixmap(self.pixmap)
        self.background.setGeometry(
            0,
            0,
            self.size_window[0],
            self.size_window[1]
        )

    def initUI(self):
        self.setGeometry(0, 25, self.size_window[0], self.size_window[1])
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(100, self)

        self.timer_monster = 0
        self.timer_BM = 0
        self.timer_immortality = 0
        self.timer_bomb = 0

        self.show()

    def show_gameover(self):
        go = QPushButton(self)
        icon = QIcon("images/Game_Over.png")
        go.setIcon(icon)
        go.setIconSize(QSize(self.size_window[0], self.size_window[1]))
        go.setStyleSheet("QPushButton {border:none; "
                         "background-color:transparent;}")
        go.setGeometry(0, 0, self.size_window[0], self.size_window[1])
        go.show()

    def timerEvent(self, e):
        direction = ['r', 'l', 'u', 'd']

        self.zeroize_timer(self.timer_monster)
        self.zeroize_timer(self.timer_BM)
        self.zeroize_timer(self.timer_immortality)
        self.zeroize_timer(self.timer_bomb)

        if not self.level.is_BM_lifes_changed:
            self.level.is_monster_kill_BM()
            self.timer_immortality = 1
            self.bomberman_image.set_picture(
                self.size_square,
                "images/person.png"
            )
        else:
            self.bomberman_image.set_picture(
                self.size_square,
                "images/person_hurt.png"
            )
            # self.lives.pop().hide()

        if not self.level.Bomb.is_active:
            self.timer_bomb = 1
            self.timer_fire = 1
        else:
            if self.timer_bomb % 30 == 0:
                self.boom()

        if self.timer_immortality % 17 == 0:
            self.level.is_BM_lifes_changed = False
            self.lives.pop().hide()

        if len(self.queue_moving_BM) > 0:
            self.moving(
                self.queue_moving_BM.pop(0),
                self.bomberman_image.character,
                self.bomberman_image
            )

        if self.level.is_gameover:
            self.show_gameover()
            self.bomberman_image.hide()
            self.timer.stop()

        # if self.timer_monster % 5 == 0:
        #     for m in self.monsters:
        #         r = random.randint(0, 3)
        #         self.moving(direction[r], m.character, m)

        self.timer_BM += 1
        self.timer_monster += 1
        self.timer_immortality += 1
        self.timer_bomb += 1
        self.step += 1

    def zeroize_timer(self, timer):
        if timer > 1000:
            timer = 0

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
        power = self.level.put_bomb()
        if power > 1:
            self.bombs.pop().hide()
        self.bomb.move(
            self.bomb.position.x * self.size_square,
            self.bomb.position.y * self.size_square
        )
        pixmap = QIcon(self.names_of_images_bombs[power])
        self.bomb.setIcon(pixmap)
        self.bomb.show()

    def update_field(self):
        self.update_character(self.walls, self.level.Wall, 'images/wall.png')
        self.update_character(
            self.monsters,
            self.level.Monster,
            'images/monster.png'
        )
        self.check_on_the_end_of_game()

    def check_on_the_end_of_game(self):
        if len(self.level.BomberMan) == 0:
            self.show_gameover()
            self.bomberman_image.hide()
            self.timer.stop()

    def update_character(self, list_of_butten, obj, image):
        removed = []
        for b in list_of_butten:
            if b.character not in obj:
                b.hide()
                removed.append(b)
        for b in removed:
            list_of_butten.remove(b)

    def boom(self):
        self.level.explode_bomb()
        self.bomb.hide()
        self.update_field()

    def moving(self, direction, level_character, button):
        self.level.moving(direction, level_character)
        button.move(
            button.position.x * self.size_square,
            button.position.y * self.size_square
        )
        self.paint_prize_and_icons(level_character)

    def paint_prize_and_icons(self, level_character):
        removed = []
        for p in self.prizes:
            if isinstance(level_character, BomberMan) and level_character.position == p.position:
                p.hide()
                removed.append(p)
                # self.paint_icon(p.character, Prize_life, self.lives, self.size_square/3, 'images/heart.png', 0)
                # power = self.bomberman_image.character.backpack[len(self.bomberman_image.character.backpack) - 1].power
                # self.paint_icon(p.character, Prize_bomb, self.bombs, self.size_square/3, self.names_of_images_bombs[power], 1)
                if isinstance(p.character, Prize_life):
                    position_life = Point(len(self.lives), 0)
                    icon_life = Icon_image(self, position_life, self.size_square/3, 'images/heart.png')
                    self.lives.append(icon_life)
                if isinstance(p.character, Prize_bomb):
                    position_bomb = Point(len(self.bombs), 1)
                    power = self.bomberman_image.character.backpack[len(self.bomberman_image.character.backpack) - 1].power
                    icon_bomb = Icon_image(self, position_bomb, self.size_square/3, self.names_of_images_bombs[power])
                    self.bombs.append(icon_bomb)
        for b in removed:
            self.prizes.remove(b)

    def paint_icon(self, prize, prize_type, array_prize, size, image, y_coordinate):
        if isinstance(prize, prize_type):
            position = Point(len(array_prize), y_coordinate)
            icon = Icon_image(self, position, size, image)
            array_prize.append(icon)
