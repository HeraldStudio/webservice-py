#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.card_cache import CardCache
from sqlalchemy.orm.exc import NoResultFound
from time import time
import tornado.web
import tornado.gen
import urllib, re
import json, base64
import datetime

class CARDHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        timedelta = int(self.get_argument('timedelta', default=0))
        cardnum = self.get_argument('cardnum')
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}
        isCached = True

        # read from cache
        try:
            status = self.db.query(CardCache).filter( CardCache.cardnum ==  cardnum ).one()
            if timedelta == 0 and status.date == int(time())/1000:
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return
        except NoResultFound:
            isCached = False

        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                CHECK_URL,
                method='POST',
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if response.body and response.body.find('Successed')>0:
                cookie = response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    LOGIN_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)

                cookie += ';' + response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    USERID_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td',{"class": "neiwen"})
                userid = td[3].text
                cardState = td[42].text
                cardLetf = td[46].text.encode('utf-8').split('元')[0]

                if timedelta == 0:
                    retjson['content'] = {'state':cardState, 'left':cardLetf}
                    retjson = json.dumps(retjson, ensure_ascii=False, indent=2)
                    self.write(retjson)
                    self.finish()

                    # refresh cache
                    if isCached:
                        status.date = int(time())/1000
                        status.text = base64.b64encode(retjson)
                        self.db.add(status)
                    else:
                        status = CardCache(cardnum=cardnum, text=base64.b64encode(retjson), date=int(time())/1000)
                        self.db.add(status)
                    self.db.commit()
                    self.db.close()
                    return

                request = HTTPRequest(
                    INIT_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action']

                now = datetime.datetime.now()
                delta = datetime.timedelta(timedelta)
                page = 1
                data = {
                    'account':userid,
                    'inputObject':'all',
                    'inputStartDate':(now - delta).strftime('%Y%m%d'),
                    'inputEndDate':now.strftime('%Y%m%d'),
                    'pageNum':page
                }
                request = HTTPRequest(
                    INDEX_URL+__continue,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action']
                request = HTTPRequest(
                    INDEX_URL+__continue,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'name':'form1'})[0]['action']
                request = HTTPRequest(
                    INIT_URL+__continue,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)

                detial = []
                count = 0
                while 1:
                    tr = soup.findAll('tr',{"class": re.compile("listbg")})
                    if not tr:
                        break
                    for td in tr:
                        td = td.findChildren()
                        tmp = {}
                        tmp['date'] = td[0].text
                        tmp['type'] = td[3].text
                        tmp['system'] = td[4].text
                        tmp['price'] = td[5].text
                        tmp['left'] = td[6].text
                        detial.append(tmp)
                    page += 1
                    data['pageNum'] = page
                    request = HTTPRequest(
                        DATA_URL,
                        method='POST',
                        headers={'Cookie':cookie},
                        body=urllib.urlencode(data),
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                retjson['content'] = {'state':cardState, 'left':cardLetf, 'detial':detial}
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()