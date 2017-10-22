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
        '-f', '--file', type=str,
        metavar='FILENAME', default='input.txt', help='file of field')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = get_argparse()
    app = QApplication(sys.argv)
    ex = Visualization(arguments.file)
    sys.exit(app.exec_())
