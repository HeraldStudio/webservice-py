# -*- coding: utf-8 -*-
# @Date    : 2016-03-24 16 16:34:57
# @Author  : jerry.liangj@qq.com

method = {
        'getDate':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/initOrderIndexP.do?sclId=1',
            'method':'GET',
            'param':[]
        },
        'myOrder':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/fetchMyOrdersP.do?sclId=1',
            'method':'GET',
            'param':[]
        },
        'cancelUrl':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/delOrderP.do?sclId=1',
            'method':'GET',
            'param':[]
        },
        'getOrder':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/phoneOrder/getOrderInfoP.do?sclId=1',
            'method':'GET',
            'param':['itemId','dayInfo']
        },
        'judgeOrder':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/judgeOrderP.do?sclId=1',
            'method':'GET',
            'param':['itemId','dayInfo','time']
        },
        'getPhone':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/initEditOrderP.do?sclId=1',
            'method':'GET',
            'param':[]
        },
        'getFriendList':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/searchUserP.do?sclId=1&pageNumber=1&start=0&pageSize=5',
            'method':'GET',
            'param':['cardNo']
        },
        'new':{
            'url':'http://yuyue.seu.edu.cn/eduplus/phoneOrder/insertOredrP.do?sclId=1',
            'method':'GET',
            'param':['orderVO.useMode','orderVO.useTime','orderVO.itemId','orderVO.phone','useUserIds']
        }
 }

