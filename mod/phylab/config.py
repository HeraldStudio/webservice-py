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
        '__EVENTVALIDATION':'/GGwHYctwrDsGO0QxbIVz5tZgB1mjzgw1d9ViogDCBBJ3aqZnAlIZ2x+397w3Cj4uik18Vf+rYKUveDJS5dL205I28CZxZg3zeG/7xldnNAvDm5CWbwIV4/tRwAJU/fbaHhCtL6JEsItYdEqRM+eFsex8DrZEQ8OT0VQp46KVbr2Zfhxm9elmBKO0/I7DfTf'
    }
