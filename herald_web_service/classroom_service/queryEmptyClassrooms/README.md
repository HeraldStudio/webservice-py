关于API维护
======

新学期到来需要的更新

###1.修改TERM
修改queryEmptyClassrooms/settings.py第8行的TERM为当前学期，短学期未测试过。。。
```
TERM = '13-14-3'
```

###2.修改START_DATE
修改queryEmptyClassrooms/settings.py第10～12行的内容
```
# 13-14-3学期第一周周一的日期
START_YEAR = 2014
START_MONTH = 2
START_DAY = 24
```
