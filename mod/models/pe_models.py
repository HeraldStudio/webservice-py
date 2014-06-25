# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 16:32:45
# @Author  : xindervella@gamil.com
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base()


class PEUser(Base):
    __tablename__ = 'pe'
    cardnum = Column(String(10), primary_key=True)
    count = Column(String(10), nullable=False)

    def __repr__(self):
        return '<PE (%s, %d)' % (self.cardnum, self.count)


def create_all():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_all()
