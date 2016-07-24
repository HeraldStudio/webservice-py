# -*- coding: utf-8 -*-
# @Date    : 2016-03-24 16 16:34:57
# @Author  : jerry.liangj@qq.com

import time,json
import urllib
from tornado.httpclient import HTTPRequest, HTTPClient,HTTPError
from ..models.cookie_cache import CookieCache
from sqlalchemy.orm.exc import NoResultFound
from config import *

def getCookie(db,cardnum,card_pwd):
	state = 1
	ret = {'code':200,'content':''}
	try:
		result = db.query(CookieCache).filter(CookieCache.cardnum==cardnum).one()
		if (result.date+COOKIE_TIMEOUT<int(time.time())):
			state = 0
		else:
			ret['content'] = result.cookie
	except NoResultFound:
		result = CookieCache(cardnum=cardnum,cookie="",date=int(time.time()))
		state = 0
	except Exception,e:
		ret['code'] = 500
		ret['content'] = str(e)
	if state==0:
		sta,cookie = RefreshCookie(cardnum,card_pwd)
		if sta:
			ret['content'] = cookie
			result.cookie = cookie
			try:
				db.add(result)
				db.commit()
			except:
				db.rollback()
		else:
			ret['code'] = 500
			ret['content'] = cookie
	return ret


def RefreshCookie(cardnum,card_pwd):
    # print "refresh"
    data = {
            'username':cardnum,
            'password':card_pwd
        }
    try:
        client = HTTPClient()
        request = HTTPRequest(
            CHECK_URL,
            method='POST',
            body=urllib.urlencode(data),
            validate_cert=False,
            request_timeout=4)
        response = client.fetch(request)
        header = response.headers
        if 'Ssocookie' in header.keys():
            headertemp = json.loads(header['Ssocookie'])
            cookie = headertemp[1]['cookieName']+"="+headertemp[1]['cookieValue']
            cookie += ";"+header['Set-Cookie'].split(";")[0]
            return True,cookie
        else:
            return False,"No cookie"
    except Exception,e:
        # print str(e)
        return False,str(e)