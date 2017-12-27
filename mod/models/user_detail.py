#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : user_detail.py
# Author            : higuoxing <higuoxing@outlook.com>
# Date              : 27.12.2017
# Last Modified Date: 27.12.2017
# Last Modified By  : higuoxing <higuoxing@outlook.com>
# -*- coding: utf-8 -*-
# @Date    : 2015-03-19 16:50:22
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT
from db import engine, Base

class UserDetail(Base):
    __tablename__ = 'user_detail'
    cardnum = Column(String(10), primary_key=True)
    schoolnum = Column(String(10), nullable=True)
    name = Column(String(50), nullable=False)
    sex = Column(String(10), nullable=True)
    nation = Column(String(50), nullable=True)
    room = Column(String(50), nullable=True)
    bed = Column(String(50), nullable=True)
    last_update = Column(BIGINT, nullable=True)
