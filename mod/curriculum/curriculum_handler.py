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
import json, base64
import re,sys,traceback
import pdb

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
        retjson = {'code':200, 'content':'','week':'','term':term}
        if not (cardnum and term):
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            try:

                try:
                    status = self.db.query(Curriculum_CookieCache).filter(Curriculum_CookieCache.cid ==  cardnum ).one()
                    if status.date > int(time())- 3600 * 12 and status.cookie != '*' and status.time < 3 :
			self.write(base64.b64decode(status.cookie))
			if status.last > int(time())-3600:
			    status.time += 1
			else:
			    status.last = int(time())
			self.db.add(status)
            		try:
                	    self.db.commit()
            		except:
                	    self.db.rollback()
            		finally:
                	    self.db.remove()
                        self.db.close()
                        self.finish()
                        return
                except NoResultFound:
                    status = Curriculum_CookieCache(cid =cardnum, cookie='*', date=int(time()))
                    self.db.add(status)
                    try:
                        self.db.commit()
                    except:
                        self.db.rollback()

                params = urllib.urlencode(
                    {'queryStudentId': cardnum,
                     'queryAcademicYear': term}
                )
                client = AsyncHTTPClient()
                request = HTTPRequest(
                    CURR_URL, 
                    body=params, 
                    method='POST',
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
                        retjson['sidebar'] = self.sidebarparser(body)
                if date != "-1":
                    url = "http://58.192.114.179/classroom/common/getdateofweek?date="+date
                    client = AsyncHTTPClient()
                    request = HTTPRequest(
                        url = url, 
                        method = "GET",
                        request_timeout=TIME_OUT
                    )
                    response = yield tornado.gen.Task(client.fetch, request)
                    retjson['week'] = json.loads(response.body)
                url = "http://58.192.114.179/classroom/common/gettermlistex"
                client = AsyncHTTPClient()
                request = HTTPRequest(
                    url = url, 
                    method = "GET",
                    request_timeout=TIME_OUT
                )
                response = yield tornado.gen.Task(client.fetch, request)
                content = json.loads(response.body)
                termTemp = term.split('-')
                term = "20"+termTemp[0]+"-"+"20"+termTemp[1]+"-"+termTemp[2]
		retjson['content']['startdate']={}
                for i in content:
                    if i['code'] == term:
                        retjson['content']['startdate']['month'] = i['startDate']['month']
                        retjson['content']['startdate']['day'] = i['startDate']['date']       
            except Exception,e:
                retjson['code'] = 500
                retjson['content'] = str(e)

        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.cookie= base64.b64encode(ret)
	    status.last = int(time())
	    status.time = 0
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            finally:
                self.db.remove()
        self.db.close()



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

    def sidebarparser(self, html):
        soup = BeautifulSoup(html)
        items = soup.findAll('td', height='34', width='35%')[:-1]
        items = [item for item in items if item.text != u'&nbsp;']
        sidebar = []
        for item in items:
            sidebar.append(
                {'course': item.text,
                 'lecturer': self.next_n_sibling(item, 2).text[6:],
                 'credit': self.next_n_sibling(item, 4).text[6:],
                 'week': self.next_n_sibling(item, 6).text[6:]
                 })
        return sidebar

    def next_n_sibling(self, item, n):
        for i in xrange(n):
            item = item.nextSibling
        return item
