#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-08 12:46:36
# @Author  : yml_bright@163.com

LOGIN_URL = "http://phylab.seu.edu.cn/plms/UserLogin.aspx?ReturnUrl=%2fplms%2fSelectLabSys%2fDefault.aspx"
phyLabCurUrl = "http://phylab.seu.edu.cn/plms/SelectLabSys/StuViewCourse.aspx"
   
TIME_OUT = 7

cur_type_up = {
    3:'基础性实验(上)',
    7:'基础性实验(上)选做',
    2:'文科及医学实验',
    9:'文科及医学实验选做'
}
cur_type_down = {
            5:'基础性实验(下)',
            6:'基础性实验(下)选做',
            2:'文科及医学实验',
            9:'文科及医学实验选做'
        }


submit = '登录'.encode('utf-8')
header = { 
            'Cache-Control': 'no-cache',
            'Origin': 'http://phylab.seu.edu.cn',
            'X-MicrosoftAjax': 'Delta=true',
            'Cookie':'',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': 'http://phylab.seu.edu.cn/plms/UserLogin.aspx?ReturnUrl=%%2fplms%%2fSelectLabSys%%2fDefault.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'
    }

loginValues = {
            'ctl00$cphSltMain$UserLogin1$txbUserCodeID':'',
            'ctl00$cphSltMain$UserLogin1$rblUserType':'Stu',
            'ctl00$cphSltMain$UserLogin1$txbUserPwd':'',
            'ctl00$cphSltMain$UserLogin1$btnLogin':submit,
            'ctl00$ScriptManager1':'ctl00$cphSltMain$UpdatePanel1|ctl00$cphSltMain$UserLogin1$btnLogin',
            '__EVENTTARGET':'',   
            '__EVENTARGUMENT':'', 
            '__LASTFOCUS':'', 
            '__VIEWSTATE':'/wEPDwUKLTQ4NDQyNDg4Nw9kFgJmD2QWAgIDD2QWBAIHD2QWAgIBD2QWAmYPZBYCAgEPZBYCAgQPZBYEAgEPEGRkFgFmZAIDDw8WAh4EVGV4dAUM5Y2h44CA5Y+377yaZGQCCQ9kFgICAg88KwAJAQAPFgQeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AgFkFgJmD2QWAgIBDw8WAh8ABZMB5a2m5Lmg6L+H56iL5Lit77yM5ZCM5a2m5Lus5aaC5pyJ6Zeu6aKY6ZyA5LiO5a6e6aqM5Lit5b+D5oiW5Lu76K++5pWZ5biI6IGU57O777yM6K+35LuO6aaW6aG16L+b5YWl4oCc55WZ6KiA5p2/4oCd55WZ6KiA77yM5oiR5Lus5Lya5Y+K5pe25YWz5rOo44CCZGRkKxkEVLSbsP4Q89+B39eC0gAAAAA=',
            '__EVENTVALIDATION':'/wEWBwKR4pj0BwKGz+fmBQLWi8GnBALIoPqxBgL6uOCYDALS7JivDAKPku6gDmbTgOYVut4URau4qec7eVYAAAAA'         
}


selectData = {
        'ctl00$ScriptManager1' :   'ctl00$cphSltMain$UpdatePanel1|ctl00$cphSltMain'
            +'$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTTARGET' :  'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS' :'',
        '__VIEWSTATE' :'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',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp':'',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseScoreType$ddlCourseScoreType' :'1',
        '__VIEWSTATEENCRYPTED':'',
        '__EVENTVALIDATION':'pB2B2AGcCuTzb+i3ke/6YcGLf3NvRiYKu4EZb0XMemTuJoXhXmDBmPFEGPSb7LT0om99tfogx'+
            'cLcTGcYqi8RAbmZCDDImlig7X99WAOlswdWmarZVDNWpNzrpYBfBaHpRmpX96k8tcSv8TQrthBwxmjbzcOuhnImUGj'+
            'REU7bnjSsLcv5QMkUc8UbkFeKlg8q'
    }