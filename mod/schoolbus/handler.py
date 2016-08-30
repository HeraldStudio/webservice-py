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
                "前往地铁站":[
                    { "time":"8:00-9:30", "bus":"每 30min 一班"},
                    { "time":"9:30-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 30min 一班"},
                    { "time":"13:30-17:00", "bus":"每 1h 一班(最后一班为17:00)"},
                    { "time":"17:00-19:00", "bus":"每 30min 一班"},
                    { "time":"19:00-22:00", "bus":"每 1h 一班"}
                ],
                "返回九龙湖":[
                    { "time":"8:00-9:30", "bus":"每 30min 一班"},
                    { "time":"9:30-11:30", "bus":"每 1h 一班"},
                    { "time":"11:30-13:00", "bus":"每 30min 一班"},
                    { "time":"13:30-17:00", "bus":"每 1h 一班(最后一班为17:00)"},
                    { "time":"17:00-19:00", "bus":"每 30min 一班"},
                    { "time":"19:00-22:00", "bus":"每 1h 一班"}
                ]
            },
            "weekday":{
                "前往地铁站":[
                    { "time":"7:10-10:00", "bus":"每 10min 一班"},
                    { "time":"10:00-11:30", "bus":"每 30min 一班"},
                    { "time":"11:30-13:30", "bus":"每 10min 一班"},
                    { "time":"13:30-15:00", "bus":"13:30,14:00"},
                    { "time":"15:00-15:50", "bus":"每 10min 一班"},
                    { "time":"16:00-17:00", "bus":"16:00"},
                    { "time":"17:00-18:30", "bus":"每 10min 一班"},
                    { "time":"18:30-22:00", "bus":"每 30min 一班(20:30没有班车)"}
                ],
                "返回九龙湖":[
                    { "time":"7:10-10:00", "bus":"每 10min 一班"},
                    { "time":"10:00-11:30", "bus":"每 30min 一班"},
                    { "time":"11:30-13:30", "bus":"每 10min 一班"},
                    { "time":"13:30-15:00", "bus":"13:30,14:00"},
                    { "time":"15:00-15:50", "bus":"每 10min 一班"},
                    { "time":"16:00-17:00", "bus":"16:00"},
                    { "time":"17:00-18:30", "bus":"每 10min 一班"},
                    { "time":"18:30-22:00", "bus":"每 30min 一班(20:30没有班车)"}
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


