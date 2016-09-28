#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 19:19:09
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from bs4 import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json, re

class LibRenewHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        barcode = self.get_argument('barcode')
        data = {
            'number': self.get_argument('cardnum'),
            'passwd': self.get_argument('password'),
            'select': 'bar_no'
        }
        retjson = {'code':200, 'content':''}

        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                LOGIN_URL,
                method='GET',
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            cookie = response.headers['Set-Cookie'].split(';')[0]
            request = HTTPRequest(
                LOGIN_URL,
                method='POST',
                headers={'Cookie':cookie},
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)

            if len(response.body) < 10000:
                data['select'] = 'cert_no'
                request = HTTPRequest(
                    LOGIN_URL,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)

            if len(response.body) > 10000:
                flag = False
                request = HTTPRequest(
                    LIST_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td', {'class': 'whitetext'})
                for i in range(0, len(td), 8):
                    if barcode == td[i].text:
                        checkcode = td[i+7].input['onclick'].split('\'')[3]
                        request = HTTPRequest(
                            RENEW_URL%(barcode, checkcode),
                            method='GET',
                            headers={'Cookie':cookie},
                            request_timeout=TIME_OUT)
                        response = yield tornado.gen.Task(client.fetch, request)
                        if response.body == 'invalid call':
                            flag = False
                        else:
                            retjson['content'] = response.body
                            flag = True
                if flag:
                    if u'续借成功' in retjson['content']:
                        retjson['content'] = 'success'
                    else:
                        temp = retjson['content']
                        temp = re.search('>.*<',temp,re.I).group()
                        retjson['content '] = temp[1:len(temp)-1]
                else:
                    retjson['content'] = 'fail'
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

