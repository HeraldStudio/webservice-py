# -*- coding: utf-8 -*-
# @Date    : 2014-11-03 15:34:57
# @Author  : yml_bright@163.com

from config import CHECK_URL, TIME_OUT
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient,HTTPError
import tornado.web
import tornado.gen
import urllib,json
from time import time, localtime, strftime
from newHandler import newAuthApi

class AuthHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Herald Web Service')

   
    def post(self):
        result = authApi(self.get_argument('cardnum'),self.get_argument('password'))
        if(result['code']==200):
            self.write(result['content'])
            self.finish()
        else:
            raise tornado.web.HTTPError(401)

def authApiTemp(username, password):
    data = {
        'user':username,
         'password':password
    }
    result = {'code':200,'content':''}

    try:
        client = HTTPClient()
        request = HTTPRequest(
        "http://192.168.56.1/auth",
        method='POST',
        body=urllib.urlencode(data),
        validate_cert=False,
        request_timeout=TIME_OUT)
        response = client.fetch(request)
        print response.body
        j = json.loads(response.body)
        result['code'] = j['code']
    except HTTPError:
        result['code'] = 400
    except Exception,e:
        result['code'] = 500
    return result

'''

def authApi(username,password):
    return newAuthApi(username,password)

'''
def authApi(username,password):
    data = {
            'username':username,
            'password':password
        }
    result = {'code':200,'content':''}
    try:
        client = HTTPClient()
        request = HTTPRequest(
            CHECK_URL,
            method='POST',
            body=urllib.urlencode(data),
            validate_cert=False,
            request_timeout=TIME_OUT)
        response = client.fetch(request)
        header = response.headers
        if 'Ssocookie' in header.keys():
            headertemp = json.loads(header['Ssocookie'])
            cookie = headertemp[0]['cookieName']+"="+headertemp[0]['cookieValue']
            cookie += ";"+header['Set-Cookie'].split(";")[0]
            result['content'] = cookie
        else:
            result['code'] = 400
    except HTTPError:
        result['code'] = 400
    except Exception,e:
        result['code'] = 500
    return result

if __name__ == '__main__':
    print(authApi('213151933', 'vme2744394782'))
