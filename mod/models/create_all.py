#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 19:23:24
# @Author  : yml_bright@163.com

import pe_models, pc_cache, jwc_cache, data_cache, lecture_cache, card_cache, nic_cache, phylab_cache,gpa_cache, library, srtp_cache, log
import empty_room, lecturedb, user_detail, library_auth_cache, curriculum_cookie
import room_cache
from db import engine, Base

Base.metadata.create_all(engine)
