# -*- coding: utf-8 -*-
# @Date    : 2014-06-26 13:57:44
# @Author  : xindervella@gamil.com yml_bright@163.com
from BeautifulSoup import BeautifulSoup
from config import CURR_URL, TIME_OUT,TERM_URL,JWC_URL
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from collections import OrderedDict
from ..models.curriculum_cookie import Curriculum_CookieCache
from sqlalchemy.orm.exc import NoResultFound
from time import time
import tornado.web
import tornado.gen
import urllib
import json
import re


class CurriculumHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')
    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        term = self.get_argument('term', default=None)
        date = self.get_argument('date',default="-1")
        retjson = {'code':200, 'content':'','week':''}
        if not (cardnum and term):
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            params = urllib.urlencode(
                {'queryStudentId': cardnum,
                 'queryAcademicYear': term}
            )
            client = AsyncHTTPClient()
            header = { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host':'xk.urp.seu.edu.cn',
                'Connection':'keep-alive',
                'Referer':'http://jwc.seu.edu.cn/',
                'Upgrade-Insecure-Requests':'1'
            }
            cookie = ""
            state = 0
            try:
                dbcookie = self.db.query(Curriculum_CookieCache).one()
                if(int(time())-dbcookie.date)>600:
                    state = 1
                header['Cookie'] = dbcookie.cookie
            except NoResultFound:
                dbcookie = Curriculum_CookieCache(cookie="",date=int(time()))
                state = 1
            if state==1:
                request = HTTPRequest(
                    JWC_URL,
                    method='GET',
                    request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                request = HTTPRequest(
                    TERM_URL,
                    method='GET',
                    headers=header,
                    request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                if "Set-Cookie" in response.headers.keys():
                    cookie = response.headers['Set-Cookie']
                    header['Cookie'] = cookie
                    dbcookie.cookie = cookie
                    dbcookie.date = int(time())


            request = HTTPRequest(
                CURR_URL, 
                body=params, 
                method='POST',
                headers=header,
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            body = response.body
            if not body:
                retjson['code'] = 408
                retjson['content'] = 'time out'
            else:
                pat = re.compile(ur'没有找到该学生信息', re.U)
                match = pat.search(body)
                if match:
                    retjson['code'] = 401
                    retjson['content'] = 'card number not exist'
                else:
                    retjson['content'] = self.parser(body)
        if date != "-1":
            try:
                url = "http://58.192.114.179/classroom/common/getdateofweek?date="+date
                client = AsyncHTTPClient()
                request = HTTPRequest(
                url = url, 
                method = "GET",
                request_timeout=TIME_OUT
                )
                response = yield tornado.gen.Task(client.fetch, request)
                retjson['week'] = json.loads(response.body)
            except Exception,e:
                retjson['code'] = 500
                retjson['week'] = u'系统错误'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

        if state==1:
            try:
                self.db.add(dbcookie)
                self.db.commit()
            except:
                self.db.rollback()

    def parser(self, html):
        soup = BeautifulSoup(html)
        table = soup.findAll('td', rowspan='5')
        table += soup.findAll('td', rowspan='2')
        self.course_split(table[1])
        curriculum = OrderedDict()
        curriculum['Mon'] = self.course_split(table[1]) + \
            self.course_split(table[7]) + \
            self.course_split(table[13])
        curriculum['Tue'] = self.course_split(table[2]) + \
            self.course_split(table[8]) + \
            self.course_split(table[14])
        curriculum['Wed'] = self.course_split(table[3]) + \
            self.course_split(table[9]) + \
            self.course_split(table[15])
        curriculum['Thu'] = self.course_split(table[4]) + \
            self.course_split(table[10]) + \
            self.course_split(table[16])
        curriculum['Fri'] = self.course_split(table[5]) + \
            self.course_split(table[11]) + \
            self.course_split(table[17])
        curriculum['Sat'] = self.course_split(table[19])
        curriculum['Sun'] = self.course_split(table[21])

        return curriculum

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
