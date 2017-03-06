# -*- coding: utf-8 -*-
# @Date    : 2016/9/19  9:31
# @Author  : 490949611@qq.com

from sqlalchemy import Column, String, Integer
from db import engine, Base

class PEDetail(Base):
    __tablename__ = 'pedetail'
    cardnum = Column(Integer, primary_key=True)
    content = Column(String(4096), nullable=False)
