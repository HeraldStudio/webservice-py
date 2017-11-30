# -*- coding: utf-8 -*-
import json, urllib
import tornado.web
import tornado.gen
from datetime import date, timedelta
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import traceback

class NewNewHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        ret = { 'code': 200, 'content': '' }
        try:
            campus_id = self.get_argument('campusId', default='22')
            date = self.get_argument('date')
            building_id = self.get_argument('buildingId', default='')
            start_sequence = self.get_argument('startSequence')
            end_sequence = self.get_argument('endSequence')
            page = self.get_argument('page', default='1')
            page_size = self.get_argument('pageSize', default='10')
            
            client = AsyncHTTPClient()
            request = HTTPRequest('http://58.192.114.179/classroom/common/getdateofweek?date=' + date)
            response = yield tornado.gen.Task(client.fetch, request)
            date_info = json.loads(response.body)
            
            request = HTTPRequest('http://58.192.114.179/classroom/show/getemptyclassroomlist', 
                                  method='POST', 
                                  body=urllib.urlencode({
                                      'pageNo': page,
                                      'pageSize': page_size,
                                      'campusId': campus_id,
                                      'buildingId': building_id,
                                      'startWeek': date_info['week'],
                                      'endWeek': date_info['week'],
                                      'dayOfWeek': date_info['dayOfWeek'],
                                      'startSequence': start_sequence,
                                      'endSequence': end_sequence,
                                      'termId': date_info['termId']
                                  }))
            response = yield tornado.gen.Task(client.fetch, request)
            ret['content'] = json.loads(response.body)
        except Exception,e:
            print e
            ret['code'] = 500
            ret['content'] = 'error'
            traceback.print_exc(e)
        self.write(json.dumps(ret,ensure_ascii=False, indent=2))
        self.finish()
