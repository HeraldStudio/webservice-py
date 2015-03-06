#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 18:51:29
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, HTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
from ..models.pc_cache import PCCache
from sqlalchemy.orm.exc import NoResultFound
from time import time, localtime, strftime
import urllib, re
import json
import base64

class PCHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def post(self):
        retjson = {'code':200, 'content':u'暂时关闭'}
        try:
            status = self.db.query(PCCache).filter( PCCache.date == self.today() ).one()
            retjson['content'] = base64.b64decode(status.text)
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.db.close()
            self.finish()
        except NoResultFound:
            retjson['code'] = 201
            retjson['content'] = 'refreshing'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()
            self.refresh_status()
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()

    def refresh_status(self):
        lock = self.db.query(PCCache).filter(
                    PCCache.date == 0).one()
        if lock.text == '1':
            return
        else:
            lock.text == '1'
            self.db.commit()

        ret = self.renren_request()
        if ret and (ret['time'].find('小时')>=0 or ret['time'].find('分钟')>=0 or ret['time'].find('刚')>=0):
            self.recognize(ret['text'])

        lock.text == '0'
        self.db.commit()
        self.db.close()

    def today(self):
        return int(strftime('%Y%m%d', localtime(time())))

    def recognize(self, text):
        y_keyword = ['正常跑操', '跑操正常', '今天继续跑操', '今天跑操']
        result = u'今天不跑操'
        for k in y_keyword:
            if text.find(k)>=0:
                result = u'今天正常跑操'
                break
        status = PCCache(date=self.today(), text=base64.b64encode(result))
        self.db.add(status)
        self.db.commit()

    def renren_request(self):
        client = HTTPClient()
        request = HTTPRequest(
            RENREN_URL,
            method='GET',
            request_timeout=TIME_OUT,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        response = client.fetch(request)
        if response.body > 2048:
            soup = BeautifulSoup(response.body)
            status = soup.findAll('div',{'class':'page-status'})[0].findChildren()
            text = status[-2].text
            time = status[-1].text
            if text.find('早播报')>0:
                return {'text':text, 'time':time}
            else:
                return None
        else:
            return None
