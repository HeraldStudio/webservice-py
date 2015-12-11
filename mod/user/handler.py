# -*- coding: utf-8 -*-
# @Date    : 2015-03-19 16 16:34:57
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from ..models.user_detail import UserDetail
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib, json

class UserHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('number')
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':500, 'content':''}

        try:
            user = self.db.query(UserDetail).filter(
                UserDetail.cardnum == cardnum).one()
            retjson['code'] = 200
            retjson['content'] = {
                'cardnum': user.cardnum,
                'schoolnum': user.schoolnum,
                'name': user.name,
                'sex': user.sex,
            }
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()
            return
        except NoResultFound:
            pass

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
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td')
                schoolnum = td[11].text
                name = td[2].text
                nation = td[4].text
                sex = td[5].text
                room = ''
                bed = ''

                user = UserDetail(
                    cardnum = cardnum,
                    schoolnum = schoolnum,
                    name = name,
                    sex = sex,
                    nation = nation,
                    room = room,
                    bed = bed
                    )
                self.db.add(user)
                self.db.commit()

                retjson['code'] = 200
                retjson['content'] = {
                    'cardnum': user.cardnum,
                    'schoolnum': user.schoolnum,
                    'name': user.name,
                    'sex': user.sex,
                }
        except:
            pass
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
