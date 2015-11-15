#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-15 18:38:57
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class DataCache(Base):
    __tablename__ = 'data'
    key = Column(Integer, primary_key=True)
    data = Column(String(10240), nullable=False)

