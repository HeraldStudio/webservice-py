# -*- coding: utf-8 -*-

import tornado.web
import tornado.gen
from tornado.httpclient import *
import json

class NewSchoolBusHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        try:
            client = AsyncHTTPClient()
            request = HTTPRequest('http://121.248.63.119/busservice/lines')
            response = yield tornado.gen.Task(client.fetch, request)
            lines = json.loads(response.body)['data']['lines']

            for line in lines:
                line_id = line['id']
                request = HTTPRequest('http://121.248.63.119/busservice/queryBus?lineId=' + str(line_id))
                response = yield tornado.gen.Task(client.fetch, request)
                buses = json.loads(response.body)
                line['buses'] = buses['data']['buses']
                
                request = HTTPRequest('http://121.248.63.119/busservice/lineDetail?lineId=' + str(line_id))
                response = yield tornado.gen.Task(client.fetch, request)
                detail = json.loads(response.body)
                line['stops'] = detail['data']['line']['linePoints']
                
            self.write(json.dumps({ 'code': 200, 'content': lines }, ensure_ascii=False))
        except:
            self.write(json.dumps({ 'code': 400, 'content': [] }, ensure_ascii=False))
        self.finish()