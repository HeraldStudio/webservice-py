# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

import page_crawler
import page_parser
import custom_exception

LOCAL_TEST_MODE = False


ServerError = "Server Error"
AccountError = "Account Error"
RequestError = "Request Error"

def tyxPc(request, cardNumber, password):
    try:
        html = page_crawler.crawl_paocao_page(cardNumber, password)
        if html == "体育系故障，请稍后再试":
            return HttpResponse("体育系故障，请稍后再试")
        pc_number = page_parser.get_paocao_number(html)
        return HttpResponse(pc_number)
    except custom_exception.AccountError, e:
        return HttpResponse(AccountError)
    except Exception, e:
        return HttpResponse(ServerError)

def check_account(reqeust):
    try:
        try:
            card_number = reqeust.POST['card_number']
            passwd = reqeust.POST['password']
        except:
            return HttpResponse(RequestError)
        state = page_crawler.login(card_number, passwd)
        if state.get_login_status():
            return HttpResponse("True")
        else:
            return HttpResponse("False")
    except Exception,e:
        return HttpResponse(ServerError)

if LOCAL_TEST_MODE:
    BASE_URL = "http://127.0.0.1:8000/herald_web_service/"
else:
    BASE_URL = "http://herald.seu.edu.cn/herald_web_service/"

def test(request):
    return render_to_response("test.html",{"base_url":BASE_URL})

def get_ren_tyb__broadcast(request):
    states = page_crawler.get_ren_tyb()
    today_list = page_parser.get_today_broadcast(states)
    return HttpResponse(json.dumps(today_list, ensure_ascii=False))
