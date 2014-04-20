# -*- coding: utf-8 -*-

import mysql_class
import page_crawler
import page_parser
import time
import custom_exception
import config


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

def refresh_status(result):
    n = int(time.time())
    lastRefresh = int(result[0]['query_date'])
    #print n - lastRefresh
    if (n - lastRefresh) > config.REFRESH_TIME or result[0]['num']=='1':
        return len(result)
    else:
        return 0

def query_paocao(cardNumber,password):
    cardNumber = str(int(cardNumber))
    if cardNumber == 0:
        return 0

    db = mysql_class.MySQL(config.DB_HOST,config.DB_USER,config.DB_USER_PWD,config.DB_PORT)
    db.selectDb(config.DB_PAOCAO_BUFF)
    db.query("select * from buff_paocao where ykt = '0' or ykt = "+cardNumber)
    result = db.fetchAll()
    
    status = refresh_status(result)
    print result,status
    if status == 0:
    	return result[1]['num']
    elif status==1:
        re = query_tyx(cardNumber,password)
        if re.isdigit():
            db.update("buff_paocao",{'query_date':time.time()},"ykt = 0")
            db.insert("buff_paocao",{'ykt':cardNumber,'num':re,'query_date':time.time()})
    else:
        re = query_tyx(cardNumber,password)
        if re.isdigit():
            db.update("buff_paocao",{'query_date':time.time()},"ykt = 0")
            if re!=result[1]['num']:
                db.update("buff_paocao",{'num':1},"ykt = 0")
                db.update("buff_paocao",{'num':re,'query_date':time.time()},"ykt = "+cardNumber)	
            else:
                db.commit()
                return result[1]['num']
    db.commit()
    return re
 	 	
if __name__ == "__main__":
    print query_paocao("213120498","07012229")
 	 		
