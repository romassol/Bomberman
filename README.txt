Игра "Бомбермен"

Версия 0.7
Автор: Ромасс Ольга

Описание
Данное приложение является реализацией игры "Бомбермен".

Требования
Python версии не ниже 3.5
PyQt версии 5

Правила
Цель игры - уничтожить все кирпичные стены в уровнях с помощью бомб. Обычная бомба - радиус 1, количество - бесконечно; Усиленная бомба - радиус 2, можно найти, разрушив одну из кирпичных стен; Супер бомба - радиус 3, можно найти, разрушив одну из кирпичных стен. Жизнь - добавляет 1 жизнь бомбермену.

Начисление очков
Поставить обычную бомбу - -10
Подобрать приз(бомба, жизнь) - 5
Уничтожить стену - 5
Убить монстра - 100

Состав
Графическая версия: main.py
Консольная версия: console.py
Изображения: images/
Тесты:
    test_game.py
    test_level.py
    test_point.py
    test_reader.py

Графическая версия
Справка по запуску: python main.py --help
Пример запуска: python main.py -f level1.txt level2.txt
Управление: передвижение бомбермена: w - вверх, a - влево, s - вниз, d- вправо; z - поставить бомбу

Консольная версия
Пример запуска: python console.py -f level1.txt level2.txt
После запуска консольной версии нужно прописывать одну из заданных комманд, после чего будет выводится краткое описание ак
Команды: step direction - бомбермен делает шаг в нужно направлении, direction - r, d, u, l
         put - поставить бомбу
         explode index_of_bomb - взорвать бомбу с заданным индексом(начиная с 0)
         exit - завершить игру
Пример игры:
1. запускаем консольную версию, по умолчанию игра содержит два уровня -level1.txt level2.txt: python console.py
2. пошагово передаем команды, после каждой команды нажимаем enter для обработки этой команды и вывода произошедших событий
    step r
    BM position is 2 1
    put
    Bomb was put in 2 1
    step r
    BM position is 3 1
    step r
    BM position is 4 1
    explode 0
    Wall in 2 2 position was destroyed

Описание уровней в текстовом файле:
Пример:
{
    "monster speed": 1
    "field":
        # # # # # # *
        # B . . . M *
        # . * . U * #
        # D . # . . #
        # . r . d * #
        # . M . . . #
        # # # # # # #
    "prizes":
        . . . . . . .
        . . . . . . .
        . . 2 . . . .
        . . . . . . .
        . . 1 . 3 2 .
        . . . . . . .
        . . . . . . .
}
Уровень должен иметь 3 обязательных поля:
"monster speed" - скорость монстра,
"field" - B - bomberman
          . - nothing
          M - monster
          # - impassable not destroyed wall
          * - impassable destroyed wall
          U - passable up not destroyed wall
          D - passable down not destroyed wall
          R - passable right not destroyed wall
          L - passable left not destroyed wall
          u - passable up destroyed wall
          d - passable down destroyed wall
          r - passable right destroyed wall
          l - passable left destroyed wall,
"prizes" - 1 - life
           . - nothing
           2, 3 - bombs with a corresponding radius of defeat

Подробности реализации
В основе всего лежит класс Level, реализующий хранение персонажей, передвижение их и взаимодействие одних персонажей с другими (взрыв бомбы, соприкосновение бомбермена и монстров, бомбермена и призов). Класс Game содержит списко всех уровней и текущий уровень, осуществляет переход между уровнями. Класс Reader обрабатывает данные из json-формата.