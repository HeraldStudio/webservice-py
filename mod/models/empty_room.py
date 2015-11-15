#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-13 13:33:33
# @Author  : yml_bright@163.com

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import engine, Base

class CourseInfo(Base):
    __tablename__ = 'course_info'
    course_id = Column(String(30), primary_key=True)    # 课程ID，人为构成
    course_term = Column(String(30))                    # 课程学期
    course_name = Column(String(255))                   # 课程名
    course_for_student = Column(String(20))             # 开课对象的年级
    course_teacher = Column(String(100))                # 开课老师

class CourseSchedule(Base):
    __tablename__ = 'course_schedule'
    course_id = Column(ForeignKey(u'course_info.course_id'), primary_key=True)    # 课程ID
    course_start_week = Column(Integer, index=True)       # 第几周开始
    course_end_week = Column(Integer, index=True)         # 第几周结束
    course_date = Column(Integer, index=True, primary_key=True)             # 周几
    course_start_lesson = Column(Integer, index=True, primary_key=True)     # 第几节开始
    course_end_lesson = Column(Integer, index=True, primary_key=True)       # 第几节结束
    course_type = Column(Integer, index=True, primary_key=True)                               # 单双周，0-全，1-单，2-双
    course_place = Column(String(255))                          # 上课地点

class ExamSchedule(Base):
    __tablename__ = 'exam_schedule'
    exam_term = Column(String(100), index=True, primary_key=True)                 # 考试学期
    exam_campus = Column(String(100), index=True, primary_key=True)               # 考试校区
    exam_place = Column(String(100), index=True, primary_key=True)                # 考试地点
    exam_date = Column(Integer, primary_key=True)                     # 考试日期，格式组织为 YYYY-MM-DD
    exam_time = Column(Integer, primary_key=True)                     # 考试时间，上午（0），下午（1），晚上（2）