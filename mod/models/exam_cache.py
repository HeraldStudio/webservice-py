#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base()

class ExamCache(Base):
    __tablename__ = 'exam'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(Integer, nullable=False)


if __name__ == '__main__':
	Base.metadata.create_all(engine)