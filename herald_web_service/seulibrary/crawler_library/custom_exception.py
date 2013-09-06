
# -*- encoding: utf-8 -*-

class LoginException(Exception):
    def __init__(self, value='Please check username and password.'):
        self.__value = value

    def __str__(self):
        return "LoginException: "+self.__value

    def __repr__(self):
        return "LoginException('"+self.__value+"')"

class ParseException(Exception):
    def __init__(self,page_name=''):
        self.__page_name = page_name
        self.__error_info = "Error occured when parse page:" + page_name

    def __str__(self):
        return "ParseException: "+self.__error_info

    def __repr__(self):
        return "ParseException('"+self.__page_name+"')"

class RequestException(Exception):
    def __init__(self,e):
        self.__error = e

    def __str__(self):
        return self.__error






