# -*- coding: utf-8 -*-
from config import LOGIN_URL, CHOISE_URL, DETIAL_URL, WEB_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json


class NICHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        # type 查询类型(a, b, web)
        data = {
            'password': self.get_argument('cardnum', default=None),
            'username': self.get_argument('password', default=None)
        }
        client = AsyncHTTPClient()
        request = HTTPRequest(
            LOGIN_URL,
            method='GET',
            request_timeout=TIME_OUT)
        response = yield tornado.gen.Task(client.fetch, request)
        try:
            cookie = response.headers['Set-Cookie'].split(';')[0]
        except:
            self.write('server error')
            return
        request = HTTPRequest(
            LOGIN_URL, body=urllib.urlencode(data),
            method='POST',
            request_timeout=TIME_OUT,
            headers={'Cookie': cookie})
        response = yield tornado.gen.Task(client.fetch, request)

        if int(response.headers['Content-Length']) == 7783:
            self.write('wrong card number or password')
        else:
            data = {
                'item': self.get_argument('type', default=None),
                'operation': 'status',
                'web_sel': '1'
            }
            status = True
            request = HTTPRequest(
                CHOISE_URL, body=urllib.urlencode(data), method='POST',
                request_timeout=TIME_OUT,
                headers={'Cookie': cookie})
            response = yield tornado.gen.Task(client.fetch, request)
            if data['item'] == "web":
                request = HTTPRequest(
                    WEB_URL, method='GET', request_timeout=TIME_OUT,
                    headers={'Cookie': cookie})
                response = yield tornado.gen.Task(client.fetch, request)
                body = response.body
                self.write(body)
                soup = BeautifulSoup(body)
                try:
                    table = soup.findAll(
                        "td", {"width": "50%", "align": "center",
                               "bgcolor": "#FFFFFF"})
                    items = {'used': table[2].getString().replace(
                        '\t', '').replace('\n', ''),
                        'status': table[0].getString() +
                        '-' + table[1].getString(), 'left': ''}
                except:
                    status = False
            else:
                request = HTTPRequest(
                    DETIAL_URL, method='GET', request_timeout=TIME_OUT,
                    headers={'Cookie': cookie})
                response = yield tornado.gen.Task(client.fetch, request)
                body = response.body
                soup = BeautifulSoup(body)
                try:
                    table = soup.findAll(
                        "td", {"width": "60%", "align": "right"})
                    items = {
                        'used': table[0].getString(),
                        'left': table[1].getString()}
                    table = soup.findAll(
                        "td", {"width": "50%", "align": "center"})
                    items['status'] = table[1].getString()
                except:
                    status = False
            if status:
                self.write(json.dumps(items, ensure_ascii=False, indent=2))
            else:
                self.write('disabled')
        self.finish()
