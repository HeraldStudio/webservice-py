# -*- coding: utf-8 -*-
# @Date    : 2015-03-19 16 16:34:57
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient
from ..models.user_detail import UserDetail
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib, json
from ..auth.handler import authApi

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
            response = authApi(cardnum,self.get_argument('password'))
            if response['code'] == 200:
                cookie = response['content']
                request = HTTPRequest(
                    URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                tempCookie = response.headers['Set-Cookie'].split(';')
                cookie = cookie.split(";")[0]+";"+tempCookie[0]+";"+tempCookie[1].split(',')[1]
                request = HTTPRequest(
                    DETAIL_URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td')
                schoolnum = self.get_schoolnum(cardnum)
                # schoolnum = td[11].text
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
        except Exception,e:
            pass
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

    def get_schoolnum(self,cardnum):
        try:
            CURR_URL = 'http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action'
            term = "16-17-1"
            params = urllib.urlencode({
                'queryStudentId': cardnum,
                'queryAcademicYear': term})
            client = HTTPClient()
            request = HTTPRequest(
                CURR_URL,
                method='POST',
                body=params,
                request_timeout=TIME_OUT)
            response = client.fetch(request)
            body = response.body
            if not body:
                return "-1"
            else:
                soup = BeautifulSoup(body)
                number = soup.findAll('td', align='left')[2].text[3:]
                return number
        except Exception,e:
            return "-1"
