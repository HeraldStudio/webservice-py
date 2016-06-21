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
    def post(self):
        cardnum = self.get_argument('cardnum')
        password = self.get_argument('password')
        method_type = self.get_argument('method')
        retjson = {'code':200, 'content':''}
        try:
            if method_type not in method.keys():
                retjson['code'] = 500
                retjson['content'] = 'method is not allowed'
            else:
                cookie = getCookie(self.db,cardnum,password)
                if cookie['code'] == 200:
                    meth = method[method_type]
                    data = []
                    for i in meth['param']:
                        if method_type=='new' and i=='useUserIds':
                            ar = json.loads(self.get_argument(i))
                            user = ""
                            for j in ar:
                                user+=j+","
                            data.append((i,user))
                        if i=='orderVO.useMode':
                            data.append((i,{'1':2,'2':1}[self.get_argument(i)]))
                        else:
                            data.append((i,self.get_argument(i)))
                    # temp ignore judge
                    if method_type == "judgeOrder":
                        retjson['content'] = {'msg':'ok','code':0}
                    else:
                        retjson['content'] = self.getData(meth['url'],meth['method'],data,cookie['content'])
                else:
                    retjson['code'] = 408
                    retjson['content'] = 'cookie can not get'
        except MissingArgumentError:
            # traceback.print_exc()
            retjson['code'] = 400
            retjson['content'] = u'参数缺少'
        except:
            # traceback.print_exc()
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
                url = url.replace("+","%20")
                request.url = url
            elif data and method=="POST":
                realData = {}
                for i in data:
                    realData[i[0]] = i[1]
                data = urllib.urlencode(realData)
                request.body = data
            response = client.fetch(request)
            return json.loads(response.body)
        except Exception,e:
            # print str(e)
            # traceback.print_exc()
            return str(e)

        
