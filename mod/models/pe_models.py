# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 16:32:45
# @Author  : xindervella@gamil.com yml_bright@163.com

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class PEUser(Base):
    __tablename__ = 'pe'
    cardnum = Column(Integer, primary_key=True)
    count = Column(String(10), nullable=False)

    def __repr__(self):
        return '<PE (%s, %d)' % (self.cardnum, self.count)

class PeDetailCache(Base):
    __tablename__ = 'pedetail'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(2048))
    date = Column(Integer, nullable=False)