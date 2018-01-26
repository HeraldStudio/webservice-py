#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 19:23:24
# @Author  : yml_bright@163.com

import pe_models
import pc_cache
import jwc_cache
import data_cache
import lecture_cache
import card_cache
import nic_cache
import phylab_cache
import gpa_cache
import library
import srtp_cache
import log
import empty_room
import lecturedb
import user_detail
import library_auth_cache
import curriculum_cookie
import room_cache
import exam_cache
from db import engine, Base

Base.metadata.create_all(engine)
