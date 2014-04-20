#体育系跑操查询
----

##跑操次数查询

* url：`http://herald.seu.edu.cn/herald_web_service/tyx/一卡通/密码/`
* 请求方法：GET
* 请求参数：无
* 响应：
    * 正确响应：跑操次数
    * 异常：Account Error, Server Error

## 验证账号正确性
* url: `http://herald.seu.edu.cn/herald_web_service/tyx/checkAccount/`
* 请求方法：POST
* 请求参数：
    * card_number:一卡通号
    * password：体育系密码
* 响应：
    * 正确响应：True、False
    * 异常：Server Error, Request Error

## 获取人人网体育部主页状态
返回请求**当天**体育部已发状态

* url:`http://herald.seu.edu.cn/herald_web_service/tyx/tyb_broadcast/`
* 请求方法：GET
* 请求参数：无
* 响应：
    * 正确响应：json格式的状态数据，见下面样例
    * 异常：Server Error

**json格式的结果样例**（内容中日期不是同一天不代表实际返回的不是同一天，实际返回只返回当天状态）：
```json
[
	{
	    "id": 4992448728, 
	    "content": "【跑操信息】大一大二滴亲们，主页菌提醒乃们，下周一开始要跑早操了(th)(th) 快快调整好自己的生物钟，咱们要一鼓作气，速速跑完(酷)(酷) 大一的孩纸有问题可以戳菌菌呐(走你)(走你) 九龙湖校区早操时间6：40～7：20， 不要赖床呦～(吻)(吻)", 
	    "createTime": "2013-9-13 9:51:27", 
	    "shareCount": 33, 
	    "commentCount": 19, 
	    "ownerId": 601258593, 
	    "sharedStatusId": 0, 
	    "sharedUserId": 0
	}, 
    {
        "id": 4990093678, 
        "content": "欢迎大家加入体育部呐(可爱)(可爱)～转自东南大学学生会:【SU 招新资讯】大一的亲们~昨晚有收到我们送的惊喜么~没有收到的亲们不要着急，我们今天会继续发送~(走你)(走你)再次提醒我们提交报名表有线下提交和现场提交两种方式呦~(th)东南大学学生会有爱的大家庭真诚期待你的加入~(吻)(吻)", 
        "createTime": "2013-9-11 14:27:46", 
        "shareCount": 2, 
        "commentCount": 2, 
        "ownerId": 601258593, 
        "sharedStatusId": 4989871580, 
        "sharedUserId": 600088527
    }, 
]
```

## 剩余可跑操天数
* url: `http://herald.seu.edu.cn/herald_web_service/tyx/remain_days/`
* 请求方法：GET
* 请求参数：无
* 响应：一个数字，表示本学期剩余可跑操天数

