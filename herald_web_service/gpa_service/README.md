绩点信息服务
==========
**请求**
```
POST http://121.248.63.105/herald_web_service/gpa/gpa
```
**参数**
username 用户名（一卡通）
password 密码

** 返回 **
```JSON
[{"name": "\u6570\u5b57\u7535\u8def\u5b9e\u9a8c\uff089\u7cfb\uff09", "extra": "", "score_type": "\u9996\u4fee", "credit": "1.0", "semester": "13-14-2", "score": "\u826f"}, {"name": "\u4f53\u80b2\u2162", "extra": "", "score_type": "\u9996\u4fee", "credit": "0.5", "semester": "13-14-2", "score": "86"}]
```
失败是返回
```
userName or password error
```
