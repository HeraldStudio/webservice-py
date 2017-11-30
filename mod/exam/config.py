#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com

CHECK_URL = "http://my.seu.edu.cn/userPasswordValidate.portal"
INDEX_URL = "http://mynew.seu.edu.cn/index.portal"
FIRST_URL = "http://my.seu.edu.cn/index.portal?.pn=p691_p1184"
DETAIL_URL = "http://my.seu.edu.cn/index.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLnYyLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjE0MjJ8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5RXhhbVBsYW5CeVN0dQ__&xnxqSelect=15-16-2"
TIME_OUT = 1000
VERCODE_URL = "http://xk.urp.seu.edu.cn/studentService/getCheckCode"
LOGIN_URL = "http://xk.urp.seu.edu.cn/studentService/system/login.action"
INFO_URL = "http://xk.urp.seu.edu.cn/studentService/cs/stuServe/runQueryExamPlanAction.action"
STANDARD = [
[18.714286, 27.142857, 32.857143, 36.714286, 38.285714, 41.571429, 43.000000, 44.714286, 46.285714, 48.285714, 48.285714, 36.428571, 27.714286, 24.714286, 23.285714, 22.285714, 21.428571, 19.428571, 19.285714, 19.000000, 18.857143, 18.714286, 19.714286, 20.571429, 20.714286, 22.714286, 26.571429, 28.000000, 35.571429, 46.714286, 46.714286, 44.857143, 43.000000, 41.285714, 39.571429, 36.142857, 34.428571, 31.000000, 26.000000, 18.714286],
[0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
[8.333333, 8.333333, 16.166667, 23.166667, 24.166667, 26.000000, 27.000000, 27.833333, 27.500000, 29.000000, 29.500000, 30.333333, 30.000000, 30.000000, 28.666667, 27.666667, 27.333333, 27.833333, 28.000000, 28.333333, 29.833333, 31.333333, 33.333333, 35.166667, 38.000000, 43.000000, 41.833333, 40.833333, 39.666667, 37.666667, 36.833333, 34.500000, 32.333333, 29.500000, 26.500000, 21.500000, 7.333333, 7.166667, 7.166667, 7.333333],
[8.200000, 8.400000, 8.400000, 8.200000, 13.200000, 18.800000, 19.000000, 19.400000, 19.000000, 26.000000, 26.200000, 26.400000, 25.400000, 26.200000, 26.000000, 26.400000, 27.400000, 27.200000, 28.400000, 29.200000, 31.200000, 33.200000, 36.400000, 41.400000, 46.800000, 48.800000, 52.600000, 51.200000, 49.200000, 48.200000, 45.200000, 40.600000, 37.600000, 33.600000, 25.800000, 18.000000, 13.800000, 7.000000, 7.000000, 7.200000],
[17.250000, 19.000000, 20.500000, 21.875000, 24.125000, 25.375000, 26.375000, 28.250000, 28.500000, 28.125000, 28.000000, 27.750000, 25.875000, 25.250000, 25.125000, 26.250000, 25.000000, 24.625000, 25.625000, 24.750000, 24.500000, 24.500000, 25.375000, 24.500000, 52.000000, 52.250000, 52.750000, 52.875000, 53.750000, 55.375000, 55.125000, 55.000000, 54.625000, 18.625000, 18.375000, 18.375000, 18.250000, 17.750000, 17.375000, 9.875000],
[8.428571, 8.285714, 8.142857, 8.285714, 8.428571, 8.285714, 14.000000, 36.285714, 36.142857, 35.857143, 36.000000, 36.000000, 36.142857, 31.714286, 27.000000, 26.857143, 27.714286, 27.571429, 27.714286, 28.714286, 27.857143, 29.142857, 29.714286, 31.000000, 34.142857, 41.000000, 40.142857, 39.285714, 38.000000, 37.857143, 36.428571, 35.000000, 33.571429, 32.000000, 28.428571, 15.714286, 8.285714, 8.285714, 8.285714, 8.142857],
[8.142857, 20.571429, 27.857143, 32.285714, 35.857143, 38.428571, 40.857143, 44.000000, 46.000000, 46.857143, 47.571429, 49.142857, 37.000000, 32.857143, 29.857143, 27.428571, 25.714286, 26.285714, 25.571429, 24.714286, 25.428571, 24.285714, 24.714286, 24.285714, 26.142857, 27.428571, 28.571429, 31.142857, 34.285714, 41.142857, 40.857143, 39.142857, 37.571429, 36.571429, 34.571429, 32.857143, 24.000000, 21.714286, 16.428571, 8.000000],
[8.428571, 8.285714, 8.142857, 8.285714, 8.285714, 8.285714, 16.285714, 16.285714, 19.000000, 21.857143, 24.000000, 25.285714, 25.857143, 27.714286, 29.857143, 31.000000, 32.857143, 34.571429, 35.285714, 32.714286, 30.142857, 29.571429, 29.142857, 28.142857, 27.285714, 27.000000, 26.000000, 26.857143, 26.428571, 26.285714, 26.428571, 26.714286, 25.142857, 24.571429, 23.571429, 21.571429, 20.857143, 18.714286, 17.571429, 17.000000],
[7.500000, 7.500000, 13.833333, 18.833333, 21.333333, 29.666667, 36.500000, 40.333333, 43.333333, 47.166667, 49.833333, 52.833333, 48.666667, 45.833333, 37.500000, 33.500000, 30.833333, 30.000000, 28.000000, 27.500000, 28.666667, 27.666667, 28.500000, 29.166667, 32.833333, 33.833333, 36.000000, 40.333333, 47.666667, 52.166667, 49.166667, 47.166667, 44.166667, 40.666667, 37.166667, 32.500000, 27.000000, 18.833333, 14.833333, 8.000000],
[8.142857, 15.857143, 20.285714, 24.142857, 30.428571, 32.571429, 34.142857, 36.285714, 38.142857, 38.000000, 39.571429, 32.428571, 29.571429, 27.571429, 26.571429, 25.714286, 25.714286, 23.714286, 23.857143, 23.428571, 24.428571, 23.142857, 23.000000, 26.285714, 26.285714, 26.428571, 30.000000, 33.857143, 39.000000, 50.142857, 49.285714, 47.857143, 47.428571, 45.571429, 44.285714, 41.142857, 38.714286, 34.142857, 29.428571, 20.714286]
]

MAX_N = 30
WHITE = 0
BLACK = 255
header = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
        }
