#!/usr/bin/env python3

import re
import sys
import subclasses_exception
'''
import check_encoding
'''


def main(name, write_file):
    """
    Функция читает файл построчно и
    выполняет проверку строки стандартам PEP-8
    """
    '''
    encoding = check_encoding(name)
    if encoding is False:
        return
    '''
    orig_stdout = sys.stdout
    f = open('out_pep.txt', 'w')
    if write_file:
        sys.stdout = f

    file_to_check = open(name, 'r', encoding='utf-8')
    number_line = 0
    count_blank_lines = 0
    previous_count_space = 0
    in_class = False
    previous_class = False
    comm = False
    previous_import = -1
    for line in file_to_check:
        line = line.replace('\n', '')
        number_line += 1
        comm = is_comm(line, comm)
        if comm:
            check_comments(line, number_line)
            continue
        check_single_comm(line, number_line)
        previous_import = check_imports(line, number_line, previous_import)[2]
        check_lenght_string(line, number_line)
        count_blank_lines, in_class, previous_class, ex = \
            check_def_and_class(line, number_line,

                                count_blank_lines,
                                in_class, previous_class)
        check_extra_spaces(line, number_line)
        check_for_tabulation(line, number_line)
        check_for_semicolon(line, number_line)
        previous_count_space = check_spaces_at_the_beginning(
            line, number_line, previous_count_space)
        check_operators(line, number_line)
        check_equality_in_function_argument(line, number_line)
        check_key_words(line, number_line)
        check_brackets(line, number_line)
        check_commas(line, number_line)
        check_class_name(line, number_line)
        check_def_name(line, number_line)
        check_variables(line, number_line)
        check_none(line, number_line)
        check_true_false(line, number_line)
        check_startswith_endswith(line, number_line)
        check_isinstance(line, number_line)
        check_exceptions(line, number_line)
    file_to_check.close()
    f.close()
    sys.stdout = orig_stdout


def is_comm(line, comm):
    if (line.find('"""') != -1) and \
            (line.find('"""') == line.rfind('"""')) and not comm:
        comm = True
    elif (line.find('"""') != -1) and \
            (line.find('"""') == line.rfind('"""')) and comm:
        comm = False
    return comm


def check_single_comm(line, number_line):
    reg = re.compile(r'"""')
    arr = reg.findall(line)
    if len(arr) == 2:
        return check_comments(line, number_line)


def get_standart_modules():
    standart_modules = []
    for e in sys.builtin_module_names:
        standart_modules.append(e.replace('_', ''))
    return standart_modules


def check_exceptions(line, number_line):
    new_line = clean_quoted_strings(line)
    subclasses = subclasses_exception.get_subclasses_exception()
    flag = False
    if (new_line.find('except') != -1) or (new_line.find('raise') != -1):

        if new_line.find('except') != -1:
            column = new_line.find('except')
        else:
            column = new_line.find('raise')

        for e in subclasses:
            if new_line.find(e) != -1\
                    and new_line.find(e) != new_line.find('Exception'):
                flag = True

        if flag is False:
            print('line: {0}, column: {1} use excluded on classes'
                  ' - inherited from "Exception"'.format(number_line, column))


def check_startswith_endswith(line, number_line):
    """
    Функция проверяет, что вместо вырезки из строк
    для проверки префиксов и суффиксов
    используется ‘‘.startswith() и ‘‘.endswith()
    """
    ex1 = 'line: {0}, column: {1} use ".startswith()"'\
          ' instead of cutting from strings to test prefixes'
    ex2 = 'line: {0}, column: {1} use ".endswith()"'\
          ' instead of cutting from strings to test suffixes'
    if line.find('[:') != -1 and (line.find('==') != -1
                                  or line.find('!=') != -1):
        print(ex1.format(number_line, line.find('[:')))
        return ex1.format(number_line, line.find('[:'))
    if line.find('[0:') != -1 and (line.find('==') != -1
                                   or line.find('!=') != -1):
        print(ex1.format(number_line,  line.find('[0:')))
        return ex1.format(number_line, line.find('[0:'))
    if line.find(':]') != -1 and (line.find('==') != -1
                                  or line.find('!=') != -1):
        print(ex2.format(number_line, line.find(':]')))
        return ex2.format(number_line, line.find(':]'))
    if line.find(':len') != -1 and (line.find('==') != -1
                                    or line.find('!=') != -1):
        print(ex2.format(number_line, line.find(':len')))
        return ex2.format(number_line, line.find(':len'))


