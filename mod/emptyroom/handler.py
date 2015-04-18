#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-13 13:49:23
# @Author  : yml_bright@163.com

import json
import tornado.web
from datetime import date, timedelta
from utils import filter_common, filter_quick, get_free_classrooms

class CommonQueryHandler(tornado.web.RequestHandler):

    def get(self, campus, week, date, start_lesson, end_lesson):
        # filter paramter
        filter_result = filter_common(campus, week, date, start_lesson, end_lesson)

        if filter_result is None:
            self.write(json.dumps(['BAD_PARAMETER'], ensure_ascii=False))
        else:
            # access db
            result = get_free_classrooms(
                filter_result[0], filter_result[1], filter_result[2], filter_result[3], filter_result[4])
            self.write(json.dumps(result, ensure_ascii=False))

        self.finish()

class QuickQueryHandler(tornado.web.RequestHandler):

    def get(self, campus, today_or_tomorrow, start_lesson, end_lesson):
        filter_result = filter_quick(
            campus, today_or_tomorrow, start_lesson, end_lesson)

        if filter_result is None:
            self.write(json.dumps(['BAD_PARAMETER'], ensure_ascii=False))
        else:
            # access db
            result = get_free_classrooms(
                filter_result[0], filter_result[1], filter_result[2], filter_result[3], filter_result[4])
            
            self.write(json.dumps(result, ensure_ascii=False))

        self.finish()
