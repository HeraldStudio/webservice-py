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
import io
# import Image
from PIL import Image
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

	@tornado.gen.engine
	def post(self):
		number = self.get_argument('cardnum',default=None)
		password = self.get_argument('password')
		retjson = {'code':200, 'content':''}
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
		retjson = yield tornado.gen.Task(self.jwcHandler,number,password)
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
	@tornado.web.asynchronous
	@tornado.gen.engine
	def newSeuHandler(self,number,password,callback=None):
		retjson = {'code':200, 'content':''}
		try:
			client = AsyncHTTPClient()
			response = authApi(number,password)
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
		except IndexError:
			retjson['code'] = 200
			retjson['content'] = u'当前不在考试周'
		except Exception,e:
			retjson['code'] = 500
		callback(retjson)
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
	@tornado.web.asynchronous
	@tornado.gen.engine
	def jwcHandler(self,number,password,callback=None):
		retjson = {'code':200, 'content':''}
		try:
			client = AsyncHTTPClient()
			request = HTTPRequest(VERCODE_URL, request_timeout=TIME_OUT)
			response = yield tornado.gen.Task(client.fetch, request)
			if not response.headers:
				retjson['code'] = 408
				retjson['content'] = 'time out'
			else:
				cookie = response.headers['Set-Cookie'].split(';')[0]+";"+response.headers['Set-Cookie'].split(';')[1].split(',')[1]
				img = Image.open(io.BytesIO(response.body))
				vercode = self.recognize(img)
				params = urllib.urlencode({
					'userName': number,
					'password': password,
					'vercode': vercode
				})
				request = HTTPRequest(LOGIN_URL, body=params, method='POST',
					headers={'Cookie': cookie},
					request_timeout=TIME_OUT)
				response = yield tornado.gen.Task(client.fetch, request)
				if not response.headers:
					retjson['code'] = 409
					retjson['content'] = 'time out'
				else:
					if 'vercode' in str(response.body):
						retjson['code'] = 401
						retjson['content'] = 'wrong card number or password'
					else:
						request = HTTPRequest(INFO_URL,
							request_timeout=TIME_OUT,
							headers={'Cookie': cookie})
						response = yield tornado.gen.Task(client.fetch, request)
						if not response.headers:
							retjson['code'] = 410
							retjson['content'] = 'time out'
						else:
							retjson['content'] = self.parser(response.body)
		except Exception,e:
			retjson['code'] = 500
			retjson['content'] = str(e)
		callback(retjson)
	def parser(self,content):
		content = BeautifulSoup(str(content))
		Table = content.findAll('table',{'id':'table2'})[0]
		tr = Table.findAll('tr')
		ret = []
		length = len(tr) 
		if length == 1:
			return ret
		else:
			for i in range(1,length):
				td = tr[i].findAll('td')
				retTemp = {
					'course':td[3].text,
					'type':td[4].text,
					'teacher':td[5].text[:-6],
					'time':td[6].text[:-6],
					'location':td[7].text,
					'hour':td[8].text
				}
				ret.append(retTemp)
		return ret

	def recognize(self, img):
		start = [13, 59, 105, 151]
		result = ''
		for i in start:
			sample = []
			for i in xrange(i, i + 40):
				temp = 0
				for j in xrange(0, 100):
					temp += (img.getpixel((i, j))[1] < 40)
				sample.append(temp)
			min_score = 1000
			max_match = 0
			for idx, val in enumerate(STANDARD):
				diff = []
				for i in xrange(len(sample)):
					diff.append(sample[i] - val[i])
				avg = float(sum(diff)) / len(diff)

				for i in xrange(len(sample)):
					diff[i] = abs(diff[i] - avg)
				score = sum(diff)
				if score < min_score:
					min_score = score
					max_match = idx

			result = result + str(max_match)
		return result

