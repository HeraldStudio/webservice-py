
# -*- encoding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import json
import datetime

import page_crawler
import custom_exception


class LoginState:
    def __init__(self, status, opener):
        self.__status =   status
        self.__opener = opener

    def get_login_status(self):
        return self.__status

    def get_opener(self):
        return self.__opener


def get_paocao_number(html):
    '''
    Raises:
        custom_exception.ParseException
    '''
    try:
        soup = BeautifulSoup(html)
        table = soup.findAll("td", {"class": "Content_Form"})
        pc = table[-1].text
        return pc
    except:
        raise custom_exception.ParseException("跑操次数页面")

def get_today_broadcast(states_str):
    obj = json.loads(states_str)
    states = obj['response']
    today_states = []
    for state in states:
        t_tr = state['createTime']
        t = datetime.datetime.strptime(t_tr, '%Y-%m-%d %H:%M:%S')
        # n_tr = "2013-9-13 12:30:30"
        # n = datetime.datetime.strptime(n_tr, '%Y-%m-%d %H:%M:%S')
        n = datetime.datetime.now()
        if t.year == n.year and t.month == n.month and t.day == n.day:
            today_states.append(state)
    return today_states


if __name__ == "__main__":
    # html = page_crawler.crawl_paocao_page("213102847", "213102847")
    # pc = get_paocao_number(html)
    # print pc
    states_str = page_crawler.get_ren_tyb()
    print get_today_broadcast(states_str)[0]




