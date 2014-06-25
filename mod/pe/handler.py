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


class PEHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        try:
            self.cardnum = self.get_argument('cardnum')
        except tornado.web.MissingArgumentError:
            self.cardnum = None
        try:
            self.pwd = self.get_argument('pwd')
        except tornado.web.MissingArgumentError:
            self.pwd = None

        if not self.pwd:
            if self.cardnum:
                self.pwd = self.cardnum  # pwd 缺省为 cardnum
            else:
                self.write('empty card number')

        data = {
            'xh': str(self.cardnum),
            'mm': str(self.pwd),
            'method': 'login'
        }

        if self.cardnum and self.pwd:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                PE_LOGIN_URL, body=urllib.urlencode(data),
                method='POST',
                request_timeout=CONNECT_TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            self.headers = response.headers
            if self.headers == {}:
                self.state = 'time out'
                try:
                    # 超时取出缓存
                    self.user = self.db.query(PEUser).filter(
                        PEUser.cardnum == str(self.cardnum)).one()
                    self.write(self.user.count)
                except NoResultFound:
                    self.write(self.state)

            else:
                # self.headers['Content-Length'] # 登陆成功 524 失败 1608
                if int(self.headers['Content-Length']) > 800:
                    self.state = 'wrong card number or password'
                    self.write(self.state)
                else:
                    self.state = 'success'

            if self.state == 'success':
                self.cookie = self.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    PE_PC_URL, method='GET', request_timeout=CONNECT_TIME_OUT,
                    headers={'Cookie': self.cookie})
                response = yield tornado.gen.Task(client.fetch, request)
                self.body = response.body
                if not self.body:
                    self.state = 'time out'
                    try:
                        # 超时取出缓存
                        self.user = self.db.query(PEUser).filter(
                            PEUser.cardnum == str(self.cardnum)).one()
                        self.write(self.user.count)
                    except NoResultFound:
                        self.write(self.state)
                else:
                    self.soup = BeautifulSoup(self.body)
                    self.table = self.soup.findAll(
                        "td", {"class": "Content_Form"})
                    self.count = self.table[7].text
                    self.write(self.count)
        self.finish()

        if self.state == 'success':
            # 更新缓存
            try:
                self.user = self.db.query(PEUser).filter(
                    PEUser.cardnum == str(self.cardnum)).one()
                self.user.count = self.count
            except NoResultFound:
                self.user = PEUser(cardnum=str(self.cardnum), count=self.count)
                self.db.add(self.user)
            finally:
                self.db.commit()
