#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-03-15 12:44:28
# @Author  : jerry.liangj@qq.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class LibraryHotCache(Base):
    __tablename__ = 'library_hot'
    id = Column(Integer,primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(Integer, nullable=False)

if __name__ == '__main__':
	Base.metadata.create_all(engine)
