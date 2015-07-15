#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
class Solution
class SolutionC
class SolutionCxx
class SolutionJava
class SolutionIo
class SolutionPhp
class SolutionPython
class SolutionPerl
class SolutionRuby
class SolutionHaskell
"""

import subprocess
import time


class Solution(object):
    def __init__(self, source_file_name):
        self.source_file_name = source_file_name

    def compile(self):
        raise NotImplementedError

    def execute(self, input_file_path, output_file_path):
        start_time = time.time()
        p = subprocess.Popen(self.get_execute_command_line(),
                             stdin=open(input_file_path, 'r'),
                             stdout=open(output_file_path, 'w'))
        if p.wait() != 0:
            print 'RuntimeError?'
            exit(-1)
        end_time = time.time()
        return end_time - start_time

    def get_execute_command_line(self):
        raise NotImplementedError


class SolutionC(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return subprocess.call([
            'gcc',
            '-O2',
            '-o',
            'a.exe',
            '-Wno-deprecated',
            '-Wall',
            self.source_file_name
        ]) == 0

    def get_execute_command_line(self):
        return ['./a.exe']


class SolutionCxx(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return subprocess.call([
            'g++',
            '-O2',
            '-o',
            'a.exe',
            '-Wno-deprecated',
            '-Wall',
            '-std=c++11',
            '-Wl,-stack,10485760',
            self.source_file_name
        ]) == 0

    def get_execute_command_line(self):
        return ['./a.exe']


class SolutionJava(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return subprocess.call(['javac', self.source_file_name]) == 0

    def get_execute_command_line(self):
        class_name = self.source_file_name.split('.')[0]
        return ['java', '-Xmx256m', class_name]


class SolutionIo(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return True

    def get_execute_command_line(self):
        return ['io', self.source_file_name]


class SolutionPhp(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return True

    def get_execute_command_line(self):
        return ['php', self.source_file_name]


class SolutionPython(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return True

    def get_execute_command_line(self):
        return ['python', self.source_file_name]


class SolutionPerl(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return True

    def get_execute_command_line(self):
        return ['perl', self.source_file_name]


class SolutionRuby(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return True

    def get_execute_command_line(self):
        return ['ruby', self.source_file_name]


class SolutionHaskell(Solution):
    def __init__(self, source_file_name):
        Solution.__init__(self, source_file_name)

    def compile(self):
        return subprocess.call([
            'ghc',
            '-o',
            'a.exe',
            self.source_file_name
        ]) == 0

    def get_execute_command_line(self):
        return ['./a.exe']


def main():
    print __doc__

if __name__ == '__main__':
    main()
