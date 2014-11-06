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
                    'index': b.h3.contents[2].strip(),
                    'name': name[name.find('.')+1:],
                    'all': b.p.span.contents[0][5:-1],
                    'left': b.p.span.contents[2].split('：')[1],
                    'publish': b.p.contents[4].strip(),
                    'author': b.p.contents[2].strip()
                    })
            self.write(json.dumps(books, ensure_ascii=False, indent=2))
        except:
            self.write('error')
        self.finish()