def check_isinstance(line, number_line):
    """
    Функция проверяет, что для проверки типа
    используется isinstance()
    """
    ex = 'line: {0}, column: {1} use ".isinstance()" to check the type'
    if line.find('type(') != -1 and (line.find('==') != -1
                                     or line.find('!=') != -1
                                     or line.find('is') != -1):
        print(ex.format(number_line, line.find('type(')))
        return ex.format(number_line, line.find('type('))
    if line.find('._class_') != -1 and (line.find('==') != -1
                                        or line.find('!=') != -1
                                        or line.find('is') != -1):
        print(ex.format(number_line, line.find('._class_')))
        return ex.format(number_line, line.find('._class_'))


def check_none(line, number_line):
    """
    Функция проверяет,
    что для проверки на None
    используется is или is not
    """
    none = line.find(r'None')
    ex1 = 'line: {0}, column: {1} comparison to None'\
          ' should be "if cond is None:"'
    ex2 = 'line: {0}, column: {1} comparison'\
          ' to None should be "if cond is not None:"'
    if none != -1 and line.find(r'==') != -1:
        print(ex1.format(number_line, line.find('==')))
        return ex1.format(number_line, line.find('=='))
    if none != -1 and line.find(r'!=') != -1:
        print(ex2.format(number_line, line.find('!=')))
        return ex2.format(number_line, line.find('!='))


def check_true_false(line, number_line):
    """
    Функция проверяет,
    что для проверки на True или False
    используется is или is not
    """
    true = line.find(r'True')
    false = line.find(r'False')
    ex1 = 'line: {0}, column: {1} comparison to True should be'\
          ' "if cond is True:" or "if cond:"'
    ex2 = 'line: {0}, column: {1} comparison to True should be'\
          ' "if cond is not True:" or "if not cond:"'
    ex3 = 'line: {0}, column: {1} comparison to False should be'\
          ' "if cond is False:" or "if not cond:"'
    ex4 = 'line: {0}, column: {1} comparison to False should be'\
          ' "if cond is not False:" or "if cond:"'
    if true != -1 and line.find(r'==') != -1:
        print(ex1.format(number_line, line.find('==')))
        return ex1.format(number_line, line.find('=='))
    if true != -1 and line.find(r'!=') != -1:
        print(ex2.format(number_line, line.find('!=')))
        return ex2.format(number_line, line.find('!='))
    if false != -1 and line.find(r'==') != -1:
        print(ex3.format(number_line, line.find('==')))
        return ex3.format(number_line, line.find('=='))
    if false != -1 and line.find(r'!=') != -1:
        print(ex4.format(number_line, line.find('!=')))
        return ex4.format(number_line, line.find('!='))


def check_comments(line, number_line):
    """
    Функция проверяет, что строка написана на английском языке
    """
    ex = 'line: {0} column: 0 comments should be written in English'
    try:
        line.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        print(ex.format(number_line))
        return ex.format(number_line)


def check_variables(line, number_line):
    """
    Функция проверяет, что в строке отстуствуют переменные с именами I, O, l
    """
    ex = 'line: {0}, column: {1} name{2}is bad name'
    bad_names = [' I ', ' O ', ' l ']
    for el in bad_names:
        arr = [m.start() for m in re.finditer(el, line)]
        if len(arr) != 0:
            for x in arr:
                print(ex.format(number_line, x, el))
                return ex.format(number_line, x, el)


