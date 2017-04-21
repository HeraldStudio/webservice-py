# -*- coding: utf-8 -*-
# @Date    : 2017/4/21  21:10
# @Author  : higuoxing@outlook.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class SrtpProjCache(Base):
    __tablename__ = 'srtp_proj_cache'
    cardnum = Column(String(16), primary_key=True)
    text = Column(String(4096), nullable=False)
    date = Column(Integer, nullable=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
