# -*- coding: utf-8 -*-
# modified from old listhandler.py 
# by yml_bright@163.com

from config import *
import re
import json
import urllib
import base64
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web, tornado.gen
from bs4 import BeautifulSoup
from ..models.library_auth_cache import LibraryAuthCache
from sqlalchemy.orm.exc import NoResultFound
from time import time

class LibListHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        self.write('herald web service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        cardnum = self.get_argument('cardnum')
        retjson = {}
        if not cardnum:
            retjson['code'] = 400
            retjson['content'] = u'parameters lack'
        else:
            try:
                status = self.db.query(LibraryAuthCache).filter(LibraryAuthCache.cardnum == cardnum).one()
                if (status.cookie != '*'):
                    cookie = status.cookie
                else:
                    retjson['code'] = 401
                    retjson['content'] = u'auth error'
            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = u'error'
            try:
                client = AsyncHTTPClient()
                request = HTTPRequest(
                    LOGIN_URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body, 'html.parser')
                name = soup.findAll('font')[0].text
                if name:
                    request = HTTPRequest(
                        LIST_URL,
                        method='GET',
                        headers={'Cookie': cookie},
                        request_timeout=TIME_OUT
                        )
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body, 'html.parser')
                    td = soup.findAll('td', {'class': 'whitetext'})
                    ret = []
                    for i in range(0, len(td), 8):
                        info = td[i+1].text.split('/')
                        book = {
                            'barcode': td[i].text,
                            'title': info[0],
                            'author': info[1],
                            'render_date': td[i+2].text,
                            'due_date': td[i+3].text,
                            'renew_time': td[i+4].text,
                            'place': td[i+5].text
                        }
                        ret.append(book)
                    retjson['content'] = ret
                else:
                    retjson['code'] = 401
                    retjson['content'] = u'auth error'
            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = u'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()