# -*- coding: utf-8 -*-
# @Date    : 2016/9/20  21:35
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer
from db import engine, Base

class ListLibrary(Base):
    __tablename__ = 'library_cache'
    cardnum = Column(Integer, primary_key=True)
    text = Column(String(2048))
    date = Column(Integer, nullable=False)

if __name__ == '__main__':
	Base.metadata.create_all(engine)