# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : yml_bright@163.com
from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.pe_models import PEUser
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib
import random
import json,socket

class PEHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        state = 'success'
        cardnum = self.get_argument('cardnum', default=None)
        pwd = self.get_argument('pwd', default=cardnum)
        retjson = {'code':200, 'content':''}
        # pwd 缺省为 cardnum

        if not cardnum:
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            result = self.get_pe_count(cardnum)
            if result == -1:
                state = 'time_out'
                try:
                    # 超时取出缓存
                    user = self.db.query(PEUser).filter(
                        PEUser.cardnum == int(cardnum)).one()
                    retjson['content'] = user.count
                except NoResultFound:
                    retjson['code'] = 408
                    retjson['content'] = 'time out'
            else:
                retjson['content'] = str(result)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

        if state == 'success':
            # 更新缓存
            try:
                user = self.db.query(PEUser).filter(
                    PEUser.cardnum == int(cardnum)).one()
                user.count = int(result)
            except NoResultFound:
                user = PEUser(cardnum=int(cardnum), count=count)
                self.db.add(user)
            finally:
                self.db.commit()
        self.db.close()

    def get_pe_count(self,cardnum):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((API_SERVER_HOST, API_SERVER_PORT))
            s.send('\x00'+A+'\x09'+cardnum+'\x00')
            recv = s.recv(1024).split(',')
            return int(recv[0])+int(recv[1])
        except socket.timeout:
            return -1