def check_class_name(line, number_line):
    """
    Функция проверяет, что имя класса соответствует CamelCase
    """
    ex = 'line: {0}, column: {1} for the class name use CamelCase'
    start_class = line.find(r'class')
    if (start_class != -1) and (line[start_class + 5] == ' ') and\
       ((line[start_class - 1] == ' ') or (start_class == 0)):
        start_name = start_class + 6
        finish_name = line.find(r':')
        name = line[start_name:finish_name]
        if (not name[:1].isupper()) or (name.find(r'_') != -1):
            print(ex.format(number_line, start_name))
            return ex.format(number_line, start_name)


def check_def_name(line, number_line):
    """
    Функция проверяет, что имя функции
    соответствует lower_case_with_underscores
    """
    ex = 'line: {0}, column: {1}'\
         ' for the def name use lower_case_with_underscores'
    start_def = line.find(r'def')
    if (start_def != -1) and (line[start_def + 3] == ' ') and\
       ((line[start_def - 1] == ' ') or (start_def == 0)):
        start_name = start_def + 4
        finish_name = line.find(r'(')
        name = line[start_name:finish_name]
        flag = False
        for char in name:
            if char.isupper():
                flag = True
                break
        if flag:
            print(ex.format(number_line, start_name))
            return ex.format(number_line, start_name)


def check_commas(line, number_line):
    """
    Функция проверяет корректность пробелов вокруг знака ','
    """
    ex1 = 'line: {0}, column: {1} whitespace before ","'
    ex2 = 'line: {0}, column: {1} missing whitespace after ","'
    new_line = clean_quoted_strings(line)
    arr = [m.start() for m in re.finditer(',', new_line)]
    if len(arr) != 0:
        for x in arr:
            if (x - 1 > 0) and (new_line[x - 1] == ' '):
                print(ex1.format(number_line, x))
                return ex1.format(number_line, x)
            if (x + 1 < len(new_line)) and (new_line[x + 1] != ' '):
                print(ex2.format(number_line, x))
                return ex2.format(number_line, x)


def check_brackets(line, number_line):
    """
    Функция проверяет корректность пробелов вокруг скобок
    """
    ex1 = 'line: {0}, column: {1} whitespace after "["'
    ex2 = 'line: {0}, column: {1} whitespace after "("'
    ex3 = 'line: {0}, column: {1} whitespace before "]"'
    ex4 = 'line: {0}, column: {1} whitespace before ")"'
    new_line = clean_quoted_strings(line)
    if new_line.find('[') != -1:
        x = new_line.find('[')
        if new_line[x + 1] == ' ':
            print(ex1.format(number_line, x))
            return ex1.format(number_line, x)
    if new_line.find('(') != -1:
        y = new_line.find('(')
        if new_line[y + 1] == ' ':
            print(ex2.format(number_line, y))
            return ex2.format(number_line, y)
    if new_line.find(']') != -1:
        z = new_line.find(']')
        if new_line[z - 1] == ' ':
            print(ex3.format(number_line, z))
            return ex3.format(number_line, z)
    if new_line.find(')') != -1:
        c = new_line.find(')')
        if new_line[c - 1] == ' ':
            print(ex4.format(number_line, c))
            return ex4.format(number_line, c)


