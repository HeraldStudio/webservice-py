from PIL import Image
import io
import urllib,json
from tornado.httpclient import HTTPRequest, AsyncHTTPClient,HTTPClient,HTTPError
import traceback

LOGIN_URL = "http://myold.seu.edu.cn/userPasswordValidate.portal"

def myoldAuthApi(username,password):
    data = {
        'Login.Token1': username,
        'Login.Token2': password
    }
    result = {'code':200,'content':''}
    try:
        client = HTTPClient()
        request = HTTPRequest(
            LOGIN_URL,
            method='POST',
            body=urllib.urlencode(data),
            request_timeout=8
        )
        response = client.fetch(request)
        if 'handleLoginSuccessed' not in response.body:
            result['code'] = 400
        else:
            result['content'] = response.headers['Set-Cookie']
    except Exception as e:
        result['code'] = 500
    return result

