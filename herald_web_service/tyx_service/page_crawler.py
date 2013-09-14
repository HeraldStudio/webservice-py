
# -*- encoding: utf-8 -*-
import cookielib
import urllib
import urllib2

import config
import page_parser
import custom_exception


def login(cardNumber, password):
    data = {
        'xh': str(cardNumber),
        'mm': str(password),
        'method': 'login'
    }
    cookieJar = cookielib.CookieJar()
    cookieHandler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookieHandler)
    urllib2.install_opener(opener)
    reqLogin = urllib2.Request(config.TYX_LOGIN_URL, urllib.urlencode(data))
    resLogin = urllib2.urlopen(reqLogin)
    html = resLogin.read()
    if len(html) == 524:
        state = page_parser.LoginState(True, opener)
    else:
        state = page_parser.LoginState(False, None)
    return state


def crawl_paocao_page(cardNumber, password):
    '''
    Returns:
        html page.

    Raises:
        AccountError:
        urllib2.HTTPError:
        urllib2.URLError:
    '''
    state = login(cardNumber, password)
    if state.get_login_status():
        urllib2.install_opener(state.get_opener())
        reqLoad = urllib2.Request(config.TYX_PC_URL)
        resLoad = urllib2.urlopen(reqLoad, timeout=config.TIME_OUT)
        html = resLoad.read()
        return html
    else:
        raise custom_exception.AccountError()

def get_ren_tyb():
    req = urllib2.Request(config.REN_TYB_URL)
    res = urllib2.urlopen(req, timeout=config.TIME_OUT)
    return res.read()

if __name__ == "__main__":
    # print crawl_paocao_page('213102847', '213102847')
    get_ren_tyb()

