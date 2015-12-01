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


submit = '登  陆'.encode('utf-8')
header = { 
            'Cache-Control': 'no-cache',
            'Origin': 'http://phylab.seu.edu.cn',
            'X-MicrosoftAjax': 'Delta=true',
            'Cookie':'',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': 'http://phylab.seu.edu.cn/plms/Default.aspx',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'
    }

loginValues = {
            'ctl00$cphSltMain$UserLogin1$txbUserCodeID':'',
            'ctl00$ScriptManager1':'UpdatePanel3|UserLogin1$btnLogin',
            'ctl00$cphSltMain$UserLogin1$rblUserType':'Stu',
            'ctl00$cphSltMain$UserLogin1$txbUserPwd':'',
            'ctl00$cphSltMain$UserLogin1$btnLogin':submit,
            '__ASYNCPOST':'true',
            # '__EVENTTARGET':'',   
            # '__EVENTARGUMENT':'', 
            # '__LASTFOCUS':'', 
            '__EVENTVALIDATION':'/wEWBwKGsL2fBwKGz+fmBQLWi8GnBALIoPqxBgL6uOCYDALS7JivDAKPku6gDn4V6JOPV7iOvuUcMu3JdF0=',       
            '__VIEWSTATE':'/wEPDwUKLTQ4NDQyNDg4Nw9kFgJmD2QWAgIDD2QWBAIHD2QWAgIBD2QWAmYPZBYCAgEPZBYCAgQPZBYEAgEPEGRkFgFmZAIDDw8WAh4EVGV4dAUM5Y2h44CA5Y+377yaZGQCCQ9kFgICAg88KwAJAQAPFgQeCERhdGFLZXlzFgAeC18hSXRlbUNvdW50AgFkFgJmD2QWAgIBDw8WAh8ABZMB5a2m5Lmg6L+H56iL5Lit77yM5ZCM5a2m5Lus5aaC5pyJ6Zeu6aKY6ZyA5LiO5a6e6aqM5Lit5b+D5oiW5Lu76K++5pWZ5biI6IGU57O777yM6K+35LuO6aaW6aG16L+b5YWl4oCc55WZ6KiA5p2/4oCd55WZ6KiA77yM5oiR5Lus5Lya5Y+K5pe25YWz5rOo44CCZGRkz8TvwOD53muTMh900O1MzQ==',
}

selectData = {
        'ctl00$ScriptManager1' : 'ctl00$cphSltMain$UpdatePanel1|ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTTARGET' :  'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS' :'',
        '__VIEWSTATE':'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',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp':'',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseScoreType$ddlCourseScoreType' :'1',
        '__VIEWSTATEENCRYPTED':'',
        '__ASYNCPOST':'true',
        '__EVENTVALIDATION':'3Sl67R6jLfq1L9LlabZ97xOrP2RuqKfKvLmNaQYd8VHeaAonq8R8W9LTDjALASske9lUke0jqUxU4L2e39YHKFyzIS9dvij9sYIc6jPTczBhY6Klq91SiC2nGc7Rakl4AC5Cx2qZSH1hbLXcyaVfJcODhkeEjDCtU1oLsFMvrUN3rAqzlzGfhu2RjhZrZsbU'
    }
