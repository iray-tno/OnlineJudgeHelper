#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
class Validator
class DiffValidator
class FloatingPointValidator
"""

import subprocess


class Validator(object):
    def validate(self, answer_path, output_path):
        raise NotImplementedError


class DiffValidator(Validator):
    def validate(self, answer_path, output_path):
        return subprocess.call([
            'diff',
            answer_path,
            output_path,
            '-y',
            '--strip-trailing-cr',
            '-W',
            '79',
            '-a',
            '-d']
        ) == 0


class FloatingPointValidator(Validator):
    absolute_error = None

    def __init__(self, absolute_error):
        self.absolute_error = float(absolute_error)

    def validate(self, answer_path, output_path):
        answer_file = open(answer_path)
        output_file = open(output_path)
        result = True
        print '%-25s %-25s   %s' % ('answer', 'output', 'diff')
        while True:
            answer_line = answer_file.readline()
            output_line = output_file.readline()

            if answer_line == '' and output_line == '':
                break

            answer_line = answer_line.strip()
            output_line = output_line.strip()

            answer_value = float(answer_line)
            output_value = float(output_line)
            ok = False
            diff = output_value - answer_value

            if abs(diff) < self.absolute_error:
                ok = True

#            if abs(answer_value) > absolute_error:
#                if abs((answer_value - output_value) / answer_value)
#                    < relative_error:
#                    ok = True

            separator = ' '

            if not ok:
                separator = '|'
                result = False

            print '%-25s %-25s %s %e' \
                % (answer_line, output_line, separator, diff)
        return result


def main():
    print __doc__

if __name__ == '__main__':
    main()
