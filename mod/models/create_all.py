#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 19:23:24
# @Author  : yml_bright@163.com

import pe_models, pc_cache, jwc_cache
from db import engine, Base

Base.metadata.create_all(engine)
