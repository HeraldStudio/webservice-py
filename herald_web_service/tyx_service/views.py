# -*- coding: utf-8 -*-
import cookielib
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from django.http import HttpResponse


def tyxPc(request, cardNumber, password):
    loginUrl = 'http://58.192.114.239:8088/sms2/studentLogin.do'
    data = {
        'xh': str(cardNumber),
        'mm': str(password),
        'method': 'login'
    }
    loadUrl = 'http://58.192.114.239:8088/sms2/studentQueryListChecks.do?method=listChecks'
    cookieJar = cookielib.CookieJar()
    cookieHandler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookieHandler)
    urllib2.install_opener(opener)

    reqLogin = urllib2.Request(loginUrl, urllib.urlencode(data))
    resLogin = urllib2.urlopen(reqLogin)
    html = resLogin.read()
    if len(html) == 524:
        reqLoad = urllib2.Request(loadUrl)
        resLoad = urllib2.urlopen(reqLoad)
        html = resLoad.read()
        soup = BeautifulSoup(html)
        table = soup.findAll("td", {"class": "Content_Form"})
        try:
            pc = table[-1].text
        except:
            pc = '出错了'
    else:
        pc = '一卡通/密码不正确'
    return HttpResponse(pc)