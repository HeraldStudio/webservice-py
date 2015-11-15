#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-09 12:11:23
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class LectureCache(Base):
    __tablename__ = 'lecture'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(4096))
    date = Column(Integer, nullable=False)
