# -*- coding: utf-8 -*-
# @Date    : 2016-02-21 15:43:36
# @Author  : jerry.liangj@qq.com

from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPError
import json
import tornado.web
import tornado.gen
import urllib
from sgmllib import SGMLParser

from config import loginurl1,runurl

import base64
from sqlalchemy.orm.exc import NoResultFound
from ..models.pe_models import PeDetailCache
from time import time,localtime, strftime

class RunningParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
    
    def getRunningTable(self, text):
        self.table = []
        self.row = []
        self.flag = 0
        self.form = 0
        # _cookies = cookies
        # _url = 'http://zccx.seu.edu.cn/SportWeb/gym/gymExercise/gymExercise_query_result_2.jsp?xh=%s'%(card_id)
        self.feed(text)

    def start_form(self, attrs):
        self.form += 1

    def end_form(self):
        self.form -= 1
        msg = {}
        msg['sign_date'] = self.row[3]
        msg['sign_time'] = self.row[4]
        msg['sign_effect'] = self.row[6]
        self.table.append(msg)
        self.row = []


    def start_td(self, attrs):
        self.flag += 1

    def end_td(self):
        self.flag -= 1

    def handle_data(self, text):
        if self.flag == 3 and self.form == 1:
            self.row.append(text)


class pedetailHandler(tornado.web.RequestHandler):
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
		retjson = {'code':200,'content':''}
		cardnum = self.get_argument('cardnum',default=None)
		password = self.get_argument('password',default=None)
		status = None
		if not (cardnum and password):
			retjson['code'] = 400
			retjson['content'] = 'params lack'
		else:
			# read from cache
			try:
				status = self.db.query(PeDetailCache).filter(PeDetailCache.cardnum == cardnum).one()
				if status.date > int(time())-10000 and status.text != '*':
					self.write(base64.b64decode(status.text))
					self.finish()
					return
			except NoResultFound:
				status = PeDetailCache(cardnum = cardnum,text = '*',date = int(time()))
				self.db.add(status)
				try:
					self.db.commit()
				except:
					self.db.rollback()

			try:
				client = AsyncHTTPClient()
				data = {
					"Login.Token1" : cardnum,
					"Login.Token2" : password,
					'goto' : "http://mynew.seu.edu.cn/loginSuccess.portal",
					'gotoOnFail' : "http://mynew.seu.edu.cn/loginFailure.portal"
				}
				data1 = {
					'IDToken0':   '',
					'IDToken1':cardnum,
					'IDToken2':password,
					'IDButton':'Submit',
					'goto':'http://zccx.seu.edu.cn/',
					'gx_charset':'gb2312'
				}

				cookie1 = ''
				request = HTTPRequest(
					loginurl1,
					method='POST',
					body = urllib.urlencode(data1),
					follow_redirects=False
				)
				initcookie = ''
				try:
					response = yield client.fetch(request)
				except HTTPError as e:
					initcookie = e.response.headers['Set-Cookie']
				init_cookie1 = initcookie.split(';')[4].split(',')[1]#+initcookie.split(';')[0]
				header = {
					'Host':'zccx.seu.edu.cn',
					'Accept': 'textml,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
					'Referer':'http://zccx.seu.edu.cn/',
					'Connection':'Keep-alive',
					'Accept-Encoding': 'gzip, deflate',
					'Accept-Language': 'zh-CN,zh;q=0.8',
					'Cookie':init_cookie1+';'+cookie1+';'+';amblcookie=02'
				}
				request = HTTPRequest(
					runurl,
					method='GET',
					headers = header
				)
				
				response = yield client.fetch(request)
				cookie1 = response.headers['Set-Cookie']
				header['Cookie'] = init_cookie1+';'+cookie1+';'+';amblcookie=02'  
				getpeurl = "http://zccx.seu.edu.cn/SportWeb/gym/gymExercise/gymExercise_query_result_2.jsp?xh=%s"%(cardnum)
				request = HTTPRequest(
				    getpeurl,
				    headers = header,
				    request_timeout=8
				    )
				response = yield client.fetch(request)
				spider = RunningParser()
				spider.getRunningTable(response.body)
				retjson['content'] = spider.table
			except HTTPError as e:
				retjson['code'] = 500
				retjson['content'] = str(e)
		ret = json.dumps(retjson, ensure_ascii=False, indent=2)
		self.write(ret)
		self.finish()

		# refresh cache
		if retjson['code'] == 200:
			status.date = int(time())
			status.text = base64.b64encode(ret)
			self.db.add(status)
			try:
				self.db.commit()
			except Exception,e:
				self.db.rollback()
			finally:
				self.db.remove()