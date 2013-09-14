
# -*- encoding: utf-8 -*-



class AccountError(Exception):
    def __init__(self):
        self.__error_info = "用户名或密码错误"
        Exception.__init__()

    def __str__(self):
        return "AccountError: " + self.__error_info

    def __repr__(self):
        return "AccountError()"

class ParseException(Exception):
    def __init__(self, page):
        self.__page_name = page
        self.__error_info = "error occured when parse "+page

    def __str__(self):
        return self.__error_info

    def __repr__(self):
        return "ParseException('"+self.__page_name+"')"




