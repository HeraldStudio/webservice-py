# -*- coding: utf-8 -*-
# @Date    : 2014-06-26 13:57:44
# @Author  : xindervella@gamil.com
from BeautifulSoup import BeautifulSoup
from config import CURR_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from collections import OrderedDict
import tornado.web
import tornado.gen
import urllib
import json
import re


class CurriculumHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        term = self.get_argument('term', default=None)
        if not (cardnum or term):
            self.write('params lack')
        else:
            params = urllib.urlencode(
                {'queryStudentId': cardnum,
                 'queryAcademicYear': term}
            )
            client = AsyncHTTPClient()
            request = HTTPRequest(CURR_URL, body=params, method='POST',
                                  request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            body = response.body

            if not body:
                self.write('time out')
            else:
                pat = re.compile(ur'没有找到该学生信息', re.U)
                match = pat.search(body)
                if match:
                    self.write('card number not exist')
                else:
                    self.write(self.parser(body))
        self.finish()

    def parser(self, html):
        soup = BeautifulSoup(html)
        table = soup.findAll('td', rowspan='5')
        table += soup.findAll('td', rowspan='2')
        self.course_split(table[1])
        curriculum = OrderedDict()
        curriculum['Mon.'] = self.course_split(table[1]) + \
            self.course_split(table[7]) + \
            self.course_split(table[13])
        curriculum['Tues.'] = self.course_split(table[2]) + \
            self.course_split(table[8]) + \
            self.course_split(table[14])
        curriculum['Wed.'] = self.course_split(table[3]) + \
            self.course_split(table[9]) + \
            self.course_split(table[15])
        curriculum['Thur.'] = self.course_split(table[4]) + \
            self.course_split(table[10]) + \
            self.course_split(table[16])
        curriculum['Fri.'] = self.course_split(table[5]) + \
            self.course_split(table[11]) + \
            self.course_split(table[17])
        curriculum['Sat.'] = self.course_split(table[19])
        curriculum['Sun.'] = self.course_split(table[21])

        return json.dumps(curriculum, ensure_ascii=False, indent=2)

    def course_split(self, table):
        br = BeautifulSoup('<br/>')
        course = []
        for item in table.contents[:-1]:
            course.append(item)
            try:
                if course[-1] == course[-2] == br.br:
                    course.insert(-1, u'')
            except IndexError:
                pass  # 忽略第一次迭代时 course 越界
        course = [item for item in course if item != br.br]

        curriculum = []
        for i in xrange(0, len(course), 3):
            curriculum.append(
                [course[i], course[i + 1], course[i + 2]]
            )
        return curriculum
