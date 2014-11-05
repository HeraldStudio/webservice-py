# -*- coding: utf-8 -*-
# @Date    : 2014-11-03 15:34:57
# @Author  : yml_bright@163.com

from config import CHECK_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import urllib

class AuthHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        data = {
            'Login.Token1':self.get_argument('cardnum'),
            'Login.Token2':self.get_argument('password'),
        }
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                CHECK_URL,
                method='POST',
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if response.body and response.body.find('Successed')>0:
                self.write(response.headers['Set-Cookie'])
                self.finish()
                return
        except:
            pass
        raise tornado.web.HTTPError(401)
