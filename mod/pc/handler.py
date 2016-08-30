#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-26 14:46:50
# @Author  : jerry.liangj@qq.com

from config import *
from tornado.httpclient import HTTPRequest, HTTPClient,HTTPError
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
from ..models.pc_cache import PCCache
from sqlalchemy.orm.exc import NoResultFound
from time import time, localtime, strftime
import datetime
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
        self.getData()
        self.write('Herald Web Service')

    def post(self):
        retjson = {'code':200, 'content':u'暂时关闭'}
        try:
            if self.ismorning():
                status = self.db.query(PCCache).filter( PCCache.date == self.today(),PCCache.lastdate+180>int(time())).one()
                retjson['content'] = base64.b64decode(status.text)
                self.db.close()
                self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
                self.finish()
            else:
                status = self.db.query(PCCache).filter( PCCache.date == self.today()).one()
                retjson['content'] = base64.b64decode(status.text)
                self.db.close()
                self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
                self.finish()
        except NoResultFound:
            retjson['code'] = 201
            retjson['content'] = 'refreshing'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()
            self.refresh_status()
        except Exception,e:
            # print traceback.print_exc()
            retjson['code'] = 500
            retjson['content'] = str(e)
            self.db.close()
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
            self.finish()

        

    def refresh_status(self):
        lock = self.db.query(PCCache).filter(
                    PCCache.date == 0).one()
        if lock.text == '1'or(lock.lastdate!=0 and lock.lastdate+180>int(time())):
            return
        else:
            lock.text == '1'
            lock.lastdate = int(time())
            self.db.commit()

        # ret = self.qq_request()
        ret = self.getData()
        if ret and (ret['code'] == 200):
            self.recognize1(ret['content'])
        lock.text == '0'
        self.db.commit()
        self.db.close()



    def getData(self):
        ret = {'code':200,'content':''}
        try:
            content = self.db.execute("select * from wechat.boardcast where date like '"+datetime.datetime.now().strftime("%Y-%m-%d")+"%%' order by mid DESC LIMIT 1").fetchall()
            if content:
                ret['content'] = content[0]['msg']
            else:
                ret['code'] = 400
        except Exception,e:
            ret['code'] = 500
        return ret

    def today(self):
        return int(strftime('%Y%m%d', localtime(time())))
    def ismorning(self):
        if int(strftime('%H', localtime(time())))==6:
            return True
        else:
            return False

    def recognize(self, text):
        y_keyword = [u'正常跑操', u'跑操正常', u'今天继续跑操', u'今天跑操']
        result = u'今天不跑操'
        for k in y_keyword:
            if text.find(k)>=0:
                result = u'今天正常跑操'
                break
        if self.ismorning():
            try:
                status = self.db.query(PCCache).filter(PCCache.date==self.today()).one()
                status.text = base64.b64encode(result)
                status.lastdate = int(time())
                self.db.add(status)
            except NoResultFound:
                status = PCCache(date=self.today(), text=base64.b64encode(result),lastdate=int(time()))
                self.db.add(status)
            except:
                pass
                # print traceback.print_exc()
        else:
            status = PCCache(date=self.today(), text=base64.b64encode(result),lastdate=int(time()))
            self.db.add(status)

        self.db.commit()

    def recognize1(self,text):
        y_keyword = [u'早操正常进行', u'正常进行', u'今天继续跑操', u'今天跑操']
        result = u'今天不跑操'
        for k in y_keyword:
            if text.find(k)>=0:
                result = u'今天正常跑操'
                break
        if self.ismorning():
            try:
                status = self.db.query(PCCache).filter(PCCache.date==self.today()).one()
                status.text = base64.b64encode(result)
                status.lastdate = int(time())
                self.db.add(status)
            except NoResultFound:
                status = PCCache(date=self.today(), text=base64.b64encode(result),lastdate=int(time()))
                self.db.add(status)
            except:
                pass
                # print traceback.print_exc()
        else:
            status = PCCache(date=self.today(), text=base64.b64encode(result),lastdate=int(time()))
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
        return bytes(bytearray.fromhex(s))
    def pwdencode(self, vcode, uin, pwd):
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
            # print response.body
#get_token
            fuckcookie = response.headers['Set-Cookie']
            temp = fuckcookie.split(';')
            
            pt2gguin = temp[0]+';'
            skey = temp[7].split(',')[1]+';'
            ptcz = temp[28].split(',')[1]+';'
            uin = temp[4].split(',')[1]+';'
            ptsip = temp[22].split(',')[1]+';'

            tempcookie = pt2gguin+skey+ptcz+uin+ptsip
            getPtSkeyUrl = response.body.split('\'')[5]
# get superkey
            request1 = HTTPRequest(
                getPtSkeyUrl,
                method="GET",
                headers={
                    'Cookie':init_cookie+tempcookie+fuckcookie,
                },
                request_timeout = 8,
                follow_redirects=False
            )

            ptskey = ""
            try:
                response = client.fetch(request1)
            except HTTPError as e:
                fuckfuckcookie = e.response.headers['Set-Cookie']
                fuckcookieTemp = fuckfuckcookie.split(';')
                ptskey = fuckcookieTemp[13].split('=')[1]
            hash1 = 5381
            for i in ptskey:
                hash1 +=(hash1<<5)+ord(i)
            super_token = hash1&2147483647


            jsonUrl = 'http://m.qzone.com/combo?g_tk='+str(super_token)+'&hostuin=3084772927&action=1&g_f=&refresh_type=1&res_type=2&format=json'#refresh_type确定说说条数
            finalUrl = 'http://m.qzone.com/infocenter#3084772927/mine'
            request = HTTPRequest(
                jsonUrl,
                method='GET',
                headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cookie':init_cookie+fuckcookie+fuckfuckcookie,
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                },
                request_timeout=4
                )
            response = client.fetch(request)
            ret = json.loads(response.body)
            testjson = ret['data']['feeds']['vFeeds']
            re_regular = re.compile("\[em\]e(\d+)\[\/em\]")

            for i in range(len(testjson)):
                try:
                    content =  testjson[i]['summary']['summary']
                    c_time = testjson[i]['comm']['time']
                    # print re_regular.sub('',content)
                    if u'跑操早播报' in content:
                        if strftime("%Y-%m-%d",localtime(c_time)) == strftime("%Y-%m-%d",localtime(time())):
                            if strftime("%H",localtime(c_time))== '06':
                                retjson['code'] = 200
                                retjson['content'] =  testjson[i]['summary']['summary'][7:]
                                # retjson['content'] =  re_regular.sub('',testjson[i]['summary']['summary'])
                except KeyError:
                    pass
        except Exception,e:
            # print traceback.print_exc()
            retjson['code'] = 201
            retjson['content'] = str(e)
        return retjson
