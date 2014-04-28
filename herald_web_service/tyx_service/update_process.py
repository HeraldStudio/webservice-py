# -*- coding: utf-8 -*-

import mysql_class
import page_crawler
import page_parser
import time
import config
import custom_exception
from threading import Timer
from datetime import datetime

COLUMN_YKT = 'xxxx'
COLUMN_PWD = 'xxxx'
ORI_DB_NAME = 'xxx'
ORI_TABLE_NAME = 'xxxx'
AUTO_UPDATE_TIME = 3600 #seconds

def print_log(msg):
    f = open("update_process.log","a+")
    f.write(str(datetime.now())+"\t"+msg+"\n")
    f.close()

def query_tyx(cardNumber,password):
    try:
        html = page_crawler.crawl_paocao_page(cardNumber, password)
        if html == "体育系故障，请稍后再试":
            return "体育系故障，请稍后再试"
        pc_number = page_parser.get_paocao_number(html)
        return pc_number
    except custom_exception.AccountError, e:
        return "AccountError"
    except Exception, e:
        return "ServerError"

def update_paocao(result):
    global COLUMN_YKT,COLUMN_PWD,ORI_DB_NAME,ORI_TABLE_NAME
    db = mysql_class.MySQL(config.DB_HOST,config.DB_USER,config.DB_USER_PWD,config.DB_PORT)
    db.selectDb(ORI_DB_NAME)
    query_result=[]
    for p in result:
        x={}
        db.query("select %s from %s where %s = '%s'"%(COLUMN_PWD,ORI_TABLE_NAME,COLUMN_YKT,p['ykt']))
        result = db.fetchAll()
        re = query_tyx(p['ykt'],result[0][COLUMN_PWD])
        if re.isdigit():
            x['ykt']=p['ykt']
            x['num']=re
            x['query_date']=int(time.time())
            query_result.append(x)
        time.sleep(1)
    return query_result

def paocao_refresh():
    global AUTO_UPDATE_TIME
    print_log("Process start")
    db = mysql_class.MySQL(config.DB_HOST,config.DB_USER,config.DB_USER_PWD,config.DB_PORT)
    db.selectDb(config.DB_PAOCAO_BUFF)
    db.query("select * from buff_paocao where ykt = '0'")
    result = db.fetchAll()
    if result[0]['num']=='1':
        db.query("select count(*) from buff_paocao where query_date < %s" % result[0]['query_date'])
        count = db.fetchAll()
        print_log("Count:%s"%count[0]['count(*)'])
        for i in range(0,int(count[0]['count(*)']),1000):
            db.query("select ykt from buff_paocao where query_date < %s limit %d,1000" % (result[0]['query_date'],i))
            res = db.fetchAll()
            ret = update_paocao(res)
            for _update in ret:
                db.update("buff_paocao", _update, "ykt = '%s'" % _update['ykt'])
            db.commit()
            print_log("Success:%d"%len(ret))
    print_log("Process end")
    t=Timer(AUTO_UPDATE_TIME,paocao_refresh)
    t.start()

if __name__ == "__main__": 
    paocao_refresh()
