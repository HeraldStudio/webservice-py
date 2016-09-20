# -*- coding: utf-8 -*-
# @Date    : 2014-06-27 14:36:45
# @Author  : xindervella@gamil.com yml_bright@163.com
import base64
from sqlalchemy.orm.exc import NoResultFound
from config import SRTP_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json
import re
from time import time
from ..models.srtp_cache import SRTPCache


class SRTPHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db
    def on_finish(self):
        self.db.close()
    def get(self):
        self.write('Herald Web Service')


    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        number = self.get_argument('number', default=None)
        retjson = {'code':200, 'content':''}
        status = None

        if not number:
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            #read from cache
            try:
                status = self.db.query(SRTPCache).filter(SRTPCache.cardnum == number).one()
                if status.date > int(time())-129600 and status.text != '*':
                        self.write(base64.b64decode(status.text))
                        self.finish()
                        return
            except NoResultFound:
                status = SRTPCache(cardnum = number,text = '*',date = int(time()))
                self.db.add(status)
                try:
                    self.db.commit()
                except:
                    self.db.rollback()

            params = urllib.urlencode({'Code': number})
            client = AsyncHTTPClient()
            request = HTTPRequest(SRTP_URL, body=params, method='POST',
                                  request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if not response.headers:
                retjson['code'] = 408
                retjson['content'] = 'time out'
            else:
                pat = re.compile('不存在|请输入', re.U)
                match = pat.search(response.body)
                if match:
                    retjson['code'] = 401
                    retjson['content'] = 'number not exist'
                else:
                    retjson['content'] = self.parser(response.body)
		ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

        # refresh cache
        if retjson['code'] == 200:
            status.date = int(time())
            status.text = base64.b64encode(ret)
            self.db.add(status)
            try:
                self.db.commit()
            except Exception,e:
                self.db.rollback()
            finally:
                self.db.remove()

    def parser(self, html):
        soup = BeautifulSoup(html)
        trs = soup.findAll('tr')

        name = trs[6].text.split(u'&nbsp;')[3].split(u'：')[1]
        cardnum = trs[6].text.split(u'&nbsp;')[1].split(u'：')[1]
        total = trs[-2].findAll('td')[-1].text
        score = trs[-1].findAll('td')[-1].text
        trs = trs[8:-2]
        srtp = [{
            'name': name,
            'card number': cardnum,
            'total': total,
            'score': score
        }]
        for td in trs:
            tds = td.findAll('td')
            srtp.append({
                'type': tds[0].text.replace('-', ''),
                'project': tds[1].text.replace('  ', ''),
                'date': tds[2].text.replace('-', ''),
                'department': tds[3].text.replace('-', ''),
                'total credit': tds[4].text.replace('-', ''),
                'proportion': tds[5].text.replace('-', ''),
                'credit': tds[6].text.replace('-', ''),
            })
        return srtp
