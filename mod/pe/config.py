#-*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:34:57
## @Author  : yml_bright@163.com


PE_LOGIN_URL = "http://223.3.65.228/student/studentFrame.jsp"
PE_PC_URL = "http://223.3.65.228/student/queryCheckInfo.jsp"

CONNECT_TIME_OUT = 3

API_SERVER_HOST = '223.3.65.228'
API_SERVER_PORT = 10086
API_SERVER_KEY = '1d10fbf11874589e0'

SECRET_KEY1 = 180847167
SECRET_KEY2 = 2366060863
A = hex(SECRET_KEY1^SECRET_KEY2)[2:] + API_SERVER_KEY + hex(SECRET_KEY1)[2:]
daymap = {'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':7}
finay_day = '2018-01-12'
final_date = 5
loginurl1 = "http://ids2.seu.edu.cn/amserver/UI/Login"
runurl = "http://zccx.seu.edu.cn"
