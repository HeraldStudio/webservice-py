#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Date   : December 09, 2016
@Author : corvo

vim: set ts=4 sw=4 tw=99 et:
"""


import json
import tornado.web
from mod.models.log import DayLogAnalyze

class LogHandler(tornado.web.RequestHandler):
    """
        本模块为日志分析后端模块, 预先分析好的日志先存储于数据库中,
        使用时读取数据库中的json信息, 做简单处理后返回
    """
    def get(self):
        self.write('herald webservice')

    def post(self):
        retjson = {'code': '200', 'content': 'None'}

        date_start = self.get_argument('date_start', default='unsolved')
        date_cnt = int(self.get_argument('date_cnt', default='1'))

        content = []
        try:
            log_list = self.db.query(DayLogAnalyze).\
                    order_by(DayLogAnalyze.date).\
                    filter(DayLogAnalyze.date >= date_start).\
                    limit(date_cnt).all()

            if log_list:
                for i in range(date_cnt):
                    content_item = dict()
                    log = log_list[i]
                    content_item['date'] = eval(log.date)
                    content_item['every_hour_count'] = eval(log.every_hour_count)
                    content_item['api_order'] = eval(log.api_order)
                    content_item['device_distribute'] = eval(log.device_distribute)
                    content_item['call_count'] = log.call_count
                    content_item['ios_version'] = eval(log.ios_version)
                    content_item['android_version'] = eval(log.android_version)

                    content.append(content_item)

        except Exception as e:
            retjson['code'] = 500
            retjson['content'] = 'error'
            print e

        retjson['code'] = 200
        retjson['content'] = content
        self.write(json.dumps(retjson, indent=2, ensure_ascii=False))
