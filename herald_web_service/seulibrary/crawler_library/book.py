
# -*- encoding: utf-8 -*-

'''Some book class

Author: Bing Liu
Date: 2013-08-31
'''

class BookRenderItem:
    '''Book object in rendered book  page.

    '''
    def __init__(self, barcode, title, author, render_date, due_date, renew_time, place, adjunct):
        self.__barcode = str(barcode)
        self.__title = str(title)
        self.__author = str(author)
        self.__render_date = str(render_date)
        self.__due_date = str(due_date)
        self.__renew_time = str(renew_time)
        self.__place = str(place)
        self.__adjunct = str(adjunct)

    def __str__(self):
        return '\n条码号:' + str(self.__barcode) + \
            '\n责任者:' + self.__author + \
            '\n题名:' + self.__title + \
            '\n借阅日期:' + self.__render_date + \
            '\n应还日期:' + self.__due_date + \
            '\n续借次数:' + self.__renew_time + \
            '\n馆藏地:' + self.__place + \
            '\n附件:' + self.__adjunct

    def to_json_obj(self):
        return {"barcode":self.__barcode, "title":self.__title, "author":self.__author,
                "render_date":self.__render_date, "due_date":self.__due_date, "renew_time":self.__renew_time,
                "place":self.__place, "adjunct":self.__adjunct }




class BookSearchItem:
    def __init__(self,marc_no, title, doctype, isbn, author, publisher, store_num, lendable_num):
        self.__marc_nol = marc_no
        self.__title = title
        self.__doctype = doctype
        self.__isbn = isbn
        self.__author = author
        self.__publisher = publisher
        self.__store_num = store_num
        self.__lendable_num = lendable_num

    def __str__(self):
        return '\nmarc_no :' + self.__marc_nol + \
            '\n书名:' + self.__title + \
            '\n责任者:' + self.__author + \
            '\n文档类型:' + self.__doctype + \
            '\nisbn: ' + self.__isbn + \
            '\n出版社:' + self.__publisher + \
            '\n馆藏副本' + self.__store_num + \
            '\n可借副本' + self.__lendable_num

    def to_json_obj(self):
        return {"marc_no":self.__marc_nol, "title":self.__title, "doctype":self.__doctype,
                "isbn":self.__isbn, "author":self.__author, "publisher":self.__publisher,
                "store_num":self.__store_num, "lendable_num":self.__lendable_num }


class BookSearchDetail:
    '''Book detail.

    Attributes:
        __detail: dict type, used to keep detail info of a book.
    '''
    def __init__(self):
        self.__detail = {}
        self.__stores = []

    def add_info(self, k, v):
        if type(k) == unicode:
            key = k.encode('utf-8')
        else:
            key = str(k)
        if type(v) == unicode:
            value = v.encode('utf8')
        else:
            value = str(v)
        self.__detail[key] = value

    def add_store(self, store):
        self.__stores.append(store)

    def __str__(self):
        s = ''
        for item in self.__detail:
            s += ('\n' + item + self.__detail[item])
        for store in self.__stores:
            s += str(store)
        return s

    def to_json_obj(self):
        return {"detail":self.__detail, "stores":[store.to_json_obj() for store in self.__stores] }

class BookStore:
    def __init__(self, call_no, barcode, years, campus, room, lendable):
        '''String type inputs are exptected

        '''
        self.__call_no = call_no
        self.__barcode = barcode
        self.__years = years
        self.__campus = campus
        self.__room = room
        self.__lendable = lendable

    def __str__(self):
        s = '\n索书号:' + self.__call_no + \
            '\n条码号:' + self.__barcode + \
            '\n年卷期:' + self.__years + \
            '\n校区:' + self.__campus + \
            '\n馆藏地:' + self.__room + \
            '\n书刊状态:' + self.__lendable
        return s

    def to_json_obj(self):
        return {"call_no":self.__call_no, "barcode":self.__barcode, "years":self.__years,
                "campus":self.__campus, "room":self.__room, "lendable":self.__lendable }


class AppointInfoItem:
    '''

    Distributions:
        __take_place: 90001 九龙湖总借还处, 00916 丁家桥中文借书处, 00940 四牌楼总借还处
    '''
    def __init__(self, call_no, room, room_num, lendable_num, in_num, appoint_count,
                 appointable_info, take_place, appointable):
        self.__call_no = call_no
        self.__room = room
        self.__room_num = room_num
        self.__lendable_num = lendable_num
        self.__in_num = in_num
        self.__appoint_count = appoint_count
        self.__appointable_info = appointable_info
        self.__take_place = take_place
        self.__appointable = appointable

    def __str__(self):
        s = '\n索书号:' + self.__call_no + \
            '\n馆藏地:' + self.__room + \
            '\n馆藏地编号:' + self.__room_num + \
            '\n可借副本:' + self.__lendable_num + \
            '\n在馆副本:' + self.__in_num + \
            '\n已预约数:' + self.__appoint_count + \
            '\n可否预约:' + self.__appointable_info + \
            '\n取书地:'
        for p in self.__take_place:
            s += (p+'; ')
        s += '\n能否预约:' + self.__appointable
        return s

    def to_json_obj(self):
        return {"call_no":self.__call_no, "room":self.__room, "room_num":self.__room_num,
                "lendable_num":self.__lendable_num, "in_num":self.__in_num, "appoint_count":self.__appoint_count,
                "appoint_info":self.__appointable_info, "appointable":self.__appointable,
                "take_place":self.__take_place}


class AppointedBookItem:
    def __init__(self, call_no, title, author, place, appoint_date, cancel_date, take_location, status, data={}):
        self.__call_no = call_no
        self.__title = title
        self.__author = author
        self.__place = place
        self.__appoint_date = appoint_date
        self.__cancel_date = cancel_date
        self.__take_location = take_location
        self.__status = status
        self.__data = data

    def set_data(self, data):
        self.__data = data


    def __str__(self):
        return "\n索书号:" + self.__call_no + \
            "\n题名:" + self.__title + \
            '\n责任者:' + self.__author + \
            '\n馆藏地:' + self.__place + \
            '\n预约(到书)日:' + self.__appoint_date + \
            '\n截止日期:' + self.__cancel_date + \
            '\n取书地:' + self.__take_location + \
            "\n状态:" + self.__status + \
            "\ndata:" + str(self.__data)

    def to_json_obj(self):
        return {"call_no":self.__call_no, "title":self.__title, "author":self.__author,
                "place":self.__place, "appoint_date":self.__appoint_date, "cancel_date":self.__cancel_date,
                "take_location":self.__take_location, "status":self.__status, "data":self.__data }










