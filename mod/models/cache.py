#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Date   : February 24, 2017
@Author : corvo

vim: set ts=4 sw=4 tw=99 et:


此处使用了Python中的cachetools类库, 究其主要原因, 因为本项目中缓存的信息只有用户的cookie
同时作为分布式爬虫的客户端, 没有必要使用mysql来增加对于宿主的要求, 故而使用内存数据库,
为的就是能减少部署的难度与维护难度, 希望接下来维护的同学能够将缓存问题整理清楚


通过阅读cachetools的说明文档, 最终决定使用TTLCache, TTLCache中的TTL为time-to-live,
也就是键值对的存在时间, 同时使用LRU算法, 在整个缓存满了之后, 将会最近最久使用的从cache中清除,
这样选择cache算法, 有一下两个方面原因
  1. 我们无法确定学校使用的cookie是否在一段时间后更换, 如果是的话, 我们需要对cache做及时的清理
  2. 作为部署在多个服务器上的应用, 需要对于原宿主机性能资源进行保护,
      不能因为简单的爬虫就将宿主机性能完全占用, 因此对最大容量进行限制
  3. 由于配置很简单, 暂时将配置信息直接写入在该文件中, 如要进行整理可以将配置信息进行迁移
"""

from cachetools import TTLCache

cache = TTLCache(maxsize = 500, ttl = 3600)
