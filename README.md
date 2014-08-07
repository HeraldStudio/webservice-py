##先声web-service文档
---

###SRTP

```
URL :`http://121.248.63.105/service/srtp`
Method : POST
Params : {"number":"10211105"}
Response : [
  {
    "score": "优", 
    "total": "8.0", 
    "name": "XXX\r\n", 
    "card number": "10211106"
  }, 
  {
    "credit": "1.8", 
    "proportion": "30%", 
    "project": "半导体纳米结构中电磁诱导透明效应研究 (13102008) 良好", 
    "department": "物理系", 
    "date": "2013年11月", 
    "type": "SRTP项目", 
    "total credit": "6.0"
  }
  ...
]
```

###Term(课表学期)

```
URL: http://121.248.63.105/service/term
Method: POST
Response:
[
  "14-15-1", 
  "13-14-3", 
  "13-14-2", 
  "13-14-1", 
  "12-13-3", 
  "12-13-2", 
  "12-13-1"
]
```

###Sidebar(课表侧边栏)

```
URL: http://121.248.63.105/service/sidebar
Method: POST
Params: {"cardnum":"213111111","term":"14-15-1"}
Response:
[
  {
    "lecturer": "", 
    "course": "实习", 
    "week": "2-4", 
    "credit": "1"
  }
]
```

###Curriculum(课程信息)

```
URL:http://121.248.63.105/service/curriculum
Method:POST
Params:{"cardnum":"213111010","term":"13-14-2"}
Response:
{
  "Mon": [
    [
      "非线性光学", 
      "[1-16周]3-4节", 
      "九龙湖教一-303"
    ]
  ], 
  "Tue": [
    [
      "固体物理A", 
      "[1-16周]3-4节", 
      "九龙湖教四-302"
    ], 
    [
      "光电检测技术", 
      "[1-16周]6-7节", 
      "九龙湖教二-312"
    ]
  ], 
  ...
}
```
###GPA(绩点信息)

```
URL: http://121.248.63.105/service/gpa
Method:POST
Params:{"username":"一卡通号","password":"统一身份认证密码"}
Response:会出现timeout，有待测试。
```
###PE(体育系信息)

```
URL: http://121.248.63.105/service/pe
Method:POST
Params:{"cardnum":"一卡通号","pwd":"体育系密码"}
Response:跑操次数
```
###Simsim(机器人聊天)

```
URL: http://121.248.63.105/service/simsimi
Method:POST
Params:{"msg":"信息"}
Response:有待测试

```