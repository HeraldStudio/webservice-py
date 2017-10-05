# -*- coding: utf-8 -*-
# modified from old renewhandler.py 
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

class LibRenewHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        cardnum = self.get_argument('cardnum')
        try:
            status = self.db.query(LibraryAuthCache).filter(cardnum == cardnum).one()
            cookie = status.cookie
        except Exception as e:
            self.write('error')
        try:
            client = HTTPClient()
            request = HTTPRequest(
                GET_CAPTCHA,
                method='GET',
                headers={'Cookie': cookie},
                request_timeout=TIME_OUT
                )
            response = client.fetch(request)
            self.set_header('Content-Type', 'image/png')
            self.write(response.body)
        except Exception as e:
            self.write('error')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum')
        captcha = self.get_argument('captcha')
        barcode = self.get_argument('barcode')
        retjson = {'code': 200, 'content': u''}
        if (not cardnum or not barcode):
            retjson['code'] = 400
            retjson['content'] = u'parameter lack'
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
                    flag = False
                    request = HTTPRequest(
                        LIST_URL,
                        method = 'GET',
                        headers={'Cookie': cookie},
                        request_timeout = TIME_OUT
                        )
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body, 'html.parser')
                    td = soup.findAll('td', {'class': 'whitetext'})
                    for i in range(0, len(td), 8):
                        if (barcode == td[i].text):
                            checkcode = td[i+7].input['onclick'].split('\'')[3]
                            request = HTTPRequest(
                                RENEW_URL%(barcode, checkcode, captcha, int(time()*1000)),
                                method='GET',
                                headers={'Cookie': cookie},
                                request_timeout=TIME_OUT
                                )
                            response = yield tornado.gen.Task(client.fetch, request)
                            if (response.body == 'invalid call'):
                                flag = False
                            else:
                                flag = True
                    if flag:
                        if u'wrong' in response.body:
                            retjson['code'] = 200
                            retjson['content'] = u'wrong captcha'
                        else:
                            soup = BeautifulSoup(response.body, 'html.parser')
                            retjson['code'] = 200
                            retjson['content'] = soup.findAll('font')[0].text
                    else:
                        retjson['code'] = 400
                        retjson['content'] = u'fail'
                else:
                    retjson['code'] = 401
                    retjson['content'] = u'auth error'
            except Exception as e:
                print e
                retjson['code'] = 500
                retjson['content'] = u'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()