#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib, re
import json
import datetime

class CARDHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        timedelta = int(self.get_argument('timedelta', default=0))
        data = {
            'Login.Token1':self.get_argument('cardnum'),
            'Login.Token2':self.get_argument('password'),
        }
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                CHECK_URL,
                method='POST',
                body=urllib.urlencode(data),
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if response.body and response.body.find('Successed')>0:
                cookie = response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    LOGIN_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)

                cookie += ';' + response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                    USERID_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td',{"class": "neiwen"})
                userid = td[3].text
                cardState = td[42].text
                cardLetf = td[46].text.encode('utf-8').split('元')[0]

                if timedelta == 0:
                    self.write(json.dumps({'state':cardState, 'left':cardLetf}, ensure_ascii=False, indent=2))
                    self.finish()
                    return

                request = HTTPRequest(
                    INIT_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action']

                now = datetime.datetime.now()
                delta = datetime.timedelta(timedelta)
                page = 1
                data = {
                    'account':userid,
                    'inputObject':'all',
                    'inputStartDate':(now - delta).strftime('%Y%m%d'),
                    'inputEndDate':now.strftime('%Y%m%d'),
                    'pageNum':page
                }
                request = HTTPRequest(
                    INDEX_URL+__continue,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action']
                request = HTTPRequest(
                    INDEX_URL+__continue,
                    method='POST',
                    headers={'Cookie':cookie},
                    body=urllib.urlencode(data),
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                __continue = soup.findAll('form',{'name':'form1'})[0]['action']
                request = HTTPRequest(
                    INIT_URL+__continue,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)

                detial = []
                count = 0
                while 1:
                    tr = soup.findAll('tr',{"class": re.compile("listbg")})
                    if not tr:
                        break
                    for td in tr:
                        td = td.findChildren()
                        tmp = {}
                        tmp['date'] = td[0].text
                        tmp['type'] = td[3].text
                        tmp['system'] = td[4].text
                        tmp['price'] = td[5].text
                        tmp['left'] = td[6].text
                        detial.append(tmp)
                    page += 1
                    data['pageNum'] = page
                    request = HTTPRequest(
                        DATA_URL,
                        method='POST',
                        headers={'Cookie':cookie},
                        body=urllib.urlencode(data),
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                self.write(json.dumps({'state':cardState, 'left':cardLetf, 'detial':detial}, ensure_ascii=False, indent=2))
            else:
                self.write('wrong card number or password')
        except:
            self.write('error')
        self.finish()