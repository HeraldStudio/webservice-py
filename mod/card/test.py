from config import *
from BeautifulSoup import BeautifulSoup
from time import time
import urllib, re
import json, base64
import datetime
import traceback
import requests
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient,HTTPError
def authApi(username,password):
    data = {
            'username':username,
            'password':password
        }
    result = {'code':200,'content':''}
    try:
        client = HTTPClient()
        request = HTTPRequest(
            "https://mobile4.seu.edu.cn/_ids_mobile/login18_9",
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
    except HTTPError as e:
        result['code'] = 400
    except Exception,e:
        result['code'] = 500
    return result


def post():
  cardnum = "213131592"
  retjson = {'code':200, 'content':''}

  try:
    response = authApi(cardnum,"lj084358!!")
    if response['code']==200:
      cookie = response['content']
      print "cookie: ", cookie
      response = requests.get(LOGIN_URL,headers={'Cookie':cookie})
      cookie += ';' + response.headers['Set-Cookie'].split(';')[0]
      response = requests.get(USERID_URL,headers={'Cookie':cookie})
      soup = BeautifulSoup(response.content)
      td = soup.findAll('td',{"class": "neiwen"})
    else:
      print "login error"
  except Exception,e:
    print str(e)
post()