def check_operators(line, number_line):
    """
    Функция проверяет пробелы вокруг операторов
    """
    ex = 'line: {0}, column: {1} missing whitespace around operator'
    operators = ['+', '-', '*', '/', '%', '//', '..', '=',
                 '+=', '-=', '*=', '/=', '%=', '**=', '//=',
                 '==', '<', '>', '!=', '<>', '<=', '>=',
                 '&', '|', '^', '`', '>>', '<<']
    regex = re.compile(r'[/+-/*/%.=<>!&|^`]+')
    if (line.find('def') == -1) and (line.find('#') == -1) and\
       (line.find('-1') == -1):
        line = clean_quoted_strings(line)
        operator_arr = regex.findall(line)
        for e in operator_arr:
            if e in operators:
                point = line.find(e)
                if (line[point - 1] != ' ') or (line[point - 2] == ' ') or\
                   (line[point + len(e)] != ' ') or\
                   (line[point + len(e) + 1] == ' '):
                    print(ex.format(number_line, point))
                    return ex.format(number_line, point)


def clean_quoted_strings(line):
    """
    Функция очищает строку от строк в кавычках
    """
    reg = re.compile(r'\'[\w\W]+\'|\"[\w\W]+\"')
    if (line.find('\'') != -1) or (line.find('\"') != -1):
        str_arr = reg.findall(line)
        for s in str_arr:
            line = line.replace(s, 'x')
    return line


def check_equality_in_function_argument(line, number_line):
    """
    Функция проверяет отсутствие пробелов вокруг = в аргументах функции
    """
    ex = 'line: {0}, column: {1}'\
         ' unexpected spaces around keyword / parameter equals'
    if (line.find('def') != -1) and (line.find('=') != -1):
        line = clean_quoted_strings(line)
        point = line.find('=')
        if (line[point - 1] == ' ') or (line[point + 1] == ' '):
            print(ex.format(number_line, point))
            return ex.format(number_line, point)


def check_key_words(line, number_line):
    """
    Функция проверяет наличие одного пробела
    и не более вокруг ключевых слов
    """
    ex1 = 'line: {0}, column: {1} missing whitespace around keyword'
    ex2 = 'line: {0}, column: {1} multiple spaces around keyword'
    keywords = ['and', 'or', 'not', 'in', 'is']
    new_line = clean_quoted_strings(line)
    for el in keywords:
        arr = [m.start() for m in re.finditer(el, new_line)]
        if len(arr) != 0:
            for x in arr:
                if (x - 1 > 0) and (x + len(el) < len(new_line)) and\
                   (not new_line[x - 1].isalpha()) and\
                   (not new_line[x + len(el)].isalpha()):
                    if (new_line[x - 1] == ')') or\
                       (new_line[x + len(el)] == '('):
                        print(ex1.format(number_line, x))
                        return ex1.format(number_line, x)
                    if ((new_line[x - 1] == ' ')
                        and (new_line[x - 2] == ' ')) or\
                            ((new_line[x + len(el)] == ' ')
                             and (new_line[x + len(el) + 1] == ' ')):
                        print(ex2.format(number_line, x))
                        return ex2.format(number_line, x)


def check_extra_spaces(line, number_line):
    """
    Функция проверяет отсутсвие лишних пробелов в конце строки
    """
    ex = 'line: {0}, column: {1} trailing whitespace'
    if line.endswith(' '):
        print(ex.format(number_line, len(line)))
        return ex.format(number_line, len(line))


def check_imports(line, number_line, previous_import):
    """
    Функция проверяет корректность модуля import стандарту PEP-8
    """
    ex1 = 'line: {0}, column: {1} multiple imports on one line'
    ex2 = 'line: {0}, column: {1} the group of imports'\
          ' of standard modules should go first and should not contain spaces'
    result1 = ''
    result2 = ''
    number_symbol = line.find(',')
    flag = False
    if line[:6] == 'import':
        if line.find('from') == -1 and (number_symbol != -1):
            result1 = ex1.format(number_line, number_symbol)
            print(result1)
        standart_modules = get_standart_modules()
        for e in standart_modules:
            if line.find(e) != -1 and line.find(e) != line.find('import'):
                flag = True
        if flag:
            if previous_import != -1 and number_line - previous_import > 1:
                result2 = ex2.format(number_line, 0)
                print(result2)
            previous_import = number_line
    return (result1, result2, previous_import)


