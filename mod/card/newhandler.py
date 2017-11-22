# -*- coding: utf-8 -*-
# @Date    : 2016/9/20  17:00
# @Author  : 490949611@qq.com
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.card_cache import CardCache
from sqlalchemy.orm.exc import NoResultFound
from time import time
import tornado.web
import tornado.gen
import urllib, re
import json, base64
import datetime
import traceback
from ..auth.handler import authApi
import requests

class NewCARDHandler(tornado.web.RequestHandler):

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
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}

        # read from cache
        try:
            status = self.db.query(CardCache).filter( CardCache.cardnum ==  cardnum ).one()
            if int(timedelta) == 0 and status.date > int(time())-600:
                self.write(base64.b64decode(status.text))
                self.db.close()
                self.finish()
                return
        except NoResultFound:
            status = CardCache(cardnum=cardnum, text='*', date=int(time()))
            self.db.add(status)
            try:
                self.db.commit()
            except:
                self.db.rollback()

        try:
            response = authApi(cardnum,self.get_argument('password'))
            if response['code']==200:
                cookie = response['content']
                response = requests.get(LOGIN_URL,headers={'Cookie':cookie})
                cookie += ';' + response.headers['Set-Cookie'].split(';')[0]
                response = requests.get(USERID_URL,headers={'Cookie':cookie})
                soup = BeautifulSoup(response.content)
                td = soup.findAll('td',{"class": "neiwen"})
                userid = td[3].text
                cardState = td[42].text
                cardLetf = td[46].text.encode('utf-8').split('元')[0]
                # do not need to get the detail
                if timedelta == 0:
                    retjson['content'] = {'state':cardState, 'left':cardLetf}
                    ret = json.dumps(retjson, ensure_ascii=False, indent=2)
                    self.write(retjson)
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
                    print "hello max~~"
                    data = {
                        'account':userid,
                        'inputObject':"all",
                    }
                    response = requests.post(TODAYDATA_URL,headers={'Cookie':cookie},data=data)
                    soup = BeautifulSoup(response.content)
                    tr = soup.findAll('tr',{"class": re.compile("listbg")})
                    detail=[]
                    for td in tr:
                            td = td.findChildren()
                            tmp = {}
                            tmp['date'] = td[0].text
                            tmp['type'] = td[3].text
                            tmp['system'] = td[4].text
                            tmp['price'] = td[5].text
                            tmp['left'] = td[6].text
                            detail.append(tmp)
                    retjson['content'] = {'state':cardState,'left':cardLetf,'detial':detail}
                #get other days detail depend on timedelta
                else:
                    response = requests.get(INIT_URL,headers={'Cookie':cookie})
                    soup = BeautifulSoup(response.content)
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
                    response = requests.post(INDEX_URL+__continue,headers={'Cookie':cookie},data=data)
                    soup = BeautifulSoup(response.content)
                    __continue = soup.findAll('form',{'id':'accounthisTrjn2'})[0]['action']
                    response = requests.post(INDEX_URL+__continue,headers={'Cookie':cookie},data=data)
                    soup = BeautifulSoup(response.content)
                    __continue = 'accounthisTrjn3.action'
                    response = requests.post(INDEX_URL+__continue,headers={'Cookie':cookie},data=data)
                    soup = BeautifulSoup(response.content)
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
                            if(tmp['type']==u'扣款'):
                                tmp['type'] = u'水电扣费'
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
                    retjson['content'] = {'state':cardState, 'left':cardLetf, 'detial':detial}
            else:
                retjson['code'] = 401
                retjson['content'] = 'wrong card number or password'
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
