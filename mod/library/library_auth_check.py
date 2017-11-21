# -*- coding: utf-8 -*-

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

class LibAuthCheckHandler(tornado.web.RequestHandler):

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
        retjson = {'code': 200, 'content': ''}
        if not cardnum:
            retjson['code'] = 400
            retjson['content'] = u'parameters lack'
        else:
            try:
                status = self.db.query(LibraryAuthCache).filter(LibraryAuthCache.cardnum == cardnum).one()
                cookie = status.cookie
            except NoResultFound:
                cookie = '*'
                retjson['code'] = 401
                retjson['content'] = u'auth error'
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
                    retjson['content'] = u'auth success'
                    retjson['code'] = 200
                else:
                    retjson['code'] = 401
                    retjson['content'] = u'auth error'
            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = u'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()
