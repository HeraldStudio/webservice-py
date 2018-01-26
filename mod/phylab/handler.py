#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:46:36
# @Author  : yml_bright@163.com

from .._config import phylabCacheTime
from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.phylab_cache import PhylabCache
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib
import json, base64
from time import time, localtime, strftime
import datetime
import traceback

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
            # read from cache
            try:
                status = self.db.query(PhylabCache).filter( PhylabCache.cardnum ==  number ).one()
                if status.date > int(time())-phylabCacheTime and status.text != '*':
                    self.write(base64.b64decode(status.text))
                    self.db.close()
                    self.finish()
                    return
            except NoResultFound:
                status = PhylabCache(cardnum=number, text='*', date=int(time()))
                self.db.add(status)
                try:
                    self.db.commit()
                except:
                    self.db.rollback()

            if int(term[3:5]) - int(number[3:5]) == 1:
                curType = cur_type_up
                retjson['content'] = {'基础性实验(上)':[],'基础性实验(上)选做':[],'文科及医学实验':[],'文科及医学实验选做':[]}
            else:
                curType = cur_type_down
                retjson['content'] = {'基础性实验(下)':[],'基础性实验(下)选做':[],'文科及医学实验':[],'文科及医学实验选做':[]}

            client = AsyncHTTPClient()
            loginValues['ctl00$cphSltMain$UserLogin1$txbUserCodeID'] = number
            loginValues['ctl00$cphSltMain$UserLogin1$txbUserPwd'] = password

            try:
                request = HTTPRequest(
                        LOGIN_URL,
                        method='GET',
                        request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                self.init_data(response.body)
                header['Cookie'] = response.headers['Set-Cookie'].split(';')[0]
                request = HTTPRequest(
                        LOGIN_URL,
                        method='POST',
                        headers = header,
                        body = urllib.urlencode(loginValues),
                        request_timeout=TIME_OUT
                    )
                response = yield tornado.gen.Task(client.fetch, request)
                header['Cookie'] += ';'+response.headers['Set-Cookie'].split(';')[0]
                self.init_select_data(header['Cookie'])
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
                    retjson['content'][curType.get(curNumber)] = self.getCur(getResponse.body)
	    except KeyError:
                retjson = {
                    'code':200,
                    'content':{}
                }
            except Exception,e:
                retjson['code'] = 500
                retjson['content'] = 'error'
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
            

    def getCur(self,html):
        dealSoup = BeautifulSoup(str(html))
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

    def init_data(self,body):
        try:
            content = BeautifulSoup(body)
            viewstate_value = content.find('input',{'id':'__VIEWSTATE'})
            EVENTVALIDATION = content.find('input',{'id':'__EVENTVALIDATION'})
            loginValues['__VIEWSTATE'] = viewstate_value['value']
            loginValues['__EVENTVALIDATION'] = EVENTVALIDATION['value']
        except:
            pass

    def init_select_data(self,cookie):
        try:
            client = HTTPClient()
            request = HTTPRequest(
                SELECTURL,
                method = "GET",
                headers = header,
                request_timeout=TIME_OUT
                )
            response = client.fetch(request)
            content = BeautifulSoup(response.body)
            viewstate_value = content.find('input',{'id':'__VIEWSTATE'})
            EVENTVALIDATION = content.find('input',{'id':'__EVENTVALIDATION'})
            selectData['__VIEWSTATE'] = viewstate_value['value']
            selectData['__EVENTVALIDATION'] = EVENTVALIDATION['value']
        except Exception,e:
            pass
