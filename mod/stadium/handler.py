# -*- coding: utf-8 -*-
# @Date    : 2015-05-24 
# @Author  : LiangJ

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib, json
from time import time, localtime, strftime
import traceback
class StadiumHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        print int(strftime('%H',localtime(time())))
        self.write('Herald Web Service')
        # url = 'http://123.57.143.92/'
        # client = HTTPClient()
        # nowtime = int(time.time())
        # print nowtime
        # content = 'hi'

        # data = {
        #     'time':nowtime,
        #     'content':content,
        #     'movieid':'000000001',
        #     'studentNum':'71113425'
        # }
        # params = urllib.urlencode(data)
        # request = HTTPRequest(url, method='POST',
        #                       body=params, request_timeout=TIME_OUT)
        # try:
        #     response = client.fetch(request)
        #     self.write(response)
        # except Exception,e:
              #print traceback.format_exc()
        #     print str(e)
        #     self.write(params)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('number')
        data = {
            'Login.Token1':cardnum,
            'Login.Token2':self.get_argument('password'),
        }
        retjson = {'code':200, 'content':''}

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
                    MY_ORDER_URL,
                    method='GET',
                    headers={'Cookie': cookie},
                    request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                #self.my_order(response.body)
                retjson['content'] = self.my_order(response.body)
        except Exception, e:
            retjson['code'] = 500
            retjson['content'] = 'error'
            print str(e)
            pass
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()
    def order(self):
        pass
    def my_order(self,content):
        dealSoup = BeautifulSoup(content)
        bodycontent = dealSoup.findAll('tr',{'class':'appos-item'})
        ret_content = []
        if bodycontent == None:
            return ''
        else:
            try:
                for i in bodycontent:
                    content = i.findAll('td')
                    length = len(content)
                    temp = {
                        'name':'',
                        'usetime':'',
                        'dotime':'',
                        'state':'' 
                    }
                    index = 0
                    temp = {
                    'name':content[index].string,
                    'usetime':content[index+1].string,
                    'dotime':content[index+2].string,
                    'state':content[index+3].contents[0].string,
                    }
                    ret_content.append(temp)
            except Exception, e:
                print e
        return ret_content


