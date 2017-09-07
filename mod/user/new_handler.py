# -*- coding: utf-8 -*-

from config import *

import re
import tornado
import urllib
import json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from ..models.user_detail import UserDetail
from sqlalchemy.orm.exc import NoResultFound


class newUserHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write("Herald Web Service")

    def on_finish(self):
        self.db.close()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        username = self.get_argument("username", default=None)
        _number = username
        password = self.get_argument("password", default=None)
        retjson = {"code": 500, "content": ""}

        if not username or not password:
            retjson['code'] = 400
            retjson['content'] = 'param lack'

        else:
            try:
                user = self.db.query(UserDetail).filter(_number == UserDetail.cardnum).one()
                retjson['code'] = 200
                retjson['content'] = {
                    'cardnum': user.cardnum,
                    'schoolnum': user.schoolnum,
                    'name': user.name,
                    'sex': user.sex
                }
                self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
                self.finish()
                return
            except NoResultFound as e:
                pass

            # result not found, start client
            client = AsyncHTTPClient()
            REQUEST_HEADERS = {
                'Connection': 'keep-alive'
                }
            try:
                request = HTTPRequest(
                    NEW_CHECK_URL,
                    method = "GET",
                    headers = REQUEST_HEADERS,
                    request_timeout = TIME_OUT,
                    follow_redirects = False
                    )
                response = yield tornado.gen.Task(client.fetch, request)

                cookie = ';'.join(response.headers["Set-Cookie"].split(';')[0].split(',')) + ';'
                REQUEST_HEADERS['Cookie'] = cookie
                POST_DATA['lt'] = re.findall(r'LT-.*-cas', response.body)[0]
                POST_DATA['execution'] = re.findall(r'e\ds\d', response.body)[0]
                POST_DATA['rmShown'] = 1
                POST_DATA['username'] = username
                POST_DATA['password'] = password

                request = HTTPRequest(
                    NEW_CHECK_URL,
                    method = "POST",
                    headers = REQUEST_HEADERS,
                    body = urllib.urlencode(POST_DATA),
                    request_timeout = TIME_OUT,
                    follow_redirects = False
                    )
                response = yield tornado.gen.Task(client.fetch, request)

                MIDDLE_REDIRECT_URL = response.headers['Location']
                cookie = re.findall(r'iPlanetDirectoryPro=.*', \
                    response.headers['Set-Cookie'])[0].split(';')[0] + ';'
                REQUEST_HEADERS['Cookie'] = cookie

                request = HTTPRequest(
                    MIDDLE_REDIRECT_URL,
                    method = "GET",
                    headers = REQUEST_HEADERS,
                    request_timeout = TIME_OUT,
                    follow_redirects = False
                    )
                response = yield tornado.gen.Task(client.fetch, request)

                cookie += re.findall(r'JSESSIONID=.*;', response.headers['Set-Cookie'])[0]
                REQUEST_HEADERS['Cookie'] = cookie

                # send a get request to my.seu.edu.cn INDEX
                # could be used to test the connection
                # request = HTTPRequest(
                #     USER_INDEX,
                #     method = "GET",
                #     headers = REQUEST_HEADERS,
                #     request_timeout = TIME_OUT,
                #     follow_redirects = False
                #     )
                # response = yield tornado.gen.Task(client.fetch, request)

                request = HTTPRequest(
                    URL,
                    method = "GET",
                    headers = REQUEST_HEADERS,
                    request_timeout = TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)

                if (len(re.findall(r'^22\d+$', username))!=0):
                    childId = '384'
                else:
                    childId = '241'
                USER_DETAIL_URL = "http://my.seu.edu.cn/" \
                    + re.findall(r'pnull\..*pen=pe575', response.body)[0] \
                    + "&itemId=381&childId=" + childId + "&page=1"

                request = HTTPRequest(
                    USER_DETAIL_URL,
                    method = "GET",
                    headers = REQUEST_HEADERS,
                    request_timeout = TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                _cardnum = username
                _schoolnum = re.findall(r'<td .*>\r\s+\S+', response.body)[11][26:]
                _name = re.findall(r'<td .*>\r\s+\S+', response.body)[2][26:]
                _sex = re.findall(r'<td .*>\r\s+\S+', response.body)[5][26:]
                retjson['content'] = {
                    'schoolnum': _schoolnum,
                    'cardnum': _cardnum,
                    'name': _name,
                    'sex': _sex
                }
                retjson['code'] = 200
                user_detail = UserDetail(schoolnum = _schoolnum, \
                    cardnum = _cardnum, name = _name, sex = _sex)
                self.db.add(user_detail)
                self.db.commit()

            except Exception as e:
                retjson['code'] = 500
                retjson['content'] = str(e)

        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
