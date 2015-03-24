#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-11-04 13:38:58
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.nic_cache import NicCache
from sqlalchemy.orm.exc import NoResultFound
from time import time
import tornado.web
import tornado.gen
import urllib, re
import json, base64


class NICHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum')
        data = {
            'username':cardnum,
            'password':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}

        # read from cache
        try:
            status = self.db.query(NicCache).filter( NicCache.cardnum ==  cardnum ).one()
            if status.date == int(time())-600 and status.text != '*':
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return
        except NoResultFound:
            status = NicCache(cardnum=cardnum, text='*', date=int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        try:
            client = AsyncHTTPClient()
            client2 = HTTPClient()
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
                self.chose_type(client2, cookie, 'a')
                request = HTTPRequest(
                    DETIAL_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = client2.fetch(request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': re.compile('center|right')})
                    if td[1].text[:-14]:
                        ret['a'] = {'state': td[0].text, 'used': td[1].text[:-14]+'B'}
                    else:
                        ret['a'] = {'state': td[0].text, 'used': td[2].text[:-14]+'B'}
                else:
                    ret['a'] = {'state':'未开通'.decode('utf-8'), 'used':'0 B'}

                self.chose_type(client2, cookie, 'b')
                request = HTTPRequest(
                    DETIAL_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = client2.fetch(request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': re.compile('center|right')})
                    if td[1].text[:-14]:
                        ret['b'] = {'state': td[0].text, 'used': td[1].text[:-14]+'B'}
                    else:
                        ret['b'] = {'state': td[0].text, 'used': td[2].text[:-14]+'B'}
                else:
                    ret['b'] = {'state':'未开通'.decode('utf-8'), 'used':'0 B'}

                self.chose_type(client2, cookie, 'web')
                request = HTTPRequest(
                    WEB_URL,
                    method='GET',
                    headers={'Cookie':cookie},
                    request_timeout=TIME_OUT)
                response = client2.fetch(request)
                if len(response.body) > 10000:
                    soup = BeautifulSoup(response.body)
                    td = soup.findAll('td', {'bgcolor': '#FFFFFF', 'align': 'center'})
                    ret['web'] = {'state': td[0].text+','+td[1].text, 'used': td[-1].text}
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

                retjson['content'] = ret
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()
            finally:
                self.db.remove()
        self.db.close()

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
        response = client.fetch(request)