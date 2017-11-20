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

class LibAuthHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):

        cardnum = self.get_argument('cardnum', default=None)
        if not cardnum:
            # 因为需要返回图片，所以一卡通为空不做提示
            raise Exception
        try:
            client = HTTPClient()
            response = client.fetch(GET_CAPTCHA)
            cookie = response.headers['Set-Cookie'].split(';')[0]
            try:
                status = self.db.query(LibraryAuthCache).filter(LibraryAuthCache.cardnum == cardnum).one()
                status.cookie = cookie
                print status.cookie
            except NoResultFound:
                status = LibraryAuthCache(cardnum=cardnum, cookie=cookie, captcha='*', date=int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except Exception:
                self.db.rollback()
            self.set_header('Content-type', 'image/png')
            self.write(response.body)   # return captcha to client
        except Exception as e:
            self.write('error')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        captcha = self.get_argument('captcha', default=None)
        retjson = {'code': 200, 'content': ''}
        status = None
        if not (cardnum and password and captcha):
            retjson['code'] = 400
            retjson['content'] = 'parameters lack'
        else:
            # 直接从数据库读取cookie，不做try的尝试
            status = self.db.query(LibraryAuthCache).filter(LibraryAuthCache.cardnum == cardnum).one()
            cookie = status.cookie
            try:
                form_data = {
                    'number': cardnum,
                    'passwd': password,
                    'captcha': captcha,
                    'select': 'cert_no'
                }
                client = AsyncHTTPClient()
                request = HTTPRequest(
                    LOGIN_URL,
                    method='POST',
                    headers={'Cookie': cookie},
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
