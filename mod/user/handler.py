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
                    DETAIL_URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                table1 = soup.findAll('table',{'class':'pa-main-table'})[0].findChildren()
                schoolnum = table1[5].text.replace('&nbsp;', '')
                name = table1[8].text.replace('&nbsp;', '')
                sex = table1[15].text.replace('&nbsp;', '')
                nation = table1[18].text.replace('&nbsp;', '')

                table2 = soup.findAll('table',{'class':'portlet-table'})[0].findChildren()
                room = table2[-5].text
                bed = table2[-4].text + '-' + table2[-3].text

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
