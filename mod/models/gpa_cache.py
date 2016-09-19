#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-19 12:35:45
# @Author  : jerry.liangj@qq.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class GpaCache(Base):
    __tablename__ = 'gpa'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(4096))
    date = Column(Integer, nullable=False)


