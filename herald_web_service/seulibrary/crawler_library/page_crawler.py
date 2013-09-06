
# -*- encoding: utf-8 -*-

'''Get library pages.

Author: Bing Liu
Date: 2013-08-30
'''
import sys
import time

import urllib2, cookielib, urllib

import config
from config import logger
import login_state
import page_parser
import custom_exception


class PageCrawler:

    def __init__(self, u='', p=''):
        self.__username = u
        self.__password = p
        self.__state = None

    def login(self):
        '''Log in the seu-library to get the cookie info.

        Args type will not be checked and not matter what type the args are, they will
        be converted into string without ensure correct. Correct username and password of
        string type are expected.

         Args:
            username: the login username, usually the original student number, it is expected
            with string type, eg: '07010115'
            password: the login password, it is also expected with string type.

        Returns:
            if login successfully, it will return a opener builded by urllib2.build_opener() and contains the cookie info
            if login success

        Raises:
            urllib2.HTTPError:
            urllib2.URLError:
        '''

        verify_url = config.LOGIN_URL

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        data = {'number' : self.__username,
                'passwd' : self.__password,
                'select' : 'cert_no',
                'returnUrl' : ''}

        req = urllib2.Request(verify_url, urllib.urlencode(data))
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        res = urllib2.urlopen(req, timeout = config.TIME_OUT)
        if res.getcode() == 200 and not page_parser.is_login_page(res.read()):  # it seems that response-code == 200 is not necessary
            state = login_state.LoginState(True, opener)
        else:
            state = login_state.LoginState(False, None)
        self.__state = state
        return state

    def get_rendered_book_page(self):
        '''Get render book list based on login.

        Only state is the result of login successfully will return book list.

        Args:
            state: login state, type: login_state

        Returns:
            If log in successfully, it will return html-string, else return None.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
            custom_exception.LoginException,
        '''
        if self.__state:
            state = self.__state
        else:
            state = self.login()
        status = state.get_status()
        if not status:
            raise custom_exception.LoginException
        else:
            opener = state.get_opener()
            result_url = config.RENDER_BOOK_LIST_URL
            urllib2.install_opener(opener)
            req = urllib2.Request(result_url)
            res = urllib2.urlopen(req, timeout=config.TIME_OUT)
            return res.read()


    def get_login_page(self):
        res = urllib2.urlopen(config.LOGIN_PAGE_URL)
        return  res.read()


    def get_search_result_page(self,strText,page=1, strSearchType='title', doctype='ALL', match_flag='forward', \
                               displaypg='20', sort='desc', orderby='CATA_DATE', showmode='list', dept='ALL'):
        '''Search book result page.

        Args:
            strSearchType搜索类型:
                title(题名), author(责任者), keyword(主题词), isbn(ISBN/ISSN), asordno(订购号), coden(分类号),
                callno(索书号), publisher(出版社) ,series(丛书名), tpinyin(题名拼音), apinyin(责任者拼音)
            doctype文档类型: (String)
                All(所有), 01(中文图书), 02(西文图书), 11(中文期刊), 12(西文期刊)
            match_flag检索模式:
                forward(前方一致), full(完全匹配), any(任意匹配)
            displaypg(每页显示个数):
                20, 30, 50, 100
            sort(结果排序):
                CATA_DATE(入藏日期), M_TITLE(题名), M_AUTHOR(责任者), M_CALL_NO(索书号), M_PUBLISHER(出版社),
                M_PUB_YEAR(出版日期)
            orderby:
                asc(升序), desc(降序)
            showmode结果显示:
                list(详细显示), table(表格显示)
            dept(选择校区):
                ALL(所有校区), 00(总馆), 01(九龙湖), 02(四牌楼), 03(丁家桥)

        Returns:
            If request successfully, return the html, else return None.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
        '''
        ori_url = "http://www.lib.seu.edu.cn:8080/opac/openlink.php?"
        params = {"strSearchType":strSearchType,  'strText':strText.encode('utf-8'), 'page':str(page),
                  'doctype':doctype, 'match_flag':match_flag, 'displaypg':displaypg,
                  'sort':sort, 'orderby':orderby, 'showmode':showmode, 'dept':dept}
        params_str = urllib.urlencode(params)
        search_url = ori_url + params_str
        req = urllib2.Request(search_url)
        res = urllib2.urlopen(req, timeout=config.TIME_OUT)
        return res.read()


    def get_search_detail_page(self, marc_no):
        '''Get book detail page.

        Args:
            relative_url: Every book has it's own detail-page url which can be gotten from the title-link
            in the search-list page

        Returns:
            If request successfully, return detail page string, else return None.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
        '''
        detail_url = config.BOOK_DETAIL_URL + marc_no
        req = urllib2.Request(detail_url)
        res = urllib2.urlopen(req, timeout=config.TIME_OUT)
        return res.read()


    def get_appoint_info_page(self, marc_no):
        '''Get appoint page .

        Args:
            marc_no: A number that can identify a book exclusively.

        Returns:
            the appoint page

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
            custom_exception.LoginException.
        '''
        renew_url = config.BOOK_APPOINT_URL + marc_no
        if self.__state:
            state = self.__state
        else:
            state = self.login()
        if state.get_status():
            req = urllib2.Request(renew_url)
            opener = state.get_opener()
            urllib2.install_opener(opener)
            res = urllib2.urlopen(req, timeout=config.TIME_OUT)
            return res.read()
        else:
            raise custom_exception.LoginException


    def renew_book(self,barcode):
        '''Renew book.

        Args:
            barcode: the unique code.

        Returns:
            SUCCESS(True) or FAILED(failed)

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
            custom_exception.LoginException
        '''
        SUCCESS = True
        FAILED = False
        if self.__state:
            state = self.__state
        else:
            state = self.login()
        timestamp = "%13f" % (time.time()*1000)
        renew_url = config.RENEW_URL % (barcode, timestamp)
        if state.get_status():
            opener = state.get_opener()
            urllib2.install_opener(opener)
            req = urllib2.Request(renew_url, urllib.urlencode({}))
            res = urllib2.urlopen(req, timeout=config.TIME_OUT)
            if res.getcode() == 200:
                # print res.info()
                html = res.read()
                return html
        else:
            raise custom_exception.LoginException

    def appoint_book(self, callno, location, check, preg_days='30', take_loca='90001', pregKeepDay='7'):
        '''Appoint book.

        Args:
            take_loca: 90001-九龙湖总借还处, 00916-丁家桥中文借书处, 00940-四牌楼总借还处
            callno: 索书号
            location: 图书馆藏处编号

        Returns:
            Result html.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
            custom_exception.LoginException
        '''
        state = self.login()
        if state.get_status():
            opener = state.get_opener()
            params = {'count':'10', 'preg_days'+str(check):preg_days, 'take_loca'+str(check):take_loca,
                      'callno'+str(check):callno, 'location'+str(check):location,
                      'pregKeepDays'+str(check):pregKeepDay ,'check':check
            }
            url = config.APPOINT_URL + urllib.urlencode(params)
            # print url
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
            # print res.info()
            html = res.read()
            return html
        else:
            raise custom_exception.LoginException

    def cancel_appoint(self, call_no, marc_no, loca):
        if self.__state:
            state = self.__state
        else:
            state = self.login()
        if state.get_status():
            t = "%13.0f"%(time.time()*1000)
            # call_no = "I712.45/488"
            # marc_no = "0000519601"
            # loca = "607"
            params = {"call_no":call_no, "marc_no":marc_no, "loca":loca, "time":t}
            url = "http://www.lib.seu.edu.cn:8080/reader/ajax_preg.php?"+urllib.urlencode(params)
            req = urllib2.Request(url, urllib.urlencode({}))
            urllib2.install_opener(state.get_opener())
            res = urllib2.urlopen(req)
            return res.read()
        else:
            raise custom_exception.LoginException


    def get_appointed_books_page(self):
        '''Get the page that can check what books i have appointed.

        Raises:
            urllib2.HTTPError,
            urllib2.URLError,
            custom_exception.LoginException
        '''
        if self.__state:
            state = self.__state
        else:
            state = self.login()
        if state.get_status():
            urllib2.install_opener(state.get_opener())
            req = urllib2.Request(config.APPOINTED_URL)
            res = urllib2.urlopen(req)
            return res.read()
        else:
            raise custom_exception.LoginException


if __name__ == '__main__':
    crawler = PageCrawler('07010115','199012')
    # html = crawler.get_rendered_book_page()
    # print html
    # crawler.renew_book()
    # print crawler.appoint_book('I712.45/488', '607', '1')
    # print crawler.get_search_result_page("python",2)
    # crawler.get_search_detail_page('item.php?marc_no=0000804600')
    # print crawler.get_appointed_books_page()
    # crawler.cancel_appoint()
    # s = "Hello,World"
    # import re
    # pattern = re.compile(r"(H.*),(W.*)")
    # # match = pattern.match(s)
    # match = re.search(r"(H.*),(W.*)", s)
    # print match.group()
    # print pattern.groups

    l = [1, 2, 3, 'a']
    print l.insert(1,4)
    print l

    d = {1:2, 'a':'b'}
    print d
    print d['a']










