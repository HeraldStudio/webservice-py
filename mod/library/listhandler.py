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

class LibListHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        self.write('herald webservice')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        retjson = {'code': 200, 'content': ''}
        status = None
        if not (cardnum and password):
            retjson['code'] = 400
            retjson['content'] = 'parameters lack'
        else:
            # 直接从数据库读取cookie，不做try的尝试
            status = self.db.query(LibraryAuthCache).filter(LibraryAuthCache.cardnum == cardnum).one()
            cookie = status.cookie
            try:
                client = AsyncHTTPClient()
                request = HTTPRequest (
                    CAPTCHA_CRACK_URL,
                    method='GET',
                    request_timeout=TIME_OUT
                )
                response = yield tornado.gen.Task(client.fetch, request)
                crack = json.loads(response.body)
                captcha = crack['captcha']
                cookies = crack['cookies']
                form_data = {
                    'number': cardnum,
                    'passwd': password,
                    'captcha': captcha,
                    'select': 'cert_no'
                }
                request = HTTPRequest(
                    LOGIN_URL,
                    method='POST',
                    headers={'Cookie': cookies},
                    body=urllib.urlencode(form_data),
                    request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body, 'html.parser')
                name = soup.findAll('font')[0].text
                if name:
                    retjson['code'] = 200
                    retjson['content'] = 'auth success'
                else:
                    retjson['code'] = 401
                    retjson['content'] = 'auth error'
            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = 'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if (retjson['code'] == 200):
            status.password = password
            status.captcha = captcha
            status.date = int(time())
            self.db.add(status)
            try:
                self.db.commit()
            except Exception as e:
                self.db.rollback()
            finally:
                self.db.remove()
