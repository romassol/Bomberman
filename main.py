from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import argparse
import sys

from graphic import Visualization


__version__ = '0.7'
__author__ = 'Romass Olga'


def get_argparse():
    parser = argparse.ArgumentParser(
        usage='%(prog)s play',
        description='Bombermen game. Version {}'.format(__version__),
        epilog='Author: {}'.format(__author__))

    parser.add_argument(
        '-f',
        '--files',
        nargs='+',
        default=['level1.txt', 'level2.txt'],
        help='List of a levels')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = get_argparse()
    app = QApplication(sys.argv)
    ex = Visualization(arguments.files)
    ex.show()
    sys.exit(app.exec_())
