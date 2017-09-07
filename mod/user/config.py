# -*- coding: utf-8 -*-
# @Date    : 2015-03-19 16:34:57
# @Author  : yml_bright@163.com


CHECK_URL = "http://my.seu.edu.cn/userPasswordValidate.portal"
# DETAIL_URL = "http://my.seu.edu.cn/index.portal?.pn=p3447_p3449"
URL = "http://my.seu.edu.cn/index.portal?.pn=p1681"

DETAIL_URL = "http://my.seu.edu.cn/pnull.portal?rar=0.6724089304070995&.pmn=view&action=showItem&.ia=false&.pen=pe632&itemId=239&childId=241&page=1"

TIME_OUT = 8


# NEW CHECK_URL
NEW_CHECK_URL = "https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal"
USER_INDEX = "http://my.seu.edu.cn/index.portal"
USER_INFO_URL = "http://my.seu.edu.cn/pnull.portal?rar=0.8130648320195498&.pmn=view&action=showItem&.ia=false&.pen=pe575&itemId=239&childId=241&page=1"
POST_DATA = {
	'lt': '',
	'dllt': 'userNamePasswordLogin',
	'execution': '',
	'_eventId': 'submit',
	'rmShown': '1',
	'password': '',
	'username': ''
}
