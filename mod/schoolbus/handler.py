#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-15 18:07:58
# @Author  : yml_bright@163.com

import tornado.web
from ..models.data_cache import DataCache
from sqlalchemy.orm.exc import NoResultFound
import json, base64

class SchoolBusHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.init_db()
        #self.write('Herald Web Service')

    def post(self):
        try:
            data = self.db.query(DataCache).filter( DataCache.key == 10001 ).one()
            self.write(base64.b64decode(data.data))
            self.db.close()
            self.finish()
        except:
            retjson = {'code':500, 'content':'error'}
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()

    def init_db(self):
        bus_json = {
            "weekend":{
                "出九龙湖":[
                    { "time":"8:00-9:30", "bus":"每 30min 一班"},
                    { "time":"9:30-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 30min 一班"},
                    { "time":"13:00-17:00", "bus":"每 1h 一班"},
                    { "time":"17:00-18:30", "bus":"每 30min 一班"},
                    { "time":"18:30-22:00", "bus":"每 1h 一班"}
                ],
                "进九龙湖":[
                    { "time":"8:00-9:30", "bus":"每 30min 一班"},
                    { "time":"9:30-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 30min 一班"},
                    { "time":"13:00-17:00", "bus":"每 1h 一班" },
                    { "time":"17:00-18:30", "bus":"每 30min 一班"},
                    { "time":"18:30-22:00", "bus":"每 1h 一班"}
                ]
            },
            "weekday":{
                "出九龙湖":[
                    { "time":"7:20-9:00", "bus":"每 5min 一班"},
                    { "time":"9:00-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 5min 一班"},
                    { "time":"13:00-17:00", "bus":"每 1h 一班"},
                    { "time":"17:00-18:30", "bus":"每 5min 一班"},
                    { "time":"18:30-22:00", "bus":"每 1h 一班"}
                ],
                "进九龙湖":[
                    { "time":"7:20-9:00", "bus":"每 5min 一班"},
                    { "time":"9:00-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 5min 一班"},
                    { "time":"13:00-17:00", "bus":"每 1h 一班"},
                    { "time":"17:00-18:30", "bus":"每 5min 一班"},
                    { "time":"18:30-22:00", "bus":"每 1h 一班"}
                ]
            }

        }
        retjson = {'code': 200, 'content': bus_json}
        try:
            data = self.db.query(DataCache).filter( DataCache.key == 10001 ).one()
            data.data = base64.b64encode(json.dumps(retjson, ensure_ascii=False, indent=2))
        except NoResultFound:
            data = DataCache(key=10001, data=base64.b64encode(json.dumps(retjson, ensure_ascii=False, indent=2)))
        self.db.add(data)
        self.db.commit()


