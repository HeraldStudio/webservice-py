About Course Crawler
======
从[教务处全校课表](http://xk.urp.seu.edu.cn/jw_service/service/academyClassLook.action)获取所有的课程信息，信息本身不完整，加上未涵盖研究生，信息并不全面，无法保证准确度  

服务器上的python库不全，脚本无法执行，可以先在自己的机器上获取然后export，用ftp传到106进行source（记得清空原数据，用脚本或者SQL都行）

####1.操作
```
python courseCrawler.py cmd

eg: python courseCrawler.py -h
# 获取帮助文档
```

脚本通过读取配置文件(**crawler_conf.json**)来确定获取的数据的存放位置，可指定主机名(host)，用户名(user)，用户密码(pwd)，数据库名(db_name)以及爬取的是第几学期(term)  

使用的数据库为MySQL，表的**格式**和**表名**已硬编码。。具体查看course.sql


####2.BUGs
a)脚本对异常的处理并未具体去考虑。。。Error定位可能不直观

b)...