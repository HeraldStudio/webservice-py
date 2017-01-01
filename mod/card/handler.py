#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.card_cache import CardCache
from sqlalchemy.orm.exc import NoResultFound
from time import time,localtime, strftime
import tornado.web
import tornado.gen
import urllib, re
import json, base64
import datetime
import traceback
from ..auth.handler import authApi

class CARDHandler(tornado.web.RequestHandler):

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
        timedelta = int(self.get_argument('timedelta', default=0))
        # if int(timedelta)>7:
        #     timedelta = 7
        cardnum = self.get_argument('cardnum')
	cardnum_with_delta = cardnum + str(timedelta)
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}

        # read from cache
        try:
            status = self.db.query(CardCache).filter( CardCache.cardnum == cardnum_with_delta).one()
            if (int(strftime('%H', localtime(time())))<8 and status.text != '*') or (status.date > int(time())-7200 and status.text != '*'):
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return
        except NoResultFound:
            status = CardCache(cardnum=cardnum_with_delta, text='*', date=int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        try:
            client = AsyncHTTPClient()
            response = authApi(cardnum,self.get_argument('password'))
            if response['code']==200:
                cookie = response['content']
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

                soup = BeautifulSoup(str(response.body))
                td = soup.findAll('td',{"class": "neiwen"})
                userid = td[3].text
                cardState = td[42].text
                cardLetf = td[46].text.encode('utf-8').split('元')[0].replace(',','')
                # do not need to get the detail
                if timedelta == 0:
                    retjson['content'] = {'state':cardState, 'left':cardLetf}
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
                    return
                #get today detail
                elif timedelta == 1:
                    data = {
                        'account':userid,
                        'inputObject':"all",
                    }
                    request = HTTPRequest(
                        TODAYDATA_URL,
                        method='POST',
                        body=urllib.urlencode(data),
                        headers={'Cookie':cookie},
                        request_timeout=TIME_OUT
                    )
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body.decode('gbk'))
                    tr = soup.findAll('tr',{"class": re.compile("listbg")})
                    detail=[]
                    for td in tr:
                            td = td.findChildren()
                            tmp = {}
                            tmp['date'] = td[0].text
                            tmp['type'] = td[3].text
                            tmp['system'] = td[4].text
			    tmp['mail'] = td[4].text
                            tmp['price'] = td[5].text.replace(',','')
                            tmp['left'] = td[6].text.replace(',','')
                            detail.append(tmp)
                    retjson['content'] = {'state':cardState,'left':cardLetf,'detial':detail,'cardLeft':cardLetf,'detail':detail}
                #get other days detail depend on timedelta
                else:
                    request = HTTPRequest(
                        INIT_URL,
                        method='GET',
                        headers={'Cookie':cookie},
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                    __continue = soup.findAll('form',{'id':'accounthisTrjn1'})[0]['action']

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
                    __continue = soup.findAll('form',{'id':'accounthisTrjn2'})[0]['action']
                    request = HTTPRequest(
                        INDEX_URL+__continue,
                        method='POST',
                        headers={'Cookie':cookie},
                        body=urllib.urlencode(data),
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body)
                    __continue = 'accounthisTrjn3.action'
                    request = HTTPRequest(
                        INDEX_URL+__continue,
                        method='POST',
                        headers={'Cookie':cookie},
                        body=urllib.urlencode(data),
                        request_timeout=TIME_OUT)
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body.decode('gbk'))
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
                            tmp['price'] = td[5].text.replace(',','')
                            tmp['left'] = td[6].text.replace(',','')
                            if(tmp['type']==u'扣款'):
                                tmp['type'] = u'扣费'
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
                        soup = BeautifulSoup(response.body.decode('gbk'))
                    retjson['content'] = {'state':cardState, 'left':cardLetf, 'detial':detial}
            else:
                retjson['code'] = 500
                retjson['content'] = "wrong cardnum or password"
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = str(e)
	ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
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

