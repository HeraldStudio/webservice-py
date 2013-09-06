
# -*- coding: utf-8 -*-

'''Parse library pages

Author: Bing Liu
Date: 2013-08-30
'''

import re

import BeautifulSoup

import book
import custom_exception

class PageParser:
    def isHonePage(self, html):
        pass


def is_login_page(html):
    '''Judge the page is library-login page or not.

    Because if the user login failed, the site will redirect to this page, so the method can
    also judge if the user login successfully.

    Since there is only one login-page, just judge it using the caption "登录我的图书馆".

    Args:
        html: The page html string.

    Returns:
        True or False.

    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        result = soup.findAll('caption')
        for cap in result:
            if "<caption>登录我的图书馆</caption>" == str(cap):
                # print "it is login page"
                return True
        # print "it is not login page"
        return False
    except Exception,e:
        raise custom_exception.ParseException("login page")

def get_render_book_list(html):
    '''Extract book info from the rendered book page.

    Args:
        html: The page-string of render book.

    Returns:
        If extract successfully, it will return the list of 'book.BookIntro' object, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_table = soup.findAll('table',{ 'width' : "100%", 'border' : "0", 'cellpadding' : "5",
                                            'cellspacing' : "1", 'bgcolor' : "#CCCCCC"})
        def __get_book_tags(tag_list):
            __remove_navi_string(tag_list)
            tag_list.remove(tag_list[0])
            return tag_list
        book_tags = book_table[0].contents
        __get_book_tags(book_tags)
        book_list = []
        for book_tag in book_tags:
            book_info_tags = book_tag.contents
            __remove_navi_string(book_info_tags)
            book_intro = book.BookRenderItem(book_info_tags[0].string.strip().encode('utf-8'),
                                        decode_strange_str(book_info_tags[1].a.string).strip().encode('utf-8'),
                                        decode_strange_str(book_info_tags[1].contents[1].string).strip().encode('utf-8')[1:].strip(),
                                        book_info_tags[2].string.strip().encode('utf-8'),
                                        book_info_tags[3].font.string.strip().encode('utf-8'),
                                        book_info_tags[4].string.strip().encode('utf-8'),
                                        book_info_tags[5].string.strip().encode('utf-8'),
                                        book_info_tags[6].string.strip().encode('utf-8')
                                        )
            print book_intro
            book_list.append(book_intro)
        return book_list
    except:
        raise custom_exception.ParseException("render-book page")


def get_search_book_list(html):
    '''Extract info from search result page.

    Args:
        html: the page resource string.

    Returns:
        If extract successfully, return the list of BookSearchItem obj, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_divs = soup.findAll('div',{'class':'list_books', 'id':'list_books'})
        book_list = []
        for book_div in book_divs:
            # print book_div
            book_item = book.BookSearchItem(
                book_div.h3.a['href'].encode('utf-8').strip()[17:],
                decode_strange_str(book_divs[0].h3.a.string[2:]).encode('utf-8').strip(),
                book_div.find('span',{'class':'doc_type_class'}).string.encode('utf-8').strip(),
                decode_strange_str(book_div.h3.contents[2].string).encode('utf-8').strip(),
                decode_strange_str(book_div.p.contents[2].string).encode('utf-8').strip(),
                decode_strange_str(book_div.p.contents[4].string).encode('utf-8').strip(),
                book_div.p.span.contents[1].string.encode('utf-8').strip(),
                book_div.p.span.contents[5].string.encode('utf-8').strip()
            )
            book_list.append(book_item)
            print book_item
        return book_list
    except:
        raise custom_exception.ParseException("search-result page")

def get_search_book_detail(html):
    '''Extract info from book detail page.

    Args:
        html: the page resource string.

    Returns:
        If extract successfully, return the list of BookSearchDetail obj, else return None.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_intro = soup.findAll('dl', {'class':'booklist'})
        # print len(book_intro)
        detail = book.BookSearchDetail()
        for i in range(len(book_intro)-1):
            intro_item = book_intro[i]
            detail.add_info(extract_string(intro_item.dt), decode_strange_str(extract_string(intro_item.dd)))

        store_table = soup.find('table', {'width':"670", 'border':"0", 'align':"center",
                                              'cellpadding':"2", 'cellspacing':"1",
                                              'bgcolor':"#d2d2d2"})
        store_items = store_table.findAll('tr')[1:]
        for store_item in store_items:
            items = store_item.findAll('td')

            # print type(items[0].string.encode('utf-8'))
            search_num = items[0].string.encode('utf-8').strip()
            barcode = items[1].string.encode('utf-8').strip()
            years = items[2].string.encode('utf-8').strip()
            campus = items[3].string.encode('utf-8').strip()
            room = items[4].string.encode('utf-8').strip()
            lend = extract_string(items[5]).encode('utf-8').strip()
            try:
                store = book.BookStore(search_num, barcode, years, campus, room, lend)
                detail.add_store(store)
            except Exception, e:
                print e

        # print store_items
        # print detail
        return detail
    except:
        raise custom_exception.ParseException("book-detail page")




