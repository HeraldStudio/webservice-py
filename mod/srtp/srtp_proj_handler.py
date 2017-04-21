#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/4/21 21:10
# @Author  : higuoxing@outlook.com

import tornado.web
import tornado.gen
import json, base64
import urllib, re
import traceback
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import url_concat
from bs4 import BeautifulSoup
from time import time
from sqlalchemy.orm.exc import NoResultFound
from ..models.srtp_proj_cache import SrtpProjCache
from ..auth.handler import authApi
from srtp_proj_config import *

class SrtpProjHandler(tornado.web.RequestHandler):
    
    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service:)')
    
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        #build data
        cardnum = self.get_argument('cardnum')
        data['UserId'] = self.get_argument('cardnum')
        data['Pwd'] = self.get_argument('password')
        client = AsyncHTTPClient()
        cookieJar = ''
        retjson = {'code': 200, 'content': ''}

        #read from cache
        try:
            status = self.db.query(SrtpProjCache).filter( \
                    SrtpProjCache.cardnum == cardnum).one()
            if status.date > int(time()) - \
                    3600 * 24 * 3 and status.text != '*':
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return 
        except NoResultFound:
            status = SrtpProjCache( \
                    cardnum = cardnum, text = '*', date = int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        #get page cookies
        try:
            response = authApi(cardnum, self.get_argument('password'))
            if response['code'] == 200:
                cookie = response['content']
                request = HTTPRequest(
                    CHECK_URL,
                    method = 'GET',
                    headers = {'Cookie': cookieJar},
                    request_timeout = TIME_OUT
                )
                response = yield tornado.gen.Task(client.fetch, request)
                cookieJar +=  response.headers['Set-Cookie'].split(';')[0] + \
                        ';' + response.headers['Set-Cookie'].split(';')[2].split(',')[1] + ';'

                #get auth
                request = HTTPRequest(
                    CHECK_URL,
                    method = 'POST',
                    body = urllib.urlencode(data),
                    headers = {'Cookie': cookieJar}
                )
                response = yield tornado.gen.Task(client.fetch, request)
                cookieJar += response.headers['Set-Cookie'].split(';')[0]
                soup = BeautifulSoup(response.body, 'html5lib')
                sid = soup.find_all(type = "text/javascript")[-1].text[47:63]
                screen = soup.find_all(type = "text/javascript")[-1].text[71:87]
                params = {'sid': sid, 'screen': screen}

                Srtp_Item = []
                count = 0

                while 1:
                    abstract_url = url_concat(ABSTRACT_URL, params)
                    request = HTTPRequest(
                        abstract_url,
                        method = 'GET',
                        headers = {
                                'Cookie': cookieJar,
                                'Referer': LOG_IN_URL
                                }
                    )
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body.decode('gbk', 'ignore'), 'html5lib')
                    tr = soup.find_all('tr', align = 'center', bgcolor = 'White')
                    if not tr:
                        break
                    for td in tr:
                        td = td.findChildren()
                        tmp = {}
                        tmp['proj_name'] = td[4].text
                        tmp['proj_type'] = td[5].text
                        tmp['clg'] = td[9].text
                        tmp['tutor'] = td[10].text[5:-5]
                        tmp['ptn'] = td[12].text[5:-5]
                        tmp['ld'] = td[14].text
                        tmp['tutor_sgst'] = td[15].text[5:-5]
                        tmp['clg_expt_sgst'] = td[18].text[5:-5]
                        tmp['clg_sgst'] = td[21].text[5:-5]
                        tmp['uni_expt_sgst'] = td[24].text[5:-5]
                        tmp['uni_sgst'] = td[27].text[5:-5]
                        Srtp_Item.append(tmp)
                        count += 1
                    break
                retjson['content'] = {'count': count, 'detail': Srtp_Item}
                ret = json.dumps(retjson, ensure_ascii = True, indent = 4)
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except Exception,e:
            #print str(e)
            retjson['code'] = 500
            retjson['content'] = 'error'
            if status.text!='*':
                self.write(base64.b64decode(status.text))
                self.finish()
                return

        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        #refresh cache
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
