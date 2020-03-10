#!/usr/bin/env python3
import sys
import pep
from ctypes import *


def main(filename, write_file):
    orig_stdout = sys.stdout
    f = open('out_color_pep.txt', 'w')
    if write_file:
        sys.stdout = f
    pep.main(filename, True)
    list_exceptions = get_list_with_exceptions()6

    windll.Kernel32.GetStdHandle.restype = c_ulong
    h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

    file_for_check = open(filename, 'r')
    number_line = 0
    for line in file_for_check:
        newline = line.replace('\n', '')
        number_line += 1
        has_exception = False
        for e in list_exceptions:
            if number_line == e[0]:
                has_exception = True
        if has_exception:
            windll.Kernel32.SetConsoleTextAttribute(h, 12)
            print('{0}. '.format(number_line) + newline)
            get_all_exceptions(list_exceptions, number_line, h)
        else:
            windll.Kernel32.SetConsoleTextAttribute(h, 7)
            print('{0}. '.format(number_line) + newline)
    file_for_check.close()
    sys.stdout = orig_stdout
    f.close()


def get_list_with_exceptions():
    list_exceptions = []
    file_with_exceptions = open('out_pep.txt', 'r')
    for line in file_with_exceptions:
        end = (line[line.find('line:') + 6:]).find(' ') \
              + line.find('line:') + 5
        row = int(line[line.find('line:') + 6:end])
        exception = line[line.find('column:'):-1]
        list_exceptions.append((row, exception))
    file_with_exceptions.close()
    return list_exceptions


def get_all_exceptions(list_exceptions, number_line, h):
    for e in list_exceptions:
        if number_line == e[0]:
            windll.Kernel32.SetConsoleTextAttribute(h, 10)
            print('fail: ' + e[1])


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == 'help'):
        print("""Программа проверяет код на соответствие формату PEP-8.
        Файл для проверки должен лежать в той же директории, что и pep-8.py.
        Пример запуска: python pep-8.py 'test.py'""")
    elif len(sys.argv) == 1:
        print("Аргумент для проверки отсутствует. Посмотрите help.")
    else:
        main(sys.argv[1], False)
