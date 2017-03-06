# -*- coding: utf-8 -*-
# @Date    : 2015-03-19 16 16:34:57
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient
from ..models.user_detail import UserDetail
from bs4 import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib, json
from ..auth.handler import authApi
from sqlalchemy import func, or_, not_

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
        _number = self.get_argument('number')
        retjson = {'code':500, 'content':''}

        try:
            user = self.db.query(UserDetail).filter(_number == UserDetail.cardnum).one()
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
        except NoResultFound as e:
            pass


        _name, _schoolnum, _cardnum = self.get_schoolnum_name(_number)
        retjson['content']= {
            'schoolnum': _schoolnum,
            'cardnum': _cardnum,
            'name': _name
        }

        user_detail = UserDetail(schoolnum = _schoolnum,  cardnum= _cardnum, name = _name)
        self.db.add(user_detail)
        self.db.commit();

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
        return

    def get_schoolnum_name(self, number):
        try:
            CURR_URL = 'http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action'
            term = "16-17-1"
            params = urllib.urlencode({
                'queryStudentId': number,
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
                name = soup.findAll('td', align='left')[4].text[3:]
                cardnum = soup.findAll('td', align='left')[3].text[5:]
                return name, number, cardnum
        except Exception,e:
            return "-1"
