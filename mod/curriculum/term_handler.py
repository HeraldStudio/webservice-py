# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 20:53:54
# @Author  : xindervella@gamil.com
from BeautifulSoup import BeautifulSoup
from config import TERM_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import json


class TermHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        client = AsyncHTTPClient()
        request = HTTPRequest(TERM_URL, request_timeout=TIME_OUT)
        response = yield tornado.gen.Task(client.fetch, request)
        body = response.body
        if not body:
            self.write('time out')
        else:
            soup = BeautifulSoup(body)
            option = soup.findAll('option')
            terms = [term.text for term in option]
            self.write(json.dumps(terms, ensure_ascii=False, indent=2))
        self.finish()
