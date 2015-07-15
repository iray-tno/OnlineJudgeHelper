#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
class OnlineJudge
"""

import cookielib
import shutil
import subprocess
import os
import urllib2

import solution
import validator


class OnlineJudge(object):
    def __init__(self, options, problem_id):
        self.options = options
        self.problem_id = problem_id
        if options.titech_pubnet:
            self.proxies = {'http': 'http://proxy.noc.titech.ac.jp:3128'}
        else:
            self.proxies = None
        self.opener = None

    def get_url(self):
        raise NotImplementedError

    def get_input_file_name(self, index):
        return self.problem_id + '.' + str(index) + '.in.txt'

    def get_output_file_name(self, index):
        return self.problem_id + '.' + str(index) + '.out.txt'

    def get_source_file_name(self):
        if self.options.source_file_name:
            return self.options.source_file_name
        else:
            return self.problem_id + '.cpp'

    def format_pre(self, s):
        s = s.replace('<br />', '\n')
        s = s.replace('&lt;', '<')
        s = s.replace('&gt;', '>')
        s = s.replace('&quot;', '"')
        s = s.replace('\r', '')
        if not s.endswith('\n'):
            s += '\n'
        while s.endswith('\n\n'):
            s = s[0:len(s) - 1]
        while s.startswith('\n'):
            s = s[1:]
        return s

    def download_html(self):
        url = self.get_url()
        return self.get_opener().open(url).read()

    def download(self):
        raise NotImplementedError

    def get_opener(self):
        if self.opener is None:
            cj = cookielib.CookieJar()
            cjhdr = urllib2.HTTPCookieProcessor(cj)
            if self.proxies is None:
                self.opener = urllib2.build_opener(cjhdr)
            else:
                self.opener = urllib2.build_opener(
                    cjhdr,
                    urllib2.ProxyHandler(self.proxies)
                )
        return self.opener

    def get_solution(self):
        source_file_name = self.get_source_file_name()
        ext = os.path.splitext(source_file_name)[1]
        if ext == '.c':
            return solution.SolutionC(source_file_name)
        elif ext == '.cpp' or ext == '.cc':
            return solution.SolutionCxx(source_file_name)
        elif ext == '.java':
            return solution.SolutionJava(source_file_name)
        elif ext == '.io':
            return solution.SolutionIo(source_file_name)
        elif ext == '.php':
            return solution.SolutionPhp(source_file_name)
        elif ext == '.py':
            return solution.SolutionPython(source_file_name)
        elif ext == '.pl':
            return solution.SolutionPerl(source_file_name)
        elif ext == '.rb':
            return solution.SolutionRuby(source_file_name)
        elif ext == '.hs':
            return solution.SolutionHaskell(source_file_name)
        else:
            return solution.Solution(source_file_name)

    def get_validator(self):
        if not self.options.floating_point:
            return validator.DiffValidator()
        else:
            return validator.FloatingPointValidator(
                self.options.floating_point)

    def check(self):
        print 'compiling...'

        solution = self.get_solution()

        if not solution.compile():
            print 'CompileError'
            exit(-1)

        if not os.path.exists(self.get_input_file_name(0)) or \
                not os.path.exists(self.get_output_file_name(0)):
            print 'downloading...'
            self.download()

        max_time = 0.0

        validator = self.get_validator()

        ok = True
        no_input_files = True

        for index in range(100):
            input_file_path = self.get_input_file_name(index)
            output_file_path = self.get_output_file_name(index)

            if not os.path.exists(input_file_path):
                break

            no_input_files = False

            print '----- Case #%d -----' % index

            execution_time = solution.execute(input_file_path, 'out.txt')

            if max_time < execution_time:
                max_time = execution_time

            if os.path.exists(output_file_path):
                ok = validator.validate(output_file_path, 'out.txt') and ok
            else:
                subprocess.Popen(['cat', 'out.txt']).wait()

        if no_input_files:
            print 'No input files...'
        elif ok:
            print 'OK (max ' + str(max_time) + "s)"
        else:
            print 'WrongAnswer (max ' + str(max_time) + "s)"

    def add_test_case_template(self):
        for index in range(100):
            input_filepath = self.get_input_file_name(index)
            output_filepath = self.get_output_file_name(index)
            if os.path.isfile(input_filepath):
                continue
            open(input_filepath, 'w').close()
            open(output_filepath, 'w').close()
            print "Test case template file " + str(index) + " is created."
            return

    def submit(self):
        raise NotImplementedError

    def create_solution_template_file(self):
        try:
            src = self.get_source_file_name()
            dst = self.get_source_file_name() + ".bak"
            shutil.copyfile(src, dst)
            print 'Copied %s to %s' % (src, dst)
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
        try:
            src = 'template.cpp'
            dst = self.get_source_file_name()
            shutil.copyfile(src, dst)
            print 'Copied %s to %s' % (src, dst)
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)

    def get_language_id(self):
        source_file_name = self.get_source_file_name()
        root, ext = os.path.splitext(source_file_name)
        return self.get_language_id_from_extension()[ext.lower()]

    def get_language_id_from_extension(self):
        raise NotImplementedError


def main():
    print __doc__

if __name__ == '__main__':
    main()
