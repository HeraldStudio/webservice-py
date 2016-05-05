# -*- coding: utf-8 -*-
# @Date    : 2016-03-24 16 16:34:57
# @Author  : jerry.liangj@qq.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient
from tornado.httputil import url_concat
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
from tornado.web import MissingArgumentError
import tornado.gen
import urllib, json
from ..models.cookie_cache import CookieCache
from ..auth.cookie import getCookie
import traceback

class YuyueHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def on_finish(self):
        self.db.close()

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self,method_type):
        cardnum = self.get_argument('cardnum')
        password = self.get_argument('password')
        retjson = {'code':200, 'content':''}
        try:
            if method_type not in method.keys():
                retjson['code'] = 500
                retjson['content'] = 'method is not allowed'
            else:
                cookie = getCookie(self.db,cardnum,password)
                if cookie['code'] == 200:
                    meth = method[method_type]
                    data = {}
                    for i in meth['param']:
                        if method_type=='new' and i=='useUserIds':
                            ar = self.get_arguments(i)
                            count = 0
                            data[i] = ''
                            for j in ar:
                                if count:
                                    data[i] += '&useUserIds='+j
                                else:
                                    data[i] += j
                                    count = 1
                            print data[i]
                        else:
                            data[i] = self.get_argument(i)
                    retjson['content'] = self.getData(meth['url'],meth['method'],data,cookie['content'])
                else:
                    retjson['code'] = 408
                    retjson['content'] = 'cookie can not get'
        except MissingArgumentError:
            traceback.print_exc()
            retjson['code'] = 400
            retjson['content'] = u'参数缺少'
        except:
            traceback.print_exc()
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()


    def getData(self,url,method,data,cookie):
        try:
            client = HTTPClient()
            request = HTTPRequest(
                    url,
                    method=method,
                    headers={
                        'Cookie':cookie
                    }
                )
            if data and method=="GET":
                url = url_concat(url,data)
                request.url = url
            elif data and method=="POST":
                data = urllib.urlencode(data)
                request.body = data
            print request.url
            response = client.fetch(request)
            return json.loads(response.body)
        except Exception,e:
            # print str(e)
            traceback.print_exc()
            return str(e)

        
