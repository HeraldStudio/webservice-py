# Create your views here.
# -*- encoding:utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

from crawler_library import library_service, config
from crawler_library import custom_exception



REQUEST_PARAMS_ERROR = "request params error"
REQUEST_POST_ERROR = "request post data error"
SERVER_ERROR = "server error"
ACOUNT_ERROR = "username or password error"

ROOT_URL = "http://herald.seu.edu.cn/herald_web_service/"


def instruction(request):
    #return HttpResponse("test")
    if config.LOCAL_TEST_MODE:
        base_url = "http://localhost:8000/herald_web_service/library"
    else:
        base_url = ROOT_URL + "library"
    return render_to_response("instruction.html",{'base_url':base_url})


def search_book(request):
    service = library_service.LibraryService()
    try:
        strText = request.GET["strText"]
    except Exception,e:
        return HttpResponse(REQUEST_PARAMS_ERROR)
    
    try:
        page = request.GET["page"]
    except Exception,e:
        config.logger.error(e)
        page = None
        
    try:  
        if page:
            book_list = service.get_search_result_list(strText, page)
        else:
            book_list = service.get_search_result_list(strText)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps(book_list, ensure_ascii=False))

def book_detail(request):
    service = library_service.LibraryService()

    try:
        marc_no = request.GET["marc_no"]
    except Exception,e:
        return HttpResponse(REQUEST_PARAMS_ERROR)
    
    try:
        book_detail = service.get_book_detail(marc_no)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps(book_detail, ensure_ascii=False))

def check_render_books(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        books = service.get_render_book_list()
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps(books, ensure_ascii=False))

def renew_book(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        barcode = request.POST["barcode"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        result = service.renew_book(barcode)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR+str(e))
    
    return HttpResponse(json.dumps({"result":result}))


def check_appointed_books(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        books = service.get_appointed_books()
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps(books,ensure_ascii=False))

def cancel_appoint(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        call_no = request.POST["call_no"]
        marc_no = request.POST["marc_no"]
        loca = request.POST["loca"]
    except:
        return HttpResponse(REQUEST_POST_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        result = service.cancel_appoint(call_no, marc_no, loca)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps({'result':result}))

def appoint_info(request):
    try:
        username = request.POST["username"]
        passwd = request.POST["password"]
        marc_no = request.POST['marc_no']
    except:
        return HttpResponse(REQUEST_PARAMS_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        detail = service.get_appoint_book_info(marc_no)
        #detail = service.get_appoint_book_info('0000519601')
        print detail
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        #print e
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps(detail, ensure_ascii=False))

def appoint_book(request):
    try:
        #callnol, location, check, take_loca='90001'
        username = request.POST["username"]
        passwd = request.POST["password"]
        call_no = request.POST["call_no"]
        location = request.POST["location"]
        check = request.POST["check"]
        take_loca = request.POST['take_loca']
    except:
        return HttpResponse(REQUEST_POST_ERROR)
    
    service = library_service.LibraryService(username, passwd)
    try:
        result = service.appoint_book(call_no, location, check, take_loca)
    except custom_exception.LoginException:
        return HttpResponse(ACOUNT_ERROR)
    except Exception,e:
        print e
        config.logger.error(e)
        return HttpResponse(SERVER_ERROR)
    
    return HttpResponse(json.dumps({"result":result}))


        


if __name__=="__main__":
    import os
    p = os.path.join(os.getcwd(),"name.txt")
    print p

