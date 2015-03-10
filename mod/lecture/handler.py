#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.lecture_cache import LectureCache
from sqlalchemy.orm.exc import NoResultFound
from time import time
import tornado.web
import tornado.gen
import json, base64
import urllib, re

class LectureHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum')
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}
        isCached = True

        # read from cache
        try:
            status = self.db.query(LectureCache).filter( LectureCache.cardnum ==  cardnum ).one()
            if status.date == int(time())/1000:
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
                client = AsyncHTTPClient()
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
                userid = soup.findAll(attrs={"align": "left"})[2].text

                page = 1
                data = {
                    'account':userid,
                    'startDate':'',
                    'endDate':'',
                    'pageno':0
                }
                fliter = ['九龙湖', '手持考', '行政楼', '网络中', '机电大', '校医院', '研究生']
                lecture = []
                count = 0
                while 1:
                    data['pageno'] = page
                    request = HTTPRequest(
                        DATA_URL,
                        method='POST', 
                        body=urllib.urlencode(data),
                        headers={'Cookie':cookie},
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                    tr = soup.findAll('tr',{"class": re.compile("listbg")})
                    if not tr:
                        break
                    for td in tr:
                        td = td.findChildren()
                        if not td[4].text[:3].encode('utf-8') in fliter:
                            tmp = {}
                            datecheck = td[0].text.split(' ')[0]
                            if count>0 and datecheck == lecture[count-1]['date'].split(' ')[0]:
                                continue
                            tmp['date'] = td[0].text
                            tmp['place'] = td[4].text
                            lecture.append(tmp)
                            count += 1
                    page += 1
                retjson['content'] = {'count':count, 'detial':lecture}
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        retjson = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(retjson)
        self.finish()

        # refresh cache
        if isCached:
            status.date = int(time())/1000
            status.text = base64.b64encode(retjson)
            self.db.add(status)
        else:
            status = LectureCache(cardnum=cardnum, text=base64.b64encode(retjson), date=int(time())/1000)
            self.db.add(status)
        try:
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.db.remove()
        self.db.close()
