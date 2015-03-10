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
        self.post()
        #self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        retjson = {'code':200, 'content':''}
        cardnum = '213120498'
        password = ''
        client = AsyncHTTPClient()
        request = HTTPRequest(
            LOGIN_URL,
            method='POST',
            body=POST_DATA + "&ctl00$cphSltMain$UserLogin1$txbUserCodeID=%s&ctl00$cphSltMain$UserLogin1$txbUserPwd=%s"%(cardnum, password),
            request_timeout=TIME_OUT,
            headers = { 'Cache-Control': 'no-cache',
                        'Origin': 'http://phylab.seu.edu.cn',
                        'X-MicrosoftAjax': 'Delta=true',
                        'Cookie':'.ASPXANONYMOUS=cgcHQ5KR0AEkAAAAOWNmNWY1MDUtZTJkYy00NmQyLTliNWEtMTUwYzkxMGYwNGYyoTztJQEuHct8TNxENP01swAAAAA1; ASPSESSIONIDCQBRRQTC=OOHHONADEEADNFCHPKMMFJNH',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': '*/*',
                        'Referer': 'http://phylab.seu.edu.cn/plms/UserLogin.aspx?ReturnUrl=%%2fplms%%2fSelectLabSys%%2fDefault.aspx',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'}
            )
        response = yield tornado.gen.Task(client.fetch, request)
        print response.headers
        self.write(response.body)
        self.finish()
        return