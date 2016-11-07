# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : yml_bright@163.com
from config import *
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from ..models.pe_models import PEUser
from ..models.tice_cache import TiceCache
from sqlalchemy.orm.exc import NoResultFound
import tornado.web
import tornado.gen
import urllib
import random
import json,socket,base64
from time import time, localtime, strftime,mktime,strptime
import datetime

last_refresh = 0
all_count = {}
all_sum = 0

class PEHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    def on_finish(self):
        self.db.close()


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        state = 'success'
        cardnum = self.get_argument('cardnum', default=None)
        pwd = self.get_argument('pwd', default=cardnum)
        retjson = {'code':200, 'content':''}
        # pwd 缺省为 cardnum

        if not cardnum:
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            result = self.get_pe_count(cardnum)
            if result == -1:
                state = 'time_out'
                try:
                    # 超时取出缓存
                    user = self.db.query(PEUser).filter(
                        PEUser.cardnum == int(cardnum)).one()
                    retjson['content'] = user.count
                    retjson['rank'] = self.get_rank(user.count)
                    retjson['remain'] = self.get_remain_day()
                except NoResultFound:
                    retjson['code'] = 408
                    retjson['content'] = 'time out'
            else:
                retjson['content'] = str(result)
                retjson['rank'] = self.get_rank(result)
                retjson['remain'] = self.get_remain_day()
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

        if state == 'success':
            # 更新缓存
            try:
                user = self.db.query(PEUser).filter(
                    PEUser.cardnum == int(cardnum)).one()
                user.count = int(result)
            except NoResultFound:
                user = PEUser(cardnum=int(cardnum), count=count)
                self.db.add(user)
            finally:
                self.db.commit()
        self.db.close()

    def get_pe_count(self,cardnum):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((API_SERVER_HOST, API_SERVER_PORT))
            s.send('\x00'+A+'\x09'+cardnum+'\x00')
            recv = s.recv(1024).split(',')
            return int(recv[0])+int(recv[1])
        except socket.timeout:
            return -1
        except:
            return -1
    def get_remain_day(self, count):
        finay_day_strp = strptime(finay_day,"%Y-%m-%d")
        final = datetime.datetime(finay_day_strp[0],finay_day_strp[1],finay_day_strp[2])
        current_day_strp = strptime(strftime('%Y-%m-%d', localtime(time())),"%Y-%m-%d")
        current = datetime.datetime(current_day_strp[0],current_day_strp[1],current_day_strp[2])
        alldays = (final-current).days
        current_date = daymap[strftime('%a', localtime(time()))]
        front_remain = 7-current_date
        front_day = 6-current_date
        front_day = front_day if front_day>0 else 0
        back_remain = 5
        all_week = (alldays-5-front_remain)/7
        workday_count = (all_week+1)*5+front_day
        if current_date<=6:
            workday_count = workday_count-1
        return workday_count if workday_count > 0  else 0
    def get_rank(self, count):
        global last_refresh
        global all_count
        global all_sum
        try:
            if last_refresh + 300 < int(time()):
                last_refresh = int(time())
                db_instance = self.db.execute("select count, count(*) as all_sum from pe group by count").fetchall()
                all_count = {}
                all_sum = 0
                for item in db_instance:
                    all_count[item.count] = int(item.all_sum)
                    all_sum += int(item.all_sum)
            temp_sum = 0
            for i, j in all_count.items():
                if int(i) >= int(count):
                    temp_sum += all_count[i]
            print temp_sum
            return '%.2f' % ((float(all_sum)-temp_sum)/all_sum*100)
        except Exception,e:
            return '0'

#体测信息
class ticeInfoHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum',default=None)
        retjson = {'code':200,'content':''}
        state = 'fail'
        if not cardnum:
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            #read from cache
            try:
                status = self.db.query(TiceCache).filter(TiceCache.cardnum == cardnum).one()
                if status.date > int(time()-100000) and status.text != '*':
                    self.write(base64.b64decode(status.text))
                    self.finish()
                    return
            except NoResultFound:
                status = TiceCache(cardnum = cardnum,text='*',date = int(time()))
                self.db.add(status)
            try:
                sefl.db.commit()
            except:
                self.db.rollback()

            try:
                result = self.get_tice_info(cardnum)
                if result == -1:
                    retjson['code'] = 408
                    retjson['content'] = 'time out'
                else:
                    state = 'success'
                    retjson['content'] = result
            except Exception,e:
                retjson['code'] = 500
                retjson['content'] = str(e)
        ret = json.dumps(retjson,ensure_ascii=False,indent=2)
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()

        #refresh cache

        if state == 'success':
            try:
                status.date = int(time())
                status.text = base64.b64encode(ret)
                self.db.add(status)
                self.db.commit()
            except:
                self.db.rollback()
    def get_tice_info(self,cardnum):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
            s.settimeout(3)  
            s.connect((API_SERVER_HOST, API_SERVER_PORT))
            s.send('\x01'+A+'\x09'+cardnum+'\x00')
            recv = s.recv(1024).split(',')
            ret = {
                'height':recv[0],
                'weight':recv[1],
                'fei':{
                    'value':recv[2],
                    'score':recv[3],
                    'comment':recv[4].decode('gbk').encode('utf-8')
                },
                '50meter':{
                    'value':recv[5],
                    'score':recv[6],
                    'comment':recv[7].decode('gbk').encode('utf-8')
                },
                'jump':{
                    'value':recv[8],
                    'score':recv[9],
                    'comment':recv[10].decode('gbk').encode('utf-8')
                },
                '1000meter':{
                    'value':recv[14],
                    'score':recv[15],
                    'comment':recv[16].decode('gbk').encode('utf-8')
                },
                'zuoqian':{
                    'value':recv[17],
                    'score':recv[18],
                    'comment':recv[19].decode('gbk').encode('utf-8')
                },
                'up-down':{
                    'value':recv[20],
                    'score':recv[21],
                    'comment':recv[22].decode('gbk').encode('utf-8')
                },
                'score':recv[23].decode('gbk').encode('utf-8')
            }
            return ret
        except:
            return -1


