#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-09 12:35:45
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT, BIGINT
from db import engine, Base

class CardCache(Base):
    __tablename__ = 'card'
    cardnum = Column(BIGINT, primary_key=True)
    text = Column(LONGTEXT)
    date = Column(Integer, nullable=False)


