# -*- coding: utf-8 -*-
# @Date    : 2014-06-26 17:00:02
# @Author  : xindervella@gamil.com
from config import VERCODE_URL, LOGIN_URL, INFO_URL
from config import STANDARD, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
import tornado.web
import tornado.gen
import urllib
import json
import io
import Image


class GPAHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        username = self.get_argument('username', default=None)
        pwd = self.get_argument('password', default=None)

        if not (username or pwd):
            self.write('params lack')
        else:
            client = AsyncHTTPClient()
            request = HTTPRequest(VERCODE_URL, request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            if not response.headers:
                self.write('time out')
            else:
                cookie = response.headers['Set-Cookie'].split(';')[0]
                img = Image.open(io.BytesIO(response.body))
                vercode = self.recognize(img)
                params = urllib.urlencode({
                    'userName': username,
                    'password': pwd,
                    'vercode': vercode
                })
                request = HTTPRequest(LOGIN_URL, body=params, method='POST',
                                      headers={'Cookie': cookie},
                                      request_timeout=TIME_OUT)
                response = yield tornado.gen.Task(client.fetch, request)
                if not response.headers:
                    self.write('time out')
                else:
                    if int(response.headers['Content-Length']) > 1000:
                        self.write('wrong username or password')
                    else:
                        request = HTTPRequest(INFO_URL,
                                              request_timeout=TIME_OUT,
                                              headers={'Cookie': cookie})
                        response = yield tornado.gen.Task(client.fetch, request)
                        if not response.headers:
                            self.write('time out')
                        else:
                            self.write(self.parser(response.body))
        self.finish()

    def recognize(self, img):
        start = [13, 59, 105, 151]
        result = ''
        for i in start:
            sample = []
            for i in xrange(i, i + 40):
                temp = 0
                for j in xrange(0, 100):
                    temp += (img.getpixel((i, j))[1] < 40)
                sample.append(temp)
            min_score = 1000
            max_match = 0
            for idx, val in enumerate(STANDARD):
                diff = []
                for i in xrange(len(sample)):
                    diff.append(sample[i] - val[i])
                avg = float(sum(diff)) / len(diff)

                for i in xrange(len(sample)):
                    diff[i] = abs(diff[i] - avg)
                score = sum(diff)
                if score < min_score:
                    min_score = score
                    max_match = idx

            result = result + str(max_match)
        return result

    def parser(self, html):
        soup = BeautifulSoup(html)
        trs = soup.findAll('tr')
        items = []
        credit = trs[-1].findAll('td')
        items.append({
            'gpa': credit[0].text,
            'gpa without revamp': credit[1].text,
            'calculate time': credit[-1].text[6:-6]
        })
        for i in xrange(2, len(trs) - 4):
            tds = trs[i].findAll('td')
            items.append({
                'semester': tds[1].text,
                'name': tds[3].text[:-6],
                'credit': tds[4].text[:-6],
                'score': tds[5].text[:-6],
                'type': tds[6].text[:-6],
                'extra': tds[7].text[:-6]
            })
        return json.dumps(items, ensure_ascii=False, indent=2)
