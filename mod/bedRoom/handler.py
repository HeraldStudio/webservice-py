#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-24 12:46:36
# @Author  : LiangJ

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from sqlalchemy.orm.exc import NoResultFound
from ..models.user_detail import UserDetail
from ..models.room_cache import RoomCache
from time import time
import tornado.web
import tornado.gen
import json, base64
from BeautifulSoup import BeautifulSoup
import urllib
from time import time, localtime, strftime
import datetime

class RoomHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def on_finish(self):
        self.db.close()
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        number = self.get_argument('number',default=None)
        retjson = {'code':200, 'content':''}
        data = {
            'Login.Token1':number,
            'Login.Token2':self.get_argument('password'),
        }

        # read from cache
        try:
            status = self.db.query(RoomCache).filter(RoomCache.cardnum == number).one()
            if status.date > int(time())-10000 and status.text != '*':
                self.write(base64.b64decode(status.text))
                self.finish()
                return
        except NoResultFound:
            status = RoomCache(cardnum = number,text = '*',date = int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                CHECK_URL,
                method='POST',
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if response.body and response.body.find('Successed')>0:
                cookie = response.headers['Set-Cookie']
                request = HTTPRequest(
                    URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                request = HTTPRequest(
                    DETAIL_URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                retjson['code']=200
                retjson['content'] = response.body
                soup = BeautifulSoup(response.body)
                table2 = soup.findAll('td')
                room = table2[2].text
                bed = table2[3].text
                retjson['code'] = 200
                retjson['content'] = {
                    'bed': bed,
                    'room': room
                }
            else:
                retjson['code'] = 408
        except Exception,e:
            retjson['code'] = 500
            with open('api_error.log','a+') as f:
                f.write(strftime('%Y%m%d %H:%M:%S in [webservice]', localtime(time()))+'\n'+str(str(e)+'\n[room]\t'+str(number)+'\nString:'+str(retjson)+'\n\n'))
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
            finally:
                self.db.remove()

        