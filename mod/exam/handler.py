#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from sqlalchemy.orm.exc import NoResultFound
from ..models.exam_cache import ExamCache
import tornado.web
import tornado.gen
from time import time,localtime, strftime
import json, base64,traceback,urllib
from config import *
from ..auth.handler import authApi

class ExamHandler(tornado.web.RequestHandler):

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
		number = self.get_argument('cardnum',default=None)
		retjson = {'code':200, 'content':''}
		data = {
		'Login.Token1':number,
		'Login.Token2':self.get_argument('password'),
		}

		# read from cache
		try:
			status = self.db.query(ExamCache).filter(ExamCache.cardnum == number).one()
			if status.date > int(time())-100000 and status.text != '*':
			    self.write(base64.b64decode(status.text))
			    self.finish()
			    return
		except NoResultFound:
			status = ExamCache(cardnum = number,text = '*',date = int(time()))
			self.db.add(status)
		try:
		    self.db.commit()
		except:
		    self.db.rollback()

		try:
			client = AsyncHTTPClient()
			response = authApi(number,self.get_argument('password'))
			if response['code'] == 200:
				header['Cookie'] = response['content']
				request = HTTPRequest(
					FIRST_URL,
					method="GET",
					headers = header,
					request_timeout=TIME_OUT
				)
				response = yield tornado.gen.Task(client.fetch,request)
				header['Cookie'] = header['Cookie'].split(';')[0]+';'+response.headers['Set-Cookie']
				request = HTTPRequest(
					DETAIL_URL,
					method="GET",
					headers = header,
					request_timeout=TIME_OUT
				)
				response = yield tornado.gen.Task(client.fetch,request)
				retjson['content'] = self.dealData(response.body)
			else:
				retjson['code'] = 408
		except Exception,e:
			print traceback.print_exc()
			retjson['code'] = 500
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

	def dealData(self,content):
		content = BeautifulSoup(str(content))
		Table = content.findAll('table',{'class':'portlet-table'})[0]
		tr = Table.findAll('tr')
		ret = []
		length = len(tr) 
		if length == 1:
			return ret
		else:
			for i in range(1,length):
				td = tr[i].findAll('td')
				print td
				retTemp = {
					'course':td[2].text,
					'type':"",
					'teacher':td[3].text,
					'time':td[4].text,
					'location':td[5].text,
					'hour':td[6].text
				}
				ret.append(retTemp)
		return ret

