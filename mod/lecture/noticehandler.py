#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-17 12:06:02
# @Author  : yml_bright@163.com

from config import *
from ..models.lecturedb import LectureDB
from sqlalchemy.orm.exc import NoResultFound
from time import time, strftime, mktime, localtime, strptime
import tornado.web
import tornado.gen
import json, base64

class LectureNoticeHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def post(self):
        retjson = {'code':500, 'content':u'暂无'}
        date = mktime(strptime(strftime('%Y-%m-%d' ,localtime(time())), '%Y-%m-%d'))

        # read from db
        try:
            status = self.db.query(LectureDB).filter( LectureDB.date >=  date ).all()
            if len(status) > 0:
                ret = []
                for l in status:
                    ret.append({
                        'date': l.time,
                        'topic': l.topic,
                        'speaker': l.speaker,
                        'location': l.location,
                        'detail': l.detail
                        })
                retjson['code'] = 200
                retjson['content'] = ret
        except NoResultFound:
            pass

        
        retjson = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(retjson)
        self.finish()
        self.db.close()

