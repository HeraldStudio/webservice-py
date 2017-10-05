from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class LibraryAuthCache(Base):
    __tablename__ = 'library_auth'
    cardnum = Column(Integer, primary_key=True)
    cookie = Column(String(4096))
    date = Column(Integer, nullable=False)
