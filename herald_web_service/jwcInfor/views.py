# -*- coding:utf-8 -*-
import json
import urllib
from BeautifulSoup import BeautifulSoup
from django.http import HttpResponse


def getJwcInfor(request):
    baseUrl = 'http://jwc.seu.edu.cn'

    uFile = urllib.urlopen('http://jwc.seu.edu.cn/')
    html = uFile.read().decode('utf-8')

    soup = BeautifulSoup(html)

    target = soup.findAll('a', {'target': '_blank', 'class': 'font3'})[5:-4]

    inforList = []
    for i in target:
        if i in target[:7]:
            channel = u'教务信息'
        elif i in target[7:14]:
            channel = u'学籍管理'
        elif i in target[14:21]:
            channel = u'实践教学'
        elif i in target[21:25]:
            channel = u'合作办学'
        elif i in target[25:29]:
            channel = u'教学研究'
        else:
            channel = u'教学评估'
        relUrl = i['href']
        page = urllib.urlopen(baseUrl + relUrl)
        pageHtml = page.read().decode('utf-8')
        pageSoup = BeautifulSoup(pageHtml)
        title = pageSoup.find('td', {'bgcolor': '#E6E6E6'}).text
        uplodeDate = pageSoup.find('td',  {'align': 'right'}).text[5:]
        linkList = pageSoup.findAll('a', {'id': True, 'target': '_blank'})
        attachmentList = []
        for i in linkList:
            link = baseUrl + i['href']
            name = i.text
            attachmentList.append([name, link])

        inforList.append([uplodeDate, channel, title, attachmentList])
    return HttpResponse(json.dumps(sorted(inforList, key=lambda uplodeDate: uplodeDate[0], reverse=True), ensure_ascii=False), mimetype='application/json')
