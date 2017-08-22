# -*- coding: utf-8 -*-

import tornado.web
import tornado.gen
from tornado.httpclient import *
import json

class NewSchoolBusHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        client = AsyncHTTPClient()
        request = HTTPRequest('http://121.248.63.119/busservice/lines')
        response = yield tornado.gen.Task(client.fetch, request)
        lines = json.loads(response.body)
        lines['code'] = 200
        for line in lines['data']['lines']:
            line_id = line['id']
            request = HTTPRequest('http://121.248.63.119/busservice/queryBus?lineId=' + str(line_id))
            response = yield tornado.gen.Task(client.fetch, request)
            buses = json.loads(response.body)
            line['buses'] = buses['data']['buses']
            
            request = HTTPRequest('http://121.248.63.119/busservice/lineDetail?lineId=' + str(line_id))
            response = yield tornado.gen.Task(client.fetch, request)
            detail = json.loads(response.body)
            line['stops'] = detail['data']['line']['linePoints']
            
        self.write(json.dumps(lines, ensure_ascii=False))
        self.finish()