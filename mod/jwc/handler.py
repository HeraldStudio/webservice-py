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
import urllib,traceback,os

class JWCHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write("hello")
    def on_finish(self):
        self.db.close()

    def post(self):
        retjson = {'code':200, 'content':''}
        try:
            status = self.db.query(JWCCache).filter( JWCCache.date > int(time())-14000).order_by(JWCCache.date.desc()).all()
	    if len(status) == 0:
		raise NoResultFound
	    status = status[0]
            self.write(base64.b64decode(status.text))
            self.finish()
            return
        except NoResultFound:
            ret = self.refresh_status()
            if ret['code'] == 200:
                ret = json.dumps(ret, ensure_ascii=False, indent=2)
                status = JWCCache(date=int(time()), text=base64.b64encode(ret))
                self.db.add(status)
                self.db.commit()
                self.write(ret)
                self.finish()
                return
            else:
                retjson['code'] = 201
                retjson['content'] = 'refresh'
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = "error:"+str(e)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()


    def refresh_status(self):
        try:
            lock = self.db.query(JWCCache).filter(
                        JWCCache.date == 0).one()
        except NoResultFound:
            lock = JWCCache(date=0, text='0')
            self.db.add(lock)
        if lock.text == '1':
            return {'code':201}
        else:
            lock.text == '1'
            self.db.commit()
        ret = self.parser()
        lock.text == '0'
        self.db.commit()
        return ret

    def today(self):
        return int(strftime('%Y%m%d', localtime(time())))

    def parser(self):
        retjson = {'code':200,'content':''}
        header = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host':'jwc.seu.edu.cn',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
        }
        try:
            client = HTTPClient()
            request = HTTPRequest(JWC_URL, method='GET',headers=header,request_timeout=TIME_OUT)
            response = client.fetch(request)
            html = response.body
            soup = BeautifulSoup(html)
            items = soup.findAll('table', {'width':"100%"})
            info = {
                '最新动态': self.abstract(items[12:17],1), 
                '教务信息': self.abstract(items[34:34+7],0), 
                '学籍管理': self.abstract(items[45:45+7],0), 
                '实践教学': self.abstract(items[56:56+7],0), 
                '合作办学': self.abstract(items[67:67+4],0),
                }
            retjson = {'code':200, 'content':info}
        except:
            retjson['code'] = 400
            # print traceback.print_exc()
        return retjson

    def abstract(self, tag, x):
        abst = []
        for t in tag:
            if 1:
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
                        'date': str(t)[-36:-26],
                        })
            #except:
            #    pass
        return abst

