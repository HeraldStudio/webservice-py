# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 17:34:57
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json, re

class LibListHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        data = {
            'number':self.get_argument('cardnum'),
            'passwd':self.get_argument('password'),
            'select': 'bar_no'
        }
        try:
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
                self.write(json.dumps(ret, ensure_ascii=False, indent=2))
            else:
                self.write('wrong card number or password')
        except:
            self.write('error')
        self.finish()

    def entity_parser(self, string):
        x = re.findall('&#x(.{4});', string)
        s = ''
        for c in x:
            s += unichr(int(c,16))
        return s


