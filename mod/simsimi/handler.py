# -*- coding: utf-8 -*-
# @Date    : 2014-11-05 22:11:57
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import tornado.web
import tornado.gen
import json
import urllib
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class SIMSIMIHandler(tornado.web.RequestHandler):

    def get(self):
        self.post()
        #self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        msg = self.get_argument('msg', default='你好')
        uid = self.get_argument('uid', default='')
        data = {
            'key': KEY,
            'info': msg,
            'loc': '江苏南京江宁',
            'userid': uid
        }
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest(
                TULING_URL + urllib.urlencode(data),
                method='GET',
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            retjson = json.loads(response.body)
            self.write(self.msgmap[retjson['code']](retjson).replace(u'小Q',u'小猴'))
        except Exception,e:
            self.write('error')
        self.finish()

        # msg = self.get_argument('msg', default='hello')
        # try:
        #     client = AsyncHTTPClient()
        #     request = HTTPRequest(
        #         SIMSIMI_URL + msg,
        #         method='GET',
        #         request_timeout=TIME_OUT,
        #         headers={'Cookie': COOKIE, 'User-Agent': AGENT})
        #     response = yield tornado.gen.Task(client.fetch, request)
        #     x = json.loads(response.body.decode('utf8'))
        #     if x[u'msg'] == 'OK':
        #         self.write(x[u'sentence_resp'].encode('utf8'))
        #         self.finish()
        #     else:
        #         self.write('error')
        #         self.finish()
        # except:
        #     self.write('error')
        #     self.finish()
    @property
    def msgmap(self):
        return {
            100000 : self.text,
            200000 : self.link,
            301000 : self.book,
            302000 : self.news,
            304000 : self.app,
            305000 : self.train,
            306000 : self.plane,
            307000 : self.shopping,
            308000 : self.movie,
            309000 : self.hotel,
            310000 : self.lottery,
            311000 : self.price,
            312000 : self.restaurant,
            50000 : self.error,
            40004 : self.useoff,
        }

    def useoff(self, data):
        return u'小猴累了，回家休息了，明天再来找TA吧'

    def text(self, data):
        return data['text']

    def link(self, data):
        return u'不如用电脑查查，么么哒'

    def book(self, data):
        msg = u'[图书]\n'
        for b in data['list']:
            msg += u'<%s> %s\n'%(b['name'], b['author'])
        return msg

    def news(self, data):
        msg = u'[新闻]\n'
        for n in data['list']:
            msg += u'<a href="%s">%s</a>\n'%(n['detailurl'],n['article'])
        return msg

    def app(self, data):
        msg = u'[应用]\n'
        for a in data['list']:
            msg += u'%s\n'%a['name']
        return msg

    def train(self, data):
        return u'不如用电脑查查，么么哒'

    def plane(self, data):
        return u'不如用电脑查查，么么哒'

    def shopping(self, data):
        return u'不如用电脑查查，么么哒'

    def movie(self, data):
        return u'不如用电脑查查，么么哒'

    def hotel(self, data):
        return u'不如用电脑查查，么么哒'

    def lottery(self, data):
        return u'不如用电脑查查，么么哒'

    def price(self, data):
        return u'不如用电脑查查，么么哒'

    def restaurant(self, data):
        return u'不如用电脑查查，么么哒'

    def error(self, data):
        return data['text']
