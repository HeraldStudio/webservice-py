#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-04 13:38:58
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib, re
import json


class NICHandler(tornado.web.RequestHandler):

    def get(self):
        self.post()
        #self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        data = {
            'username':self.get_argument('cardnum'),
            'password':self.get_argument('password'),
        }
        if 1:
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
                body = urllib.urlencode(data),
                headers={'Cookie':cookie},
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if len(response.body) > 10000:
                ret = {}
                self.chose_type(client, cookie, 'a')
                request = HTTPRequest(
                    DETIAL_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': re.compile('center|right')})
                    ret['a'] = {'state': td[0].text, 'used': td[1].text[:-14]+'B'}
                else:
                    ret['a'] = {'state':'未开通'.decode('utf-8'), 'used':'0 B'}

                self.chose_type(client, cookie, 'b')
                request = HTTPRequest(
                    DETIAL_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': re.compile('center|right')})
                    ret['b'] = {'state': td[0].text, 'used': td[1].text[:-14]+'B'}
                else:
                    ret['b'] = {'state':'未开通'.decode('utf-8'), 'used':'0 B'}

                self.chose_type(client, cookie, 'web')
                request = HTTPRequest(
                    WEB_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': 'center'})
                    ret['web'] = {'state': td[0].text+','+td[1].text, 'used': td[2].text}
                else:
                    ret['web'] = {'state':'未开通'.decode('utf-8'), 'used':'0 B'}

                request = HTTPRequest(
                    FEE_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body)
                td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': 'center'})
                ret['left'] = td[0].text

                self.write(json.dumps(ret, ensure_ascii=False, indent=2))
            else:
                self.write('wrong card number or password')
        #except:
        #    self.write('error')
        self.finish()

    @tornado.gen.engine
    def chose_type(self, client, cookie, type):
        data = {
            'operation': 'status',
            'item': type,
            'web_sel':1,
        }
        request = HTTPRequest(
            CHOISE_URL,
            method='POST',
            body = urllib.urlencode(data),
            headers={'Cookie':cookie},
            request_timeout=TIME_OUT)
        response = yield tornado.gen.Task(client.fetch, request)