def check_def_and_class(line, number_line, count_blank_lines,
                        in_class, previous_class):
    """
    Функция проверяет соответствует ли количество пробелов
    между функциями и классами стандарту PEP-8
    """
    ex1 = 'line: {0}, column: 0 too many blank lines ({1})'
    ex2 = 'line: {0}, column: 0 too few empty lines ({1})'
    ex3 = 'line: {0}, column: 0 blank line contains whitespace'
    ex = ''
    if len(line) == 0:
        count_blank_lines += 1
    else:
        if line[0] != ' ' and in_class:
            in_class = False
        if ((line.find('class') != -1)
                or (line.find('def') != -1)
                or (line.find(r"if __name__ == '__main__':") != -1)):
            if in_class is True:
                if count_blank_lines > 1 and previous_class is False:
                    ex = ex1.format(number_line, count_blank_lines)
                    print(ex)
                elif count_blank_lines < 1 and previous_class is False:
                    ex = ex2.format(number_line, count_blank_lines)
                    print(ex)
                elif count_blank_lines != 0 and previous_class is True:
                    ex = ex3.format(number_line)
                    print(ex)
                count_blank_lines = 0
                previous_class = False
            elif in_class is False:
                if count_blank_lines > 2:
                    ex = ex1.format(number_line, count_blank_lines)
                    print(ex)
                elif count_blank_lines < 2:
                    ex = ex2.format(number_line, count_blank_lines)
                    print(ex)
                count_blank_lines = 0
                in_class = True
                previous_class = True
        else:
            if count_blank_lines != 0:
                ex = ex3.format(number_line)
                print(ex)
            count_blank_lines = 0
    return (count_blank_lines, in_class, previous_class, ex)


def check_for_tabulation(line, number_line):
    """
    Функция проверяет отсутствие табуляции в коде
    """
    ex = 'line: {0}, column: {1} unexpected indentation'
    if line.find('\t') != -1:
        print(ex.format(number_line, line.find('\t')))
        return ex.format(number_line, line.find('\t'))


def check_for_semicolon(line, number_line):
    """
    Функция проверяет отсутствие знака ';' в коде
    """
    ex = 'line: {0}, column: {1} statement ends with a semicolon'
    if line.find(';') != -1:
        print(ex.format(number_line, line.find(';')))
        return ex.format(number_line, line.find(';'))


def check_spaces_at_the_beginning(line, number_line, previous_count_space):
    """
    Функция проверяет соответствуют ли отступы
    в начале строки стандарту PEP-8
    """
    ex1 = 'line: {0}, column: {1} indentation is not a multiple of four'
    ex2 = 'line: {0}, column: {1} unexpected indentation'
    number_symbol = 0
    count_of_spaces = 0
    for char in line:
        number_symbol += 1
        if char == ' ':
            count_of_spaces += 1
        else:
            break
    if count_of_spaces % 4 != 0:
        print(ex1.format(number_line, number_symbol))
    if (count_of_spaces > previous_count_space) and\
       (count_of_spaces != previous_count_space + 4):
        print(ex2.format(number_line, number_symbol))
    previous_count_space = count_of_spaces
    return previous_count_space


def check_lenght_string(line, number_line):
    """
    Функция проверяет соответствует длина строки стандарту PEP-8
    """
    ex = 'line: {0}, column: 80 line too long ({1} > 79 characters)'
    max_lenght = 79
    if len(line) > max_lenght:
        print(ex.format(number_line, len(line)))
        return ex.format(number_line, len(line))


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == 'help'):
        print("""Программа проверяет код на соответствие формату PEP-8.
Файл для проверки должен лежать в той же директории, что и pep-8.py.
Пример запуска: python pep-8.py 'test.py'""")
    elif len(sys.argv) == 1:
        print("Аргумент для проверки отсутствует. Посмотрите help.")
    else:
        main(sys.argv[1], False)
