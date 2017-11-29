���� "���������"

������ 0.7
�����: ������ �����

��������
������ ���������� �������� ����������� ���� "���������".

����������
Python ������ �� ���� 3.5
PyQt ������ 5

�������
���� ���� - ���������� ��� ��������� ����� � ������� � ������� ����. ������� ����� - ������ 1, ���������� - ����������; ��������� ����� - ������ 2, ����� �����, �������� ���� �� ��������� ����; ����� ����� - ������ 3, ����� �����, �������� ���� �� ��������� ����. ����� - ��������� 1 ����� ����������.

���������� �����
��������� ������� ����� - -10
��������� ����(�����, �����) - 5
���������� ����� - 5
����� ������� - 100

������
����������� ������: main.py
���������� ������: console.py
�����������: images/
�����:
    test_game.py
    test_level.py
    test_point.py
    test_reader.py

����������� ������
������� �� �������: python main.py --help
������ �������: python main.py -f level1.txt level2.txt
����������: ������������ ����������: w - �����, a - �����, s - ����, d- ������; z - ��������� �����

���������� ������
������ �������: python console.py -f level1.txt level2.txt
����� ������� ���������� ������ ����� ����������� ���� �� �������� �������, ����� ���� ����� ��������� ������� �������� ��
�������: step direction - ��������� ������ ��� � ����� �����������, direction - r, d, u, l
         put - ��������� �����
         explode index_of_bomb - �������� ����� � �������� ��������(������� � 0)
         exit - ��������� ����
������ ����:
1. ��������� ���������� ������, �� ��������� ���� �������� ��� ������ -level1.txt level2.txt: python console.py
2. �������� �������� �������, ����� ������ ������� �������� enter ��� ��������� ���� ������� � ������ ������������ �������
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

�������� ������� � ��������� �����:
������:
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
������� ������ ����� 3 ������������ ����:
"monster speed" - �������� �������,
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

����������� ����������
� ������ ����� ����� ����� Level, ����������� �������� ����������, ������������ �� � �������������� ����� ���������� � ������� (����� �����, ��������������� ���������� � ��������, ���������� � ������). ����� Game �������� ������ ���� ������� � ������� �������, ������������ ������� ����� ��������. ����� Reader ������������ ������ �� json-�������.