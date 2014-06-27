# -*- coding: utf-8 -*-
# @Date    : 2014-06-27 14:36:45
# @Author  : xindervella@gamil.com
from config import SRTP_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json


class SRTPHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        cardnum = self.get_argument('cardnum', default=None)

        if not cardnum:
            self.write('params lack')
        else:
            params = urllib.urlencode({'Code': cardnum})
            client = AsyncHTTPClient()
            request = HTTPRequest(SRTP_URL, body=params, method='POST',
                                  request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if not response.headers:
                self.write('time out')
            else:
                self.write(self.parser(response.body))
        self.finish()

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
        return json.dumps(srtp, ensure_ascii=False, indent=2)
