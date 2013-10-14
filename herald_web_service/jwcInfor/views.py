# -*- coding:utf-8 -*-
import json
import urllib
from BeautifulSoup import BeautifulSoup
import datetime
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

from jwcInfor.models import Info, Attachment


def setJwcInfo():
    baseUrl = 'http://jwc.seu.edu.cn'

    uFile = urllib.urlopen('http://jwc.seu.edu.cn/')
    html = uFile.read().decode('utf-8')

    soup = BeautifulSoup(html)

    target = soup.findAll('a', {'target': '_blank', 'class': 'font3'})[5:-4]
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
        contentList = pageSoup.findAll('p')
        linkList = pageSoup.findAll('a', {'id': True, 'target': '_blank'})

        # print title
        # print uplodeDate
        # print channel
        content = ''
        uplodeDate = datetime.datetime.strptime(uplodeDate, "%Y-%m-%d").date()
        if Info.objects.filter(title=title, time=uplodeDate):
            continue
        else:
            for i in contentList:
                sentence = i.text.replace(u'&nbsp;', '')
                if len(sentence) > 5:
                    if sentence[-4] != u'.' and sentence[-5] != u'.':
                        content += sentence +'\n'
                else:
                    content += sentence + '\n'
            info = Info.objects.create(title=title, time=uplodeDate, channel=channel, content=content)
            for i in linkList:
                Attachment.objects.create(info_id=info.id, title=i.text, link=baseUrl+i['href'])


def getJwcInfo(request):
    try:
        setJwcInfo()
    except:
        pass
    infoList = Info.objects.order_by('-time', '-id')[:5]
    info = []
    attachment = []
    for i in infoList:
        # attachmentList = Attachment.objects.filter(info_id=i.id)
        # for j in attachmentList:
        #     attachment.append([j.title, j.link])
        info.append([i.id,  i.channel, i.title, str(i.time)])
        # attachment = []
        # info.append(i.id)
    return HttpResponse(json.dumps(info, ensure_ascii=False))

def getMoreInfo(request, offset):
    incomming = Info.objects.get(id=offset)
    allInfo = Info.objects.order_by('-time', '-id').filter(time__lte=incomming.time)
    flag = 0
    infoList = []
    for i in allInfo:
        if flag > 0 and flag <=5:
            infoList.append(i)
            flag += 1
        if i == incomming:
            flag = 1
    print infoList
    info = []
    attachment = []
    for i in infoList:
        # attachmentList = Attachment.objects.filter(info_id=i.id)
        # for j in attachmentList:
        #     attachment.append([j.title, j.link])
        info.append([i.id, i.channel, i.title, str(i.time)])
        # attachment = []
        # info.append(i.id)
    return HttpResponse(json.dumps(info, ensure_ascii=False))

def getDetaile(request, offset):
    info = Info.objects.filter(id=int(offset)).get()
    detail = [info.id, info.channel, info.title, str(info.time), info.content]
    attachmentList = Attachment.objects.filter(info_id=info.id)
    attachment = []
    for i in attachmentList:
        attachment.append([i.title, i.link])
    detail.append(attachment)
    return  HttpResponse(json.dumps(detail, ensure_ascii=False))
