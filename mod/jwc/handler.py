#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-12 18:17:20
# @Author  : yml_bright@163.com

from BeautifulSoup import BeautifulSoup
from config import JWC_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, HTTPClient
import tornado.web
import tornado.gen
from ..models.jwc_cache import JWCCache
from sqlalchemy.orm.exc import NoResultFound
from time import time, localtime, strftime
import json, base64
import urllib

class JWCHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write(self.parser())
        #self.write('Herald Web Service')

    def post(self):
        retjson = {'code':200, 'content':''}
        try:
            status = self.db.query(JWCCache).filter( JWCCache.date == self.today() ).one()
            self.write(base64.b64decode(status.text))
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
        lock = self.db.query(JWCCache).filter(
                    JWCCache.date == 0).one()
        if lock.text == '1':
            return
        else:
            lock.text == '1'
            self.db.commit()

        ret = self.parser()
        status = JWCCache(date=self.today(), text=base64.b64encode(ret))
        self.db.add(status)

        lock.text == '0'
        self.db.commit()
        self.db.close()

    def today(self):
        return int(strftime('%Y%m%d', localtime(time())))

    def parser(self):
        client = HTTPClient()
        request = HTTPRequest(JWC_URL, method='GET', request_timeout=TIME_OUT)
        response = client.fetch(request)
        html = response.body

        soup = BeautifulSoup(html)
        items = soup.findAll('table', {'width':"100%"})
        #return json.dumps([[i,items[i].text] for i in range(len(items))], ensure_ascii=False, indent=2)
        info = {
            '最新动态': self.abstract(items[13:13+5],1), 
            '教务信息': self.abstract(items[36:36+7],0), 
            '学籍管理': self.abstract(items[47:47+7],0), 
            '实践教学': self.abstract(items[58:58+7],0), 
            '合作办学': self.abstract(items[69:69+4],0),
            }
        
        return json.dumps(info, ensure_ascii=False, indent=2)

    def abstract(self, tag, x):
        abst = []
        for t in tag:
            try:
                if x:
                    abst.append({
                        'title': t.a.attrs[2][1],
                        'href': JWC_URL+t.a.attrs[0][1],
                        'date': t.div.text,
                        })
                else:
                    abst.append({
                        'title': t.a.attrs[2][1],
                        'href': JWC_URL+t.a.attrs[0][1],
                        'date': str(t)[-34:-24],
                        })
            except:
                pass
        return abst

