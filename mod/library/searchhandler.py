#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-06 10:36:01
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json, re

class LibSearchHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        data = {
            's2_text': self.get_argument('book'),
            's2_type': 'title',
            'search_bar': 'new',
            'title': self.get_argument('book'),
            'doctype': 'ALL',
            'match_flag': 'forward',
            'showmod': 'json',
            'dept': 'ALL'
        }
        retjson = {'code':200, 'content':''}
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                SEARCH_URL,
                method='POST',
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            soup = BeautifulSoup(response.body)
            li = soup.findAll('li', {'class': 'book_list_info'})
            books = [] 
            for b in li:
                name = b.a.text
                books.append({
                    'type': b.span.text,
                    'index': self.entity_parser(b.h3.contents[2].strip()),
                    'name': self.entity_parser(name[name.find('.')+1:]),
                    'all': b.p.span.contents[0][5:-1],
                    'left': b.p.span.contents[2].split('：')[1],
                    'publish': self.entity_parser(b.p.contents[4].strip()),
                    'author': self.entity_parser(b.p.contents[2].strip())
                    })
            retjson['content'] = books
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

    def entity_parser(self, string):
        x = re.findall('&#x(.{4});', string)
        s = ''
        for c in x:
            s += unichr(int(c,16))
        return s