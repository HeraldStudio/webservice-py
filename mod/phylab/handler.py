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

class PhylabHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        number = self.get_argument('number',default=None)
        password = self.get_argument('password',default=None)
        term = self.get_argument('term',default=None)

        retjson = {'code':200, 'content':''}

        if not number or not password or not term:
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            if term =='shangbanxueqi':
                curType = cur_type_up
                retjson['content'] = {'基础性实验(上)':[],'基础性实验(上)选做':[],'文科及医学实验':[],'文科及医学实验选做':[]}
            elif term =='xiabanxueqi':
                curType = cur_type_down
                retjson['content'] = {'基础性实验(下)':[],'基础性实验(下)选做':[],'文科及医学实验':[],'文科及医学实验选做':[]}

            client = AsyncHTTPClient()
            loginValues['ctl00$cphSltMain$UserLogin1$txbUserCodeID'] = number
            loginValues['ctl00$cphSltMain$UserLogin1$txbUserPwd'] = password


            loginGet = HTTPRequest( 
                        LOGIN_URL,
                        method='GET',
                        request_timeout=TIME_OUT
            )
            Re = yield tornado.gen.Task(client.fetch, loginGet)
            if not Re.headers:
                    retjson['code'] = 408
                    retjson['content'] = 'time out'
            else:
                cookie_first = Re.headers['Set-Cookie'].split(';')[0]
                header['Cookie'] = cookie_first
                request = HTTPRequest(
                        LOGIN_URL,
                        method='POST',
                        headers = header,
                        body = urllib.urlencode(loginValues),
                        request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                cookie_second = cookie_first+";"+response.headers['Set-Cookie'].split(';')[0]
                header['Cookie'] = cookie_second

                for curNumber in curType:
                    selectData['ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp'] = curNumber
                    getRequest =HTTPRequest(
                            phyLabCurUrl,
                            body=urllib.urlencode(selectData),
                            method='POST',
                            headers = header,
                            request_timeout=TIME_OUT
                        )
                    getResponse = yield tornado.gen.Task(client.fetch, getRequest)
                    getContent = getResponse.body
                    retjson['content'][curType.get(curNumber)] = self.getCur(getContent)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
            

    def getCur(self,html):
        dealSoup = BeautifulSoup(html)
        curTable = dealSoup.find('table',id="ctl00_cphSltMain_ShowAStudentScore1_gvStudentCourse")
        if curTable==None:
            return ''
        else:
            ret_content = []
            content = curTable.findAll('span')
            length = len(content)
            temp = {
                'name':'',
                'Date':'',
                'Day':'',
                'Teacher':'',
                'Address':'',
                'Grade':''
            }
            k = length/6
            print k
            for i in range(k):
                index = i*6
                temp = {
                'name':content[index].string,
                'Date':content[index+2].string,
                'Day':content[index+3].string,
                'Teacher':content[index+1].string,
                'Address':content[index+4].string,
                'Grade':content[index+5].string
            }
                ret_content.append(temp)
        return ret_content