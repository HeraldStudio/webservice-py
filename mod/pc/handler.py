#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-12-11 18:51:29
# @Author  : yml_bright@163.com

from config import *
from tornado.httpclient import HTTPRequest, HTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
from ..models.pc_cache import PCCache
from sqlalchemy.orm.exc import NoResultFound
from time import time, localtime, strftime
import urllib, re
import json
import base64
import rsa,tea,traceback
import os, hashlib, re, tempfile, binascii, base64

class PCHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def post(self):
        retjson = {'code':200, 'content':u'暂时关闭'}
        try:
            status = self.db.query(PCCache).filter( PCCache.date == self.today() ).one()
            retjson['content'] = base64.b64decode(status.text)
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.db.close()
            self.finish()
        except NoResultFound:
            retjson['code'] = 201
            retjson['content'] = 'refreshing'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()
            self.refresh_status()
        except Exception,e:
            retjson['code'] = 500
            retjson['content'] = str(e)
            with open('api_error.log','a+') as f:
                    f.write(strftime('%Y%m%d %H:%M:%S in [webservice]', localtime(time()))+'\n'+str(str(e)+'\n[pc]\t'+'\nString:'+str(retjson)+'\n\n'))
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()

    def refresh_status(self):
        # print 'get'
        lock = self.db.query(PCCache).filter(
                    PCCache.date == 0).one()
        if lock.text == '1' or (lock.lastdate!=0&lock.lastdate+300>int(time())):
            # print 'exit'
            return
        else:
            lock.text == '1'
            lock.lastdate = int(time())
            self.db.commit()

        ret = self.qq_request()
        # print ret
        if ret and (ret['code'] == 200):
            self.recognize(ret['content'])

        lock.text == '0'
        self.db.commit()
        self.db.close()

    def today(self):
        return int(strftime('%Y%m%d', localtime(time())))

    def recognize(self, text):
        y_keyword = [u'正常跑操', u'跑操正常', u'今天继续跑操', u'今天跑操']
        result = u'今天不跑操'
        for k in y_keyword:
            if text.find(k)>=0:
                result = u'今天正常跑操'
                break
        status = PCCache(date=self.today(), text=base64.b64encode(result))
        self.db.add(status)
        self.db.commit()


    pubKey=rsa.PublicKey(int(
        'F20CE00BAE5361F8FA3AE9CEFA495362'
        'FF7DA1BA628F64A347F0A8C012BF0B25'
        '4A30CD92ABFFE7A6EE0DC424CB6166F8'
        '819EFA5BCCB20EDFB4AD02E412CCF579'
        'B1CA711D55B8B0B3AEB60153D5E0693A'
        '2A86F3167D7847A0CB8B00004716A909'
        '5D9BADC977CBB804DBDCBA6029A97108'
        '69A453F27DFDDF83C016D928B3CBF4C7',
        16
    ), 3)
    def fromhex(self, s):
        # Python 3: bytes.fromhex
        return bytes(bytearray.fromhex(s))
    def pwdencode(self, vcode, uin, pwd):
        # uin is the bytes of QQ number stored in unsigned long (8 bytes)
        salt = uin.replace(r'\x', '')
        h1 = hashlib.md5(pwd.encode()).digest()
        s2 = hashlib.md5(h1 + self.fromhex(salt)).hexdigest().upper()
        rsaH1 = binascii.b2a_hex(rsa.encrypt(h1, self.pubKey)).decode()
        rsaH1Len = hex(len(rsaH1) // 2)[2:]
        hexVcode = binascii.b2a_hex(vcode.upper().encode()).decode()
        vcodeLen = hex(len(hexVcode) // 2)[2:]
        l = len(vcodeLen)
        if l < 4:
            vcodeLen = '0' * (4 - l) + vcodeLen
        l = len(rsaH1Len)
        if l < 4:
            rsaH1Len = '0' * (4 - l) + rsaH1Len
        pwd1 = rsaH1Len + rsaH1 + salt + vcodeLen + hexVcode
        saltPwd = base64.b64encode(
            tea.encrypt(self.fromhex(pwd1), self.fromhex(s2))
        ).decode().replace('/', '-').replace('+', '*').replace('=', '_')
        return saltPwd
    def qq_request(self):
        retjson = {'code':400,'content':'No Result'}
        try:
            client = HTTPClient()
#init
            request = HTTPRequest(
                init_url,
                method='GET',
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie':'',
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                },
                request_timeout=4
                )
            response = client.fetch(request)
            init_cookie = response.headers['Set-Cookie']
            # print init_cookie
#check
            request = HTTPRequest(
                checkurl,
                method='GET',
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie':init_cookie,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                },
                request_timeout=4
                )
            response = client.fetch(request)
            check_cookie = response.headers['Set-Cookie']

            result = response.body.split('\'')
           
#login
            
            session = result[7]
            code = result[3]
            salt = result[5]
            data = {
                'aid':'549000929',
                'daid':'147',
                'device':2,
                'fp':'loginerroralert',
                'from_ui':1,
                'g':1,
                'h':1,
                'low_login_enable':0,
                'p':self.pwdencode(code,salt,password),
                'pt_3rd_aid':0,
                'pt_randsalt':0,
                'pt_uistyle':9,
                'pt_vcode_v1':0,
                'pt_verifysession_v1':session,
                'ptlang':2052,
                'ptredirect':1,
                'u':username,
                'u1':'http://m.qzone.com/infocenter?g_f=',
                'verifycode':code
            }

            request = HTTPRequest(
                login_url+urllib.urlencode(data),
                method='GET',
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie':init_cookie+check_cookie,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                },
                request_timeout=4
                )
            response = client.fetch(request)
            print response.body
            #get_token
            fuckcookie = response.headers['Set-Cookie']
            fuckcookieTemp = fuckcookie.split(';')
            superykey = fuckcookieTemp[7].split('=')[1]
            hash1 = 5381
            for i in superykey:
                hash1 +=(hash1<<5)+ord(i)
            super_token = hash1&2147483647
            fuck = response.body.split('\'')
            jsonUrl = 'http://m.qzone.com/combo?g_tk='+str(super_token)+'&hostuin=3084772927&action=1&g_f=&refresh_type=1&res_type=2&format=json'#refresh_type确定说说条数
            finalUrl = 'http://m.qzone.com/infocenter#3084772927/mine'
            request = HTTPRequest(
                jsonUrl,
                method='GET',
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie':init_cookie+check_cookie+fuckcookie,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                },
                request_timeout=4
                )
            response = client.fetch(request)
            ret = json.loads(response.body)
            print response.body
            testjson = ret['data']['feeds']['vFeeds']
            for i in range(len(testjson)):
                try:
                    content =  testjson[i]['summary']['summary']
                    c_time = testjson[i]['comm']['time']
                    if u'跑操早播报' in content:
                        print i,'ok'
                        if strftime("%Y-%m-%d",localtime(c_time)) == strftime("%Y-%m-%d",localtime(time())):
                            print i,'time ok',strftime("%H",localtime(c_time))
                            if strftime("%H",localtime(c_time))== '06':
                                retjson['code'] = 200
                                retjson['content'] =  testjson[i]['summary']['summary'][7:]
                except KeyError:
                    pass
        except Exception,e:
            print traceback.print_exc()
            retjson['code'] = 201
            retjson['content'] = str(e)
            # print traceback.print_exc()
        return retjson
    # def renren_request(self):
    #     client = HTTPClient()
    #     request = HTTPRequest(
    #         RENREN_URL,
    #         method='GET',
    #         request_timeout=TIME_OUT,
    #         headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
    #     response = client.fetch(request)
    #     if response.body > 2048:
    #         soup = BeautifulSoup(response.body)
    #         text = soup.findAll('span',{'class':'status-detail'})[0].text
    #         time = soup.findAll('span',{'class':'pulish-time'})[0].text
    #         if text.find('早播报')>0 or (text.find('气温')>0 and text.find('跑操')>0):
    #             return {'text':text, 'time':time}
    #         else:
    #             return None
    #     else:
    #         return None
