
# -*- utf-8 -*-

'''Provide kinds of operations about library.

operations include many kinds, such as get rendered books, search book, appoint book.

Author: Bing Liu
Date: 2013-08-30
'''

import page_crawler
import page_parser

class LibraryService:
    def __init__(self, username='', password=''):
        self.crawler = page_crawler.PageCrawler(username, password)

    def get_render_book_list(self):
        html = self.crawler.get_rendered_book_page()
        books = page_parser.get_render_book_list(html)
        # print book_list
        book_list = []
        for book in books:
            book_list.append(book.to_json_obj())
        return book_list

    def get_appoint_book_info(self, marc_no):
        html = self.crawler.get_appoint_info_page(marc_no)
        books = page_parser.get_appoint_list(html)
        book_list = [b.to_json_obj() for b in books]
        return book_list

    def get_appointed_book_list(self):
        html = self.crawler.get_appointed_books_page()
        books = page_parser.get_appointed_books(html)
        book_list = [b.to_json_obj() for b in books]
        return book_list

    def get_search_result_list(self,strText,page=1, strSearchType='title', doctype='ALL', match_flag='forward', \
                               displaypg='20', sort='desc', orderby='CATA_DATE', showmode='list', dept='ALL'):
        html = self.crawler.get_search_result_page(strText,page, strSearchType, doctype, match_flag, \
                               displaypg, sort, orderby, showmode, dept)
        books = page_parser.get_search_book_list(html)
        book_list = []
        for book in books:
            book_list.append(book.to_json_obj())
        return book_list

    def get_appointed_books(self):
        html = self.crawler.get_appointed_books_page()
        book_list = page_parser.get_appointed_books(html)
        books = [b.to_json_obj() for b in book_list]
        return books


    def get_book_detail(self, marc_no):
        html = self.crawler.get_search_detail_page(marc_no)
        book = page_parser.get_search_book_detail(html)
        return book.to_json_obj()

    def appoint_book(self, call_no, location, check, take_loca='90001', preg_days='30', pregKeepDay='7'):
        html = self.crawler.appoint_book(call_no, location, check, preg_days, take_loca, pregKeepDay)
        if page_parser.is_appoint_success(html):
            return True
        else:
            return False

    def cancel_appoint(self, call_no, marc_no, loca):
        html = self.crawler.cancel_appoint(call_no, marc_no, loca)
        if page_parser.is_cancel_appoint_success(html):
            return True
        else:
            return False

    def renew_book(self, barcode):
        html = self.crawler.renew_book(barcode)
        if page_parser.is_renew_success(html):
            return True
        else:
            return False



if __name__ == '__main__':
    # crawler = page_crawler.PageCrawler('71111229','213113709')
    # html = crawler.get_rendered_book_page()
    # book_table = page_parser.get_render_book_list(html)
    # print book_table

    # html = crawler.get_search_result_page("python")
    # page_parser.get_search_book_list(html)

    # html = crawler.get_search_detail_page('0000804600')
    # page_parser.get_search_book_detail(html)

    # html = crawler.get_appoint_page('0000703988')
    # page_parser.get_appoint_list(html)

    # crawler.renew_book('2612220')

    service = LibraryService('07010115', '199012')
    # service.get_render_book_list('71111229','213113709')
    # service.get_search_result_list("python")
    # service.get_book_detail('0000664599')
    print service.appoint_book('I712.45/488', '607', '1')
    # print service.renew_book('2612220')
    # print service.get_appoint_book_info('0000519601')#('0000664599')
    # print service.get_appointed_books()
    # print service.get_appointed_books()
    # print service.cancel_appoint("I712.45/488", "0000519601", "607")





