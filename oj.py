#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
main script
"""

import json
import re
import time
import subprocess
import urllib

from optparse import OptionParser

from onlinejudge import OnlineJudge


class POJ(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return 'http://acm.pku.edu.cn/JudgeOnline/problem?id='+self.problem_id

    def download(self):
        html = self.download_html()
        p = re.compile('<pre class="sio">(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        setting = json.load(open('setting.json'))['poj']
        postdata = dict()
        postdata['user_id1'] = setting['user_id']
        postdata['password1'] = setting['password']
        params = urllib.urlencode(postdata)
        p = opener.open('http://poj.org/login', params)
        print 'Login ... ' + str(p.getcode())

        postdata = dict()
        postdata['language'] = self.get_language_id()
        postdata['problem_id'] = self.problem_id
        postdata['source'] = open(self.get_source_file_name()).read()
        postdata['submit'] = 'Submit'
        params = urllib.urlencode(postdata)
        p = opener.open('http://poj.org/submit', params)
        print 'Submit ... ' + str(p.getcode())

        time.sleep(2.0)
        subprocess.call([setting['browser'],
                         'http://poj.org/status?problem_id=&user_id=' +
                         setting['user_id'] +
                         '&result=&language='])

    def get_language_id_from_extension(self):
        return {
            '.cpp':  '4',
            '.cc':   '4',
            '.c':    '5',
            '.java': '2'
        }


class CodeForces(OnlineJudge):
    contest_id = None

    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[1])
        self.contest_id = args[0]

    def get_input_file_name(self, index):
        return self.contest_id+self.problem_id+'.'+str(index)+'.in.txt'

    def get_output_file_name(self, index):
        return self.contest_id+self.problem_id+'.'+str(index)+'.out.txt'

    def get_url(self):
        return 'http://codeforces.com/contest/' + self.contest_id + \
            '/problem/' + self.problem_id

    def download(self):
        html = self.download_html()
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True


class MJudge(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return 'http://m-judge.maximum.vc/problem.cgi?pid=' + self.problem_id

    def download_html(self):
        opener = self.get_opener()

        setting = json.load(open('setting.json'))['m_judge']
        postdata = dict()
        postdata['user'] = setting['user_id']
        postdata['pswd'] = setting['password']
        params = urllib.urlencode(postdata)
        p = opener.open('http://m-judge.maximum.vc/login.cgi', params)

        url = self.get_url()
        p = opener.open(url)
        return p.read()

    def download(self):
        html = self.download_html()
        index = html.rfind('Sample Input')
        html = html[index:]
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        setting = json.load(open('setting.json'))['m_judge']
        postdata = dict()
        postdata['user'] = setting['user_id']
        postdata['pswd'] = setting['password']
        params = urllib.urlencode(postdata)
        p = opener.open('http://m-judge.maximum.vc/login.cgi', params)
        print 'Login ... ' + str(p.getcode())

        postdata = dict()
        postdata['m'] = '1'
        postdata['pid'] = self.problem_id
        postdata['lang'] = '1'
        postdata['code'] = open(self.get_source_file_name()).read()
        params = urllib.urlencode(postdata)
        p = opener.open('http://m-judge.maximum.vc/submit.cgi', params)
        print 'Submit ... ' + str(p.getcode())

        subprocess.call([
            setting['browser'],
            'http://m-judge.maximum.vc/result.cgi'
        ])


class AOJ(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return 'http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=' + \
            self.problem_id

    def download(self):
        html = self.download_html()
        index = html.rfind('>Sample Input</')
        html = html[index:]
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        setting = json.load(open('setting.json'))['aoj']

        postdata = dict()
        postdata['userID'] = setting['user_id']
        postdata['password'] = setting['password']
        postdata['problemNO'] = self.problem_id
        postdata['language'] = self.get_language_id()
        postdata['sourceCode'] = open(self.get_source_file_name()).read()
        postdata['submit'] = 'Send'
        params = urllib.urlencode(postdata)
        p = opener.open('http://judge.u-aizu.ac.jp/onlinejudge/servlet/Submit',
                        params)
        print 'Submit ... ' + str(p.getcode())

        time.sleep(2.0)
        subprocess.call([
            setting['browser'],
            'http://judge.u-aizu.ac.jp/onlinejudge/status.jsp'
        ])

    def get_language_id_from_extension(self):
        return {
            '.cpp':  'C++',
            '.cc':   'C++',
            '.c':    'C',
            '.java': 'JAVA',
            '.cs':   'C#',
            '.d':    'D',
            '.rb':   'Ruby',
            '.py':   'Python',
            '.php':  'PHP'
        }


class CodeChef(OnlineJudge):
    contest_id = None

    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[1])
        self.contest_id = args[0]

    def get_input_file_name(self, index):
        return self.contest_id+'.'+self.problem_id+'.'+str(index)+'.in.txt'

    def get_output_file_name(self, index):
        return self.contest_id+'.'+self.problem_id+'.'+str(index)+'.out.txt'

    def get_url(self):
        return 'http://www.codechef.com/' + self.contest_id + \
            '/problems/' + self.problem_id

    def download(self):
        html = self.download_html()
        p = re.compile('put:</b>(.+?)<', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True


class ImoJudge(OnlineJudge):
    contest_id = None

    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[1])
        self.contest_id = args[0]

    def get_input_file_name(self, index):
        return self.contest_id+'.'+self.problem_id+'.'+str(index)+'.in.txt'

    def get_output_file_name(self, index):
        return self.contest_id+'.'+self.problem_id+'.'+str(index)+'.out.txt'

    def get_url(self):
        return 'http://judge.imoz.jp/page.php?page=view_problem&pid=%s&cid=%s'\
            % (self.problem_id, self.contest_id)

    def download(self):
        html = self.download_html()
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True


class AtCoder(OnlineJudge):
    contest_id = None

    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[1])
        self.contest_id = args[0]

    def get_url(self):
        return "http://%s.contest.atcoder.jp/tasks/%s" % \
            (self.contest_id, self.problem_id)

    def get_opener(self):
        if self.opener is None:
            opener = OnlineJudge.get_opener(self)

            setting = json.load(open('setting.json'))['atcoder']
            postdata = dict()
            postdata['name'] = setting['user_id']
            postdata['password'] = setting['password']
            postdata['submit'] = 'login'
            params = urllib.urlencode(postdata)
            url = 'https://%s.contest.atcoder.jp/login' % self.contest_id

            p = opener.open(url, params)
            print 'Login ... ' + str(p.getcode())

        return self.opener

    def download(self):
        html = self.download_html()
        if '入力例' in html:
            html = html[html.find('入力例'):]
        if 'Sample Input' in html:
            html = html[html.find('Sample Input'):]
        p = re.compile('<pre.*?>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        html = self.download_html()
        p = re.compile('"/submit\\?task_id=(.+?)"', re.M | re.S | re.I)
        result = p.findall(html)
        task_id = int(result[0])

        html = self.get_opener().open(
            'http://%s.contest.atcoder.jp/submit?task_id=%d' %
            (self.contest_id, task_id)
        ).read()

        p = re.compile(
            'name="__session" value="([0-9a-f]+?)"', re.M | re.S | re.I)
        result = p.findall(html)
        session = result[0]

        opener = self.get_opener()

        postdata = dict()
        postdata['__session'] = session
        postdata['task_id'] = task_id
        postdata['language_id_%d' % task_id] = self.get_language_id()
        postdata['source_code'] = open(self.get_source_file_name()).read()
        postdata['submit'] = 'submit'
        params = urllib.urlencode(postdata)
        p = opener.open(
            'https://%s.contest.atcoder.jp/submit?task_id=%d' %
            (self.contest_id, task_id), params)

        print 'Submit ... ' + str(p.getcode())

        time.sleep(2.0)
        setting = json.load(open('setting.json'))['atcoder']
        subprocess.call([
            setting['browser'],
            'http://%s.contest.atcoder.jp/submissions/me' % self.contest_id
        ])

    def get_language_id_from_extension(self):
        return {
            '.cpp':  '10',
            '.cc':   '10',
            '.c':    '1',
            '.java': '3',
            '.php':  '5',
            '.py':   '7',
            '.pl':   '8',
            '.rb':   '9',
            '.hs':   '11'
        }


class ZOJContest(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return 'http://acm.zju.edu.cn/onlinejudge/'\
            'showContestProblem.do?problemId=%s' % self.problem_id

    def get_opener(self):
        if self.opener is None:
            opener = OnlineJudge.get_opener(self)

            setting = json.load(open('setting.json'))['zoj']
            postdata = dict()
            postdata['handle'] = setting['user_id']
            postdata['password'] = setting['password']
            postdata['rememberMe'] = '1'
            postdata['submit'] = 'Login'
            params = urllib.urlencode(postdata)
            p = opener.open(
                'http://acm.zju.edu.cn/onlinejudge/login.do', params)
            print 'Login ... ' + str(p.getcode())
        return self.opener

    def download(self):
        # opener = self.get_opener()
        self.get_opener()

        html = self.download_html()
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        postdata = dict()
        postdata['problemId'] = self.problem_id
        postdata['languageId'] = '2'
        postdata['source'] = open(self.get_source_file_name()).read()
        postdata['submit'] = 'Submit'
        # params = urllib.urlencode(postdata)
        urllib.urlencode(postdata)
        p = opener.open('http://acm.zju.edu.cn/onlinejudge/contestSubmit.do')
        print 'Submit ... ' + str(p.getcode())

    def get_language_id_from_extension(self):
        return {
            '.cpp':  '2',
            '.cc':   '2',
            '.c':    '1',
            '.java': '4',
            '.py':   '5',
            '.perl': '6',
            '.php':  '8'
        }


class NPCA(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return 'http://judge.npca.jp/problems/view/%s' % self.problem_id

    def get_opener(self):
        if self.opener is None:
            opener = OnlineJudge.get_opener(self)

            setting = json.load(open('setting.json'))['npca']
            postdata = dict()
            postdata['_method'] = 'POST'
            postdata['data[User][username]'] = setting['user_id']
            postdata['data[User][password]'] = setting['password']
            postdata['data[User][active]'] = '1'
            postdata['submit'] = 'Login'
            params = urllib.urlencode(postdata)
            p = opener.open('http://judge.npca.jp/users/login', params)
            print 'Login ... ' + str(p.getcode())
        return self.opener

    def download(self):
        # opener = self.get_opener()
        self.get_opener()

        html = self.download_html()
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        postdata = dict()
        postdata['_method'] = 'POST'
        postdata['data[Submission][language_id]'] = self.get_language_id()
        postdata['data[Submission][source]'] = \
            open(self.get_source_file_name()).read()
        postdata['submit'] = 'Submit'
        # params = urllib.urlencode(postdata)
        urllib.urlencode(postdata)
        p = opener.open(
            'http://judge.npca.jp/submissions/submit/%s/' % self.problem_id)
        print 'Submit ... ' + str(p.getcode())

    def get_language_id_from_extension(self):
        return {
            '.cpp':  '2',
            '.cc':   '2',
            '.c':    '1',
            '.java': '7',
            '.py':   '11',
            '.perl': '9',
            '.php':  '10'
        }


class KCS(OnlineJudge):
    contest_id = None

    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[1])
        self.contest_id = args[0]

    def get_url(self):
        return "http://kcs.miz-miz.biz/contest/%s/view_problem/%s" % \
            (self.contest_id, self.problem_id)

    def get_opener(self):
        if self.opener is None:
            opener = OnlineJudge.get_opener(self)

            setting = json.load(open('setting.json'))['kcs']
            postdata = dict()
            postdata['user_id'] = setting['user_id']
            postdata['password'] = setting['password']
            postdata['submit'] = '送信'
            params = urllib.urlencode(postdata)
            p = opener.open('http://kcs.miz-miz.biz/login', params)
            print 'Login ... ' + str(p.getcode())
        return self.opener

    def download(self):
        html = self.download_html()
        if '入出力例' in html:
            html = html[html.find('入出力例'):]
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True

    def submit(self):
        opener = self.get_opener()

        postdata = dict()
        postdata['language'] = self.get_language_id()
        postdata['code'] = open(self.get_source_file_name()).read()
        postdata['submit'] = 'submit'
        params = urllib.urlencode(postdata)
        p = opener.open(
            'http://kcs.miz-miz.biz/contest/%s/submit_problem/%s' %
            (self.contest_id, self.problem_id), params)
        print 'Submit ... ' + str(p.getcode())

        time.sleep(2.0)
        setting = json.load(open('setting.json'))['kcs']
        subprocess.call([
            setting['browser'],
            'http://kcs.miz-miz.biz/contest/%s/submission_list/page=1' %
            self.contest_id])

    def get_language_id_from_extension(self):
        return {
            '.c':    'C',
            '.cc':   'C++11',
            '.cpp':  'C++11',
            '.cs':   'C#',
            '.py':   'Python',
            '.rb':   'Ruby',
            '.java': 'Java'
        }


class yukicoder(OnlineJudge):
    def __init__(self, options, args):
        OnlineJudge.__init__(self, options, args[0])

    def get_url(self):
        return "http://yukicoder.me/problems/%s" % self.problem_id

    def download(self):
        html = self.download_html()
        if 'サンプル' in html:
            html = html[html.find('サンプル'):]
        p = re.compile('<pre>(.+?)</pre>', re.M | re.S | re.I)
        result = p.findall(html)
        n = len(result) / 2
        for index in range(n):
            input_file_name = self.get_input_file_name(index)
            output_file_name = self.get_output_file_name(index)
            open(input_file_name,  'w').write(
                self.format_pre(result[index*2+0]))
            open(output_file_name, 'w').write(
                self.format_pre(result[index*2+1]))
        return True


def main():
    usage = "usage: %prog [options] ... [contest_id] problem_id"
    parser = OptionParser(usage=usage)
    # function
    parser.add_option(
        "-c",
        "--create-solution-template-file",
        action="store_true",
        dest="create_solution_template_file",
        default=False,
        help="Build and check the solution"
    )
    parser.add_option(
        "-s",
        "--submit",
        action="store_true",
        dest="submit",
        default=False,
        help="Submit the solution"
    )
    parser.add_option(
        "-a",
        "--add-test-case-template",
        action="store_true",
        dest="add_test_case",
        default=False,
        help="Add a test case template file"
    )
    parser.add_option(
        '-i',
        '--source-file-name',
        action='store',
        dest='source_file_name',
        default=None,
        help='Specify the source file name'
    )

    # switch online judge
    parser.add_option(
        "--poj",
        action="store_true",
        dest="poj",
        default=True,
        help="PKU JudgeOnline"
    )
    parser.add_option(
        "--codeforces",
        action="store_true",
        dest="codeforces",
        default=False,
        help="CodeForces"
    )
    parser.add_option(
        "--mjudge",
        action="store_true",
        dest="m_judge",
        default=False,
        help="M-Judge"
    )
    parser.add_option(
        "--aoj",
        action="store_true",
        dest="aoj",
        default=False,
        help="Aizu Online Judge"
    )
    parser.add_option(
        "--codechef",
        action="store_true",
        dest="codechef",
        default=False,
        help="CodeChef"
    )
    parser.add_option(
        "--imojudge",
        action="store_true",
        dest="imojudge",
        default=False,
        help="Imo Judge"
    )
    parser.add_option(
        "--atcoder",
        action="store_true",
        dest="atcoder",
        default=False,
        help="AtCoder"
    )
    parser.add_option(
        "--zojcontest",
        action="store_true",
        dest="zoj_contest",
        default=False,
        help="ZOJ Contest"
    )
    parser.add_option(
        "--npca",
        action="store_true",
        dest="npca",
        default=False,
        help="NPCA (Nada Personal Computer users' Association) Judge"
    )
    parser.add_option(
        "--kcs",
        action="store_true",
        dest="kcs",
        default=False,
        help="KCS (Kagamiz Contest System)"
    )
    parser.add_option(
        "--yukicoder",
        action="store_true",
        dest="yukicoder",
        default=False,
        help="yukicoder"
    )

    # misc
    parser.add_option(
        "-t",
        "--titech-pubnet",
        action="store_true",
        dest="titech_pubnet",
        default=False,
        help="Use titech pubnet proxy",
    )
    parser.add_option(
        "-e",
        action="store",
        dest="floating_point",
        default=None,
        help="Use floating point validator and set max error"
    )
    parser.add_option(
        '-d',
        '--download',
        action="store_true",
        dest='download',
        default=False,
        help="Only download the test cases"
    )

    (options, args) = parser.parse_args()

    if len(args) == 0:
        print "Select problem id."
        parser.print_help()
        return

    online_judge = None
    if options.zoj_contest:
        online_judge = ZOJContest(options, args)
    elif options.atcoder:
        online_judge = AtCoder(options, args)
    elif options.imojudge:
        online_judge = ImoJudge(options, args)
    elif options.codechef:
        online_judge = CodeChef(options, args)
    elif options.codeforces:
        online_judge = CodeForces(options, args)
    elif options.m_judge:
        online_judge = MJudge(options, args)
    elif options.aoj:
        online_judge = AOJ(options, args)
    elif options.npca:
        online_judge = NPCA(options, args)
    elif options.kcs:
        online_judge = KCS(options, args)
    elif options.yukicoder:
        online_judge = yukicoder(options, args)
    elif options.poj:
        online_judge = POJ(options, args)
    else:
        print 'Select an online judge!!!'
        parser.print_help()
        return

    if options.add_test_case:
        online_judge.add_test_case_template()
    elif options.submit:
        online_judge.submit()
    elif options.create_solution_template_file:
        online_judge.create_solution_template_file()
    elif options.download:
        online_judge.download()
    else:
        online_judge.check()

if __name__ == '__main__':
    main()
