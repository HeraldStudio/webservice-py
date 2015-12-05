#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-08 12:46:36
# @Author  : yml_bright@163.com

LOGIN_URL = "http://phylab.seu.edu.cn/plms/UserLogin.aspx?ReturnUrl=%2fplms%2fSelectLabSys%2fDefault.aspx"
phyLabCurUrl = "http://phylab.seu.edu.cn/plms/SelectLabSys/StuViewCourse.aspx"
SELECTURL = "http://phylab.seu.edu.cn/plms/SelectLabSys/StuViewCourse.aspx"
   
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
}

selectData = {
        'ctl00$ScriptManager1' : 'ctl00$cphSltMain$UpdatePanel1|ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTTARGET' :  'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS' :'',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseGroup$ddlCgp':'',
        'ctl00$cphSltMain$ShowAStudentScore1$ucDdlCourseScoreType$ddlCourseScoreType' :'1',
        '__VIEWSTATEENCRYPTED':'',
        '__ASYNCPOST':'true',
    }
