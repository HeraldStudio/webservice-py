#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-12 20:19:05
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class JWCCache(Base):
    __tablename__ = 'jwc'
    date = Column(Integer, primary_key=True)
    text = Column(String(10240), nullable=False)