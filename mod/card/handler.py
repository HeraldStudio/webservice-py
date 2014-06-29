# -*- coding: utf-8 -*-
from config import CARD_HOME_URL, CARD_LOGIN_URL, CARD_VERIFY_URL, CARD_PWD_URL, CARD_DETIAL_URL, CARD_PAGE_URL, CARD_REMAIN_URL, STAND, BOX, CONNECT_TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import cStringIO, urllib, urllib2, Image
import json
import datetime,time


class CARDHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)
        password = self.get_argument('password', default=None)
        timedelta = self.get_argument('timedelta', default=0)    #留空只查询余额

        client = AsyncHTTPClient()
        request = HTTPRequest(
            CARD_HOME_URL,
            method='GET',
            request_timeout=CONNECT_TIME_OUT)
        response = yield tornado.gen.Task(client.fetch, request)
        cookie = response.headers['Set-Cookie'].split(';')[0]      

        data = {
            'name': cardnum,
            'userType': '1',
            'passwd': self.pwdchange(password,cookie),  #读取密码表
            'loginType': '2',
            'rand': '5000', 
            'imageField.x': '25',
            'imageField.y': '7'
        }

        #获取验证码
        request = HTTPRequest(
            CARD_VERIFY_URL,
            method='GET',
            request_timeout=CONNECT_TIME_OUT,
            headers={'Cookie': cookie})
        response = yield tornado.gen.Task(client.fetch, request)
        request = HTTPRequest(
            CARD_LOGIN_URL, body=urllib.urlencode(data),
            method='POST',
            request_timeout=CONNECT_TIME_OUT,
            headers={'Cookie': cookie})
        response = yield tornado.gen.Task(client.fetch, request)

        if response.body and response.body.find('frameset'):
            record = []
            if timedelta: #交易明细查询
                now = datetime.datetime.now()
                delta = datetime.timedelta(timedelta)
                date = {
                    'inputStartDate': (now-delta).strftime('%Y%m%d'),
                    'inputEndDate': now.strftime('%Y%m%d')
                }
                _continue,soup,page = self.login(cookie,date)
                soup = soup.findAll('tr',{'class': 'listbg'})

                for x in soup:
                    record.append(self.deal(x))
                for i in range(1,page):     #读取每一页
                    date['pageNum'] = i+1
                    request = HTTPRequest(
                        CARD_PAGE_URL, body=urllib.urlencode(date),
                        method='POST',
                        request_timeout=CONNECT_TIME_OUT,
                        headers={'Cookie': cookie})
                    response = yield tornado.gen.Task(client.fetch, request)
                    soup = BeautifulSoup(response.body).findAll('tr',{'class': 'listbg'})
                    for x in soup:
                        record.append(self.deal(x))
            else:  #余额状态查询
                request = HTTPRequest(
                    CARD_REMAIN_URL,
                    method='GET',
                    request_timeout=CONNECT_TIME_OUT,
                    headers={'Cookie': cookie})
                response = yield tornado.gen.Task(client.fetch, request)
                soup = BeautifulSoup(response.body).findAll('td',{'class':'neiwen'})
                record.append({'left': str(soup[46].getString()), 'status': str(soup[44].contents[1].getString())})
            self.write(json.dumps(record, ensure_ascii=False, indent=2))
        elif len(response.body) == 975: #用户密码错误
            self.write('wrong card number or password')
        else:
            self.write('server error')
        self.finish()

    def solve(self,im):
        count = []
        for x in range(13):
            count.append(0)
            for y in range(16):
                if im.getpixel((x,y))[2] < 5:
                    count[x] +=1
        for idx,val in enumerate(STAND):
            s = 0
            for i in range(13):
                s += abs(count[i]-val[i])
            if s < 5:
                return idx
        return 0

    def pwdchange(self,pwd,cookie):
        table = []
        req = urllib2.Request(CARD_PWD_URL, headers={'Cookie': cookie})
        f = urllib2.urlopen(req)
        tmpIm = cStringIO.StringIO(f.read())
        im = Image.open(tmpIm)

        for i in range(10):
            tm = im.crop(BOX[i])
            table.append(self.solve(tm))

        re = ""
        for x in pwd:
            re += str(table.index(int(x)))
        return re

    def stepin(self,_continue,data,cookie):
        try:
            req = urllib2.Request(CARD_DETIAL_URL+'?'+_continue,
                headers={'Cookie': cookie})
            return urllib2.urlopen(req,urllib.urlencode(data)).read()
        except:
            return ''

    def login(self,cookie,date):
        soup = BeautifulSoup(self.stepin('','',cookie))
        try:
            _continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action'].split('?')[1]
            cardid = soup.findAll('option')[0].getString()
        except:
            _continue = ''
            cardid = ''
        #发送查询类型
        data = {
            'account' : str(cardid),
            'inputObject' : 'all',
        }
        soup = BeautifulSoup(self.stepin(_continue,data,cookie))
        try:
            _continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action'].split('?')[1]
        except:
            pass
        #查询流水
        soup = BeautifulSoup(self.stepin(_continue,date,cookie))
        try:
            _continue = soup.findAll('form',{'id':'accounthisTrjn'})[0]['action'].split('?')[1]
        except:
            pass
        #等待查询结果
        while True:
            time.sleep(1)
            soup = BeautifulSoup(self.stepin(_continue,date,cookie))
            try:
                _continue = soup.findAll('form',{'name':'form1'})[0]['action'].split('?')[1]
            except:
                break
        try:
            page = soup.findAll('script',{'language': 'javascript'})[1].getString()
            p1 = page.find('button15')
            page = int(page[page.find('=',p1)+1:page.find(';',p1)])
        except:
            page = 1
        return _continue,soup,page

    def deal(self,tablelist):
        li = {}
        li['time'] = str(tablelist.contents[1].getString())
        li['type'] = str(tablelist.contents[3].getString())
        li['system'] = str(tablelist.contents[5].getString())
        li['dealtype'] = str(tablelist.contents[7].getString())
        li['money'] = str(tablelist.contents[9].getString())
        li['left'] = str(tablelist.contents[11].getString())
        li['index'] = str(tablelist.contents[13].getString())
        li['status'] = str(tablelist.contents[15].getString())
        return li


