# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:37:23
# @Author  : xindervella@gamil.com yml_bright@163.com

DB_HOST = '192.168.56.1'
DB_USER = 'herald'
DB_PWD = '******'
DB_NAME = 'herald_webservice'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                       (DB_USER, DB_PWD, DB_HOST, DB_NAME), echo=False,pool_size=500, pool_recycle=100)
