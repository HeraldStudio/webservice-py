# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com
from config import PE_LOGIN_URL, PE_PC_URL, CONNECT_TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.pe_models import PEUser
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib
import random


class PEHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        state = ''
        cardnum = self.get_argument('cardnum', default=None)
        pwd = self.get_argument('pwd', default=cardnum)
        # pwd 缺省为 cardnum

        if not cardnum:
            self.write('empty card number')

        else:
            data = {
                'displayName':'',
                'displayPasswd':'',
                'select':2,
                'submit.x':52+int(random.random()*10),
                'submit.y':16+int(random.random()*10),
                'userName':str(cardnum),
                'passwd':str(pwd)
            }
            client = AsyncHTTPClient()
            request = HTTPRequest(
                PE_LOGIN_URL, body=urllib.urlencode(data),
                method='POST',
                request_timeout=CONNECT_TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            headers = response.headers
            if not headers:
                state = 'time out'
                try:
                    # 超时取出缓存
                    user = self.db.query(PEUser).filter(
                        PEUser.cardnum == str(cardnum)).one()
                    self.write(user.count)
                except NoResultFound:
                    self.write(state)

            else:
                # self.headers['Content-Length'] # 登陆成功 524 失败 1608
                if int(headers['Content-Length']) > 1630:
                    state = 'wrong card number or password'
                    self.write(state)
                else:
                    state = 'success'

            if state == 'success':
                cookie = headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    PE_PC_URL, method='GET', request_timeout=CONNECT_TIME_OUT,
                    headers={'Cookie': cookie})
                response = yield tornado.gen.Task(client.fetch, request)
                body = response.body
                if not body:
                    state = 'time out'
                    try:
                        # 超时取出缓存
                        user = self.db.query(PEUser).filter(
                            PEUser.cardnum == str(cardnum)).one()
                        self.write(user.count)
                    except NoResultFound:
                        self.write(state)
                else:
                    soup = BeautifulSoup(body)
                    table = soup.findAll(
                        "td", {"bgcolor": "#FFFFFF"})
                    count = table[1].text[6:-2]
                    self.write(count)
        self.finish()

        if state == 'success':
            # 更新缓存
            try:
                user = self.db.query(PEUser).filter(
                    PEUser.cardnum == str(cardnum)).one()
                user.count = count
            except NoResultFound:
                user = PEUser(cardnum=str(cardnum), count=count)
                self.db.add(user)
            finally:
                self.db.commit()
