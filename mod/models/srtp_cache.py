# -*- coding: utf-8 -*-
# @Date    : 2016/9/20  23:23
# @Author  : 490949611@qq.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class SRTPCache(Base):
    __tablename__ = 'srtp_cache'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(Integer, nullable=False)

if __name__ == '__main__':
	Base.metadata.create_all(engine)