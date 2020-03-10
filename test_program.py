#!/usr/bin/env python3

import pep as t
import subclasses_exception
import unittest


class Testpep(unittest.TestCase):
    def test_check_good_comment(self):
        result = t.check_comments('Good comment', 1)
        self.assertEqual(result, None)

    def test_check_bad_comment(self):
        ex = 'line: 2 column: 0 comments should be written in English'
        result = t.check_comments('Плохой комментарий', 2)
        self.assertEqual(result, ex)

    def test_check_bad_variable_I(self):
        ex = 'line: 3, column: 3 name I is bad name'
        result = t.check_variables('    I = 5', 3)
        self.assertEqual(result, ex)

    def test_check_bad_variable_O(self):
        ex = 'line: 4, column: 3 name O is bad name'
        result = t.check_variables('    O = 6', 4)
        self.assertEqual(result, ex)

    def test_check_bad_variable_l(self):
        ex = 'line: 5, column: 3 name l is bad name'
        result = t.check_variables('    l = 7', 5)
        self.assertEqual(result, ex)

    def test_check_good_variable(self):
        result = t.check_variables('    a = 7', 6)
        self.assertEqual(result, None)

    def test_check_bad_class_name(self):
        ex = 'line: 7, column: 6 for the class name use CamelCase'
        result = t.check_class_name('class bad_class:', 7)
        self.assertEqual(result, ex)

    def test_check_good_class_name(self):
        result = t.check_class_name('class GoodClass:', 8)
        self.assertEqual(result, None)

    def test_check_bad_def_name(self):
        ex = 'line: 9, column: 4'\
             ' for the def name use lower_case_with_underscores'
        result = t.check_def_name('def BadDef', 9)
        self.assertEqual(result, ex)

    def test_check_good_def_name(self):
        result = t.check_def_name('def good_def', 10)
        self.assertEqual(result, None)

    def test_check_whitespace_before_commas(self):
        ex = 'line: 11, column: 9 whitespace before ","'
        result = t.check_commas('arr = [1 , 2]', 11)
        self.assertEqual(result, ex)

    def test_check_whitespace_after_commas(self):
        ex = 'line: 12, column: 8 missing whitespace after ","'
        result = t.check_commas('arr = [1,2]', 12)
        self.assertEqual(result, ex)

    def test_check_good_whitespaces_commas(self):
        result = t.check_commas('arr = [1, 2]', 13)
        self.assertEqual(result, None)

    def test_check_whitespace_after_square_bracket(self):
        ex = 'line: 14, column: 6 whitespace after "["'
        result = t.check_brackets('arr = [ 1, 2]', 14)
        self.assertEqual(result, ex)

    def test_check_whitespace_before_square_bracket(self):
        ex = 'line: 15, column: 12 whitespace before "]"'
        result = t.check_brackets('arr = [1, 2 ]', 15)
        self.assertEqual(result, ex)

    def test_check_whitespace_after_round_bracket(self):
        ex = 'line: 16, column: 6 whitespace after "("'
        result = t.check_brackets('set = ( 1, 2)', 16)
        self.assertEqual(result, ex)

    def test_check_whitespace_before_round_bracket(self):
        ex = 'line: 17, column: 12 whitespace before ")"'
        result = t.check_brackets('set = (1, 2 )', 17)
        self.assertEqual(result, ex)

    def test_check_good_whitespaces_square_brackets(self):
        result = t.check_brackets('arr = [1, 2]', 18)
        self.assertEqual(result, None)

    def test_check_good_whitespaces_round_brackets(self):
        result = t.check_brackets('set = (1, 2)', 19)
        self.assertEqual(result, None)

    def test_check_good_operators(self):
        operators = [' + ', ' - ', ' * ', ' / ', ' % ', ' // ', ' .. ', ' = ',
                     ' += ', ' -= ', ' *= ', ' /= ', ' %= ', ' **= ', ' //= ',
                     ' == ', ' < ', ' > ', ' != ', ' <> ', ' <= ', ' >= ',
                     ' & ', ' | ', ' ^ ', ' ` ', ' >> ', ' << ']
        for e in operators:
            result = t.check_operators('sum = 5{0}4'.format(e), 20)
            self.assertEqual(result, None)

    def test_check_bad_operators(self):
        ex = 'line: 21, column: 8 missing whitespace around operator'
        operators = ['+', '-', '*', '/', '%', '//', '..', '=',
                     '+=', '-=', '*=', '/=', '%=', '**=', '//=',
                     '==', '<', '>', '!=', '<>', '<=', '>=',
                     '&', '|', '^', '`', '>>', '<<']
        for e in operators:
            result = t.check_operators('if count{0}4'.format(e), 21)
            self.assertEqual(result, ex)

    def test_check_good_equality_in_function_arguments(self):
        result = t.check_equality_in_function_argument(
            'def check(arg, sum=5):', 22)
        self.assertEqual(result, None)

    def test_check_bad_equality_in_function_arguments(self):
        ex = 'line: 23, column: 15 unexpected spaces around keyword'\
             ' / parameter equals'
        result = t.check_equality_in_function_argument('def check(a, b = 3):',
                                                       23)
        self.assertEqual(result, ex)

    def test_check_good_whitespaces_around_key_words(self):
        keywords = ['and', 'or', 'not', 'in', 'is']
        for e in keywords:
            result = t.check_key_words('if a = 3 {0} b = 4:'.format(e), 24)
            self.assertEqual(result, None)

    def test_check_bad_whitespaces_around_key_words(self):
        keywords = ['and', 'or', 'not', 'in', 'is']
        ex = 'line: 25, column: 9 missing whitespace around keyword'
        for e in keywords:
            result = t.check_key_words('if (flag){0}(sum == max):'
                                       .format(e), 25)
            self.assertEqual(result, ex)

    def test_check_very_bad_whitespaces_around_key_words(self):
        keywords = ['and', 'or', 'not', 'in', 'is']
        ex = 'line: 26, column: 15 multiple spaces around keyword'
        for e in keywords:
            result = t.check_key_words('if sum == max  {0}  flag:'
                                       .format(e), 26)
            self.assertEqual(result, ex)

    def test_check_good_extra_spaces(self):
        result = t.check_extra_spaces('flag = True', 27)
        self.assertEqual(result, None)

    def test_check_bad_extra_spaces(self):
        ex = 'line: 28, column: 14 trailing whitespace'
        result = t.check_extra_spaces('flag = False  ', 28)
        self.assertEqual(result, ex)

    def test_check_good_imports(self):
        result = t.check_imports('import sys', 29, 28)
        self.assertEqual(result[0], '')

    def test_check_bad_import_first(self):
        ex = 'line: 30, column: 10 multiple imports on one line'
        result = t.check_imports('import sys, re', 30, 29)
        self.assertEqual(result[0], ex)

    def test_check_bad_imports_second(self):
        ex = 'line: 30, column: 0 the group of imports of standard'\
            ' modules should go first and should not contain spaces'
        result = t.check_imports('import sys', 30, 28)
        self.assertEqual(result[1], ex)

    def test_good_check_for_tabulation(self):
        result = t.check_for_tabulation('    count = 5', 31)
        self.assertEqual(result, None)

    def test_bad_check_for_tabulation(self):
        ex = 'line: 32, column: 0 unexpected indentation'
        result = t.check_for_tabulation('\tcount = 7', 32)
        self.assertEqual(result, ex)

    def test_good_check_for_semicolon(self):
        result = t.check_for_semicolon('x, y = 1, 1', 33)
        self.assertEqual(result, None)

    def test_bad_check_for_semicolon(self):
        ex = 'line: 34, column: 11 statement ends with a semicolon'
        result = t.check_for_semicolon('return True;', 34)
        self.assertEqual(result, ex)

    def test_good_check_lenght_string(self):
        result = t.check_lenght_string('small string', 35)
        self.assertEqual(result, None)

    def test_bad_check_lenght_string(self):
        ex = 'line: 36, column: 80 line too long (109 > 79 characters)'
        result = t.check_lenght_string('This is very very very very'
                                       ' very very very very very'
                                       ' very very very very very'
                                       ' very very very very long'
                                       ' string', 36)
        self.assertEqual(result, ex)

    def test_clean_quoted_strings(self):
        line = 'a = "tyty"'
        line2 = 'b = \'tyty\''
        result = t.clean_quoted_strings(line)
        result2 = t.clean_quoted_strings(line2)
        self.assertEqual(result, 'a = x')
        self.assertEqual(result2, 'b = x')

    def test_check_startswith_endswith_starts_with_first(self):
        ex1 = 'line: 37, column: {0} use ".startswith()"' \
              ' instead of cutting from strings to test prefixes'
        result1 = t.check_startswith_endswith('a[:4] == "abcd"', 37)
        result2 = t.check_startswith_endswith('a[:4] != "abcd"', 37)
        self.assertEqual(result1, ex1.format(1))
        self.assertEqual(result2, ex1.format(1))

    def test_check_startswith_endswith_starts_with_second(self):
        ex1 = 'line: 38, column: {0} use ".startswith()"' \
              ' instead of cutting from strings to test prefixes'
        result1 = t.check_startswith_endswith('a[0:4] == "abcd"', 38)
        result2 = t.check_startswith_endswith('a[0:4] != "abcd"', 38)
        self.assertEqual(result1, ex1.format(1))
        self.assertEqual(result2, ex1.format(1))

    def test_check_startswith_endswith_starts_with_good(self):
        result1 = t.check_startswith_endswith('a.startswith("abcd")', 39)
        result2 = t.check_startswith_endswith('not a.startswith("abcd")', 39)
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_check_startswith_endswith_ends_with_first(self):
        ex2 = 'line: 40, column: {0} use ".endswith()"'\
          ' instead of cutting from strings to test suffixes'
        result1 = t.check_startswith_endswith('a[4:] == "abcd"', 40)
        result2 = t.check_startswith_endswith('a[4:] != "abcd"', 40)
        self.assertEqual(result1, ex2.format(3))
        self.assertEqual(result2, ex2.format(3))

    def test_check_startswith_endswith_ends_with_second(self):
        ex2 = 'line: 41, column: {0} use ".endswith()"'\
          ' instead of cutting from strings to test suffixes'
        result1 = t.check_startswith_endswith('a[4:len(a) - 1] == "abcd"', 41)
        result2 = t.check_startswith_endswith('a[4:len(a) - 1] != "abcd"', 41)
        self.assertEqual(result1, ex2.format(3))
        self.assertEqual(result2, ex2.format(3))

    def test_check_startswith_endswith_ends_with_good(self):
        result1 = t.check_startswith_endswith('a.endswith("abcd")', 42)
        result2 = t.check_startswith_endswith('not a.endswith("abcd")', 42)
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_check_isinstance_type(self):
        ex = 'line: 43, column: {0} use ".isinstance()" to check the type'
        result1 = t.check_isinstance('type(5) == int', 43)
        result2 = t.check_isinstance('type(5,5) != int', 43)
        result3 = t.check_isinstance('type(5) is int', 43)
        result4 = t.check_isinstance('type(5,5) is not int', 43)
        self.assertEqual(result1, ex.format(0))
        self.assertEqual(result2, ex.format(0))
        self.assertEqual(result3, ex.format(0))
        self.assertEqual(result4, ex.format(0))

    def test_check_isinstance_class(self):
        ex = 'line: 44, column: {0} use ".isinstance()" to check the type'
        result1 = t.check_isinstance('5._class_ == int', 44)
        result2 = t.check_isinstance('(5,5)._class_ != int', 44)
        result3 = t.check_isinstance('5._class_ is int', 44)
        result4 = t.check_isinstance('(5,5)._class_ is not int', 44)
        self.assertEqual(result1, ex.format(1))
        self.assertEqual(result2, ex.format(5))
        self.assertEqual(result3, ex.format(1))
        self.assertEqual(result4, ex.format(5))

    def test_check_isinstance_good(self):
        result1 = t.check_isinstance('isinstance(5, int)', 45)
        result2 = t.check_isinstance('not isinstance(5,5, int)', 45)
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_check_none_is(self):
        ex1 = 'line: 46, column: {0} comparison to None' \
              ' should be "if cond is None:"'
        result1 = t.check_none('a == None', 46)
        self.assertEqual(result1, ex1.format(2))

    def test_check_none_is_not(self):
        ex2 = 'line: 47, column: {0} comparison'\
          ' to None should be "if cond is not None:"'
        result2 = t.check_none('a != None', 47)
        self.assertEqual(result2, ex2.format(2))

    def test_check_none_good(self):
        result1 = t.check_none('a is None', 48)
        result2 = t.check_none('b is not None', 48)
        self.assertEqual(result1, None)
        self.assertEqual(result2, None)

    def test_check_true_false_true_is(self):
        ex1 = 'line: 49, column: {0} comparison to True should be' \
              ' "if cond is True:" or "if cond:"'
        result1 = t.check_true_false('flag == True', 49)
        self.assertEqual(result1, ex1.format(5))

    def test_check_true_false_true_is_not(self):
        ex2 = 'line: 50, column: {0} comparison to True should be'\
          ' "if cond is not True:" or "if not cond:"'
        result2 = t.check_true_false('flag != True', 50)
        self.assertEqual(result2, ex2.format(5))

    def test_check_true_false_false_is(self):
        ex3 = 'line: 51, column: {0} comparison to False should be'\
          ' "if cond is False:" or "if not cond:"'
        result3 = t.check_true_false('flag == False', 51)
        self.assertEqual(result3, ex3.format(5))

    def test_check_true_false_false_is_not(self):
        ex4 = 'line: 52, column: {0} comparison to False should be'\
          ' "if cond is not False:" or "if cond:"'
        result4 = t.check_true_false('flag != False', 52)
        self.assertEqual(result4, ex4.format(5))

    def test_check_true_false_good(self):
        results = []
        results.append(t.check_true_false('if flag is True', 53))
        results.append(t.check_true_false('if True', 53))
        results.append(t.check_true_false('if flag is not True', 53))
        results.append(t.check_true_false('if not True', 53))
        results.append(t.check_true_false('if flag is False', 53))
        results.append(t.check_true_false('if not False', 53))
        results.append(t.check_true_false('if flag is not False', 53))
        results.append(t.check_true_false('if False', 53))
        for e in results:
            self.assertEqual(e, None)

    def test_check_def_and_class_not_in_class_class(self):
        ex1 = 'line: 54, column: 0 too many blank lines ({0})'
        ex2 = 'line: 54, column: 0 too few empty lines ({0})'
        result1 = t.check_def_and_class("class Game:", 54, 3, False, False)[3]
        result2 = t.check_def_and_class("class Game:", 54, 1, False, False)[3]
        self.assertEqual(result1, ex1.format(3))
        self.assertEqual(result2, ex2.format(1))

    def test_check_def_and_class_not_in_class_def(self):
        ex1 = 'line: 55, column: 0 too many blank lines ({0})'
        ex2 = 'line: 55, column: 0 too few empty lines ({0})'
        result1 = t.check_def_and_class("def get_square(a, b):",
                                        55, 3, False, False)[3]
        result2 = t.check_def_and_class("def get_square(a, b):",
                                        55, 1, False, False)[3]
        self.assertEqual(result1, ex1.format(3))
        self.assertEqual(result2, ex2.format(1))

    def test_check_def_and_class_in_class_class(self):
        ex1 = 'line: 56, column: 0 too many blank lines ({0})'
        ex2 = 'line: 56, column: 0 too few empty lines ({0})'
        result1 = t.check_def_and_class("    class Game:",
                                        56, 2, True, False)[3]
        result2 = t.check_def_and_class("    class Game:",
                                        56, 0, True, False)[3]
        self.assertEqual(result1, ex1.format(2))
        self.assertEqual(result2, ex2.format(0))

    def test_check_def_and_class_in_class_def(self):
        ex1 = 'line: 57, column: 0 too many blank lines ({0})'
        ex2 = 'line: 57, column: 0 too few empty lines ({0})'
        result1 = t.check_def_and_class("    def get_square(a, b):",
                                        57, 2, True, False)[3]
        result2 = t.check_def_and_class("    def get_square(a, b):",
                                        57, 0, True, False)[3]
        self.assertEqual(result1, ex1.format(2))
        self.assertEqual(result2, ex2.format(0))

    def test_check_def_and_class_in_class_previous_class(self):
        ex = 'line: 58, column: 0 blank line contains whitespace'
        result = t.check_def_and_class("    def get_square(a, b):",
                                       58, 1, True, True)[3]
        self.assertEqual(result, ex)

    def test_check_def_and_class_empty(self):
        ex = 'line: 59, column: 0 blank line contains whitespace'
        results = []
        results.append(t.check_def_and_class("sum = a + b",
                                             59, 1, False, False)[3])
        results.append(t.check_def_and_class("sum = a + b",
                                             59, 1, True, False)[3])
        results.append(t.check_def_and_class("sum = a + b",
                                             59, 1, True, True)[3])
        for e in results:
            self.assertEqual(e, ex)

    def test_subclasses_exception(self):
        result = subclasses_exception.get_subclasses_exception()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Exception')

    def test_get_modules(self):
        result = t.get_standart_modules()
        self.assertIsNotNone(result)

    def test_is_comm_True(self):
        current_comm = t.is_comm('"""', False)
        self.assertTrue(current_comm)

    def test_is_comm_False(self):
        arr = []
        arr.append('"""')
        arr.append('it is comm')
        arr.append('"""')
        current_comm = False
        for el in arr:
            current_comm = t.is_comm(el, current_comm)
        self.assertFalse(current_comm)

    def test_check_single_comm_good(self):
        result = t.check_single_comm('"""It is single comm"""', 60)
        self.assertIsNone(result)

    def test_check_single_comm_bad(self):
        ex = 'line: 61 column: 0 comments should be written in English'
        result = t.check_single_comm('"""Это однострочный комментарий"""', 61)
        self.assertEqual(result, ex)

    def test_pep_main_start(self):
        t.main('test.txt', True)
        f = open('out_pep.txt', 'w')
        self.assertIsNotNone(f)


if __name__ == '__main__':
    unittest.main()
