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
            'weekday' : {
                '进九龙湖' : [
                    {'time': '06:50', 'bus': '2辆九江线、3辆九河直、3辆九河B'},
                    {'time': '07:50', 'bus': '1辆九桥线'},
                    {'time': '08:00', 'bus': '2辆九江线、7辆(周一+1)九河直、7辆(周一+1)九河B'},
                    {'time': '08:30', 'bus': '3辆九河直、3辆九河B'},
                    {'time': '09:30', 'bus': '1辆九河B'},
                    {'time': '13:00', 'bus': '3辆九河直、3辆九河B'},
                    {'time': '14:30', 'bus': '1辆九河B'},
                    {'time': '17:00', 'bus': '1辆九河B'},
                    {'time': '17:30', 'bus': '1辆九河B'},
                    {'time': '19:00', 'bus': '1辆九河B'},
                ],
                '出九龙湖' : [
                    {'time': '08:15', 'bus': '1辆九河B'},
                    {'time': '09:50', 'bus': '2辆九河直、2辆九河B'},
                    {'time': '10:50', 'bus': '2辆九河直、2辆九河B'},
                    {'time': '11:45', 'bus': '3辆九河直、3辆九河B、3辆九江线'},
                    {'time': '13:00', 'bus': '3辆九河直、3辆九河B'},
                    {'time': '15:50', 'bus': '3辆九河直、3辆九河B'},
                    {'time': '17:00', 'bus': '9辆（周一+1）九河直、9辆（周一+1）九河B、9辆（周一+1）九江线、9辆（周一+1）九桥线'},
                    {'time': '17:40', 'bus': '1辆九河B'},
                    {'time': '18:30', 'bus': '1辆九河B'},
                    {'time': '21:30', 'bus': '1辆九河B'},
                ],
            },
            'weekend' : {
                '进九龙湖' : [
                    {'time': '08:00', 'bus': '2辆九河直、2辆九河B'},
                    {'time': '09:00', 'bus': '1辆九河B'},
                    {'time': '10:00', 'bus': '1辆九河直'},
                    {'time': '13:00', 'bus': '1辆九河B'},
                    {'time': '15:00', 'bus': '1辆九河直'},
                    {'time': '17:00', 'bus': '1辆九河直'},
                    {'time': '19:00', 'bus': '1辆九河直'},
                ],
                '出九龙湖' : [
                    {'time': '09:00', 'bus': '1辆九河直'},
                    {'time': '10:00', 'bus': '1辆九河直'},
                    {'time': '13:00', 'bus': '1辆九河B'},
                    {'time': '17:00', 'bus': '2辆九河直、2辆九河B'},
                    {'time': '18:00', 'bus': '1辆九河直'},
                    {'time': '20:00', 'bus': '1辆九河直'},
                ],
            },
        }
        retjson = {'code': 200, 'content': bus_json}
        try:
            data = self.db.query(DataCache).filter( DataCache.key == 10001 ).one()
            data.data = base64.b64encode(json.dumps(retjson, ensure_ascii=False, indent=2))
        except NoResultFound:
            data = DataCache(key=10001, data=base64.b64encode(json.dumps(retjson, ensure_ascii=False, indent=2)))
        self.db.add(data)
        self.db.commit()