def __remove_navi_string(tag_list):
    '''Remove NavigableString in tag.contents especially u'\n'.

    Args:
        tag_list: the list of tags and nav_string gotten from tag.contents.
    '''

    tag_type = BeautifulSoup.Tag
    for tag in tag_list:
        if type(tag) is not tag_type:
            tag_list.remove(tag)
    return tag_list

def __remove_blank(s):
    s.replace('&nbsp;','')
    return s

def decode_strange_str(s):
    s = s.replace('&#x','\u').replace(';','').replace('&nbsp','')
    u = s.decode('unicode-escape')
    return u


def extract_string(node):
    '''Extract all strings under one Tag.

    It is properly to use this function to extract strings under one node only when the strings are
    split from a entirety in meaning.

    Args:
        node: BeautifulSoup node.
    Returns:
        All the split strings will be combined into a entirety of unicode type.
    '''
    u = u''
    if type(node) == BeautifulSoup.Tag:
        for i in node.contents:
            u += extract_string(i)
    else:
        u += node.string
    return u

def get_appoint_list(html):
    '''Get appoint books.

    Args: appoint-books page html.

    Returns:
        Appoint books list.

    Raises:
        raise custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        renew_table = soup.find('table', {'width':"98%", 'border':"0", 'align':"center",
                                          'cellpadding':"2", 'cellspacing':"1",
                                          'bgcolor':"#CCCCCC", 'class':"table-line"})
        items = renew_table.findAll('tr')
        #print items
        appoint_item_list = []
        for i in range(1, len(items)-1):
            item = items[i]
            td_items = item.findAll('td')
            print item
            print '-----------------'
            places = []
            tmp = td_items[6].findAll('option')
            for tag in tmp:
                places.append(tag['value'].encode('utf-8').strip())
            appoint_item = book.AppointInfoItem(
                td_items[0].string.encode('utf-8').strip(),
                td_items[1].string.encode('utf-8').strip(),
                td_items[7].findAll('input')[1]['value'].encode('utf-8').strip(),
                td_items[2].string.encode('utf-8').strip(),
                td_items[3].string.encode('utf-8').strip(),
                td_items[4].string.encode('utf-8').strip(),
                extract_string(td_items[5]).encode('utf-8').strip(),
                places,
                td_items[7].findAll('input')[3]['disabled'].encode('utf-8').strip()
            )
            print appoint_item
            appoint_item_list.append(appoint_item)
        return appoint_item_list
    except:
        raise custom_exception.ParseException("appoint-books page")

def get_appointed_books(html):
    '''

    Returns:
        list of book.AppointedBookItem or [].

    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        book_table = soup.find('table', {'width':"100%", 'border':"0", 'cellpadding':"5",
                               'cellspacing':"1", 'bgcolor':"#CCCCCC"})
        # print book_table
        if not book_table:
            return []
        book_trs = book_table.findAll('tr')
        book_trs.remove(book_trs[0])
        # print book_trs
        book_list = []
        for b in book_trs:
            book_tds = b.findAll('td')
            book_item = book.AppointedBookItem(
                extract_string(book_tds[0]).encode('utf-8').strip(),
                decode_strange_str(extract_string(book_tds[1])).encode('utf-8').strip(),
                decode_strange_str(extract_string(book_tds[2])).encode('utf-8').strip(),
                extract_string(book_tds[3]).encode('utf-8').strip(),
                extract_string(book_tds[4]).encode('utf-8').strip(),
                extract_string(book_tds[5]).encode('utf-8').strip(),
                extract_string(book_tds[6]).encode('utf-8').strip(),
                extract_string(book_tds[7]).encode('utf-8').strip()
            )
            # print extract_string(book_tds[7]).encode('utf-8').strip()
            contain_data = book_tds[8].div.input['onclick']
            # pattern = re.compile(r"\((\'.*\'?)\,(\'.*\'?)\,(\'.*\'?)\,(\'.*\'?)\)")
            pattern = re.compile(r"\((\'.*\'?\,){3}(\'.*\'?)\)")
            match = pattern.search(contain_data)
            data_list = eval(match.group())
            data = {"marc_no":data_list[0], "call_no":data_list[1], "loca":data_list[3]}
            book_item.set_data(data)
            print book_item
            book_list.append(book_item)
        return book_list
    except Exception,e:
        raise custom_exception.ParseException("appointed-book page")


def is_renew_success(html):
    '''Judge if the page is the renew-success returns.

    Args:
        Renew operation's return html.

    Returns:
        True if yes, or False.

    Raise:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
        all_string = extract_string(soup.font)
        print all_string
        index = all_string.find(u"不得续借")
        if index == -1:
            return True
        else:
            return False
    except Exception,e:
        raise custom_exception.ParseException('renew result page')
    # print refuse

def is_appoint_success(html):
    '''Judge if the page is the return of appoint successfully.
    '''
    if html.find("预约成功") != -1:
        return True
    else:
        return False

def is_cancel_appoint_success(html):
    if html.find("已取消") != -1:
        return True
    else:
        return False


if __name__ == '__main__':
    print