#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 19:29:24
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class PCCache(Base):
    __tablename__ = 'pc'
    date = Column(Integer, primary_key=True)
    text = Column(String(1023), nullable=False)
    lastdate = Column(Integer)

