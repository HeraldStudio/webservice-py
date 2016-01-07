#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com

CHECK_URL = "http://my.seu.edu.cn/userPasswordValidate.portal"
INDEX_URL = "http://mynew.seu.edu.cn/index.portal"
FIRST_URL = "http://my.seu.edu.cn/index.portal?.pn=p691_p1184"
DETAIL_URL = "http://my.seu.edu.cn/index.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLnYyLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjE0MjJ8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5RXhhbVBsYW5CeVN0dQ__&xnxqSelect=15-16-2"
TIME_OUT = 4

header = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
        }