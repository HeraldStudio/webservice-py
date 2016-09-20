# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 17:34:57
# @Author  : yml_bright@163.com
import base64
from sqlalchemy.orm.exc import NoResultFound

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json, re
from ..models.library_cache import ListLibrary
from time import time

class LibListHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    def get(self):
        self.write('Herald Web Service')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum')
        password = self.get_argument('password')
        retjson = {'code':200, 'content':''}
        if not (cardnum and password):
            retjson['code'] = 400
            retjson['content'] = 'param lack'
        else:
            #read from cache
            try:
                status = self.db.query(ListLibrary).filter(ListLibrary.cardnum == cardnum).one()
                if status.date > int(time())-43200 and status.text != '*':
                        self.write(base64.b64decode(status.text))
                        self.finish()
                        return
            except NoResultFound:
                status = ListLibrary(cardnum = cardnum,text = '*',date = int(time()))
                self.db.add(status)
                try:
                    self.db.commit()
                except:
                    self.db.rollback()

            try:
                data = {
                'number':cardnum,
                'passwd':password,
                'select': 'bar_no'
                }
                client = AsyncHTTPClient()
                request = HTTPRequest(
                    LOGIN_URL,
                    method='GET',
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                cookie = response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    LOGIN_URL,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)

                if len(response.body) < 10000:
                    data['select'] = 'cert_no'
                    request = HTTPRequest(
                        LOGIN_URL,
                        method='POST',
                        headers={'Cookie':cookie},
                        body=urllib.urlencode(data),
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)

                if len(response.body) > 10000:
                    request = HTTPRequest(
                        LIST_URL,
                        method='GET',
                        headers={'Cookie':cookie},
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'class': 'whitetext'})
                    ret = []
                    for i in range(0, len(td), 8):
                        s = td[i+1].text.split('/')
                        book = {
                            'barcode': td[i].text,
                            'title': self.entity_parser(s[0]),
                            'author': self.entity_parser(s[1]),
                            'render_date': td[i+2].text,
                            'due_date': td[i+3].text,
                            'renew_time': td[i+4].text,
                            'place': td[i+5].text,
                        }
                        ret.append(book)
                    retjson['content'] = ret
                else:
                    retjson['code'] = 401
                    retjson['content'] = 'wrong card number or password'
            except:
                retjson['code'] = 500
                retjson['content'] = 'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
            finally:
                self.db.remove()


    def entity_parser(self, string):
        x = re.findall('&#x(.{4});', string)
        s = ''
        for c in x:
            s += unichr(int(c,16))
        return s


