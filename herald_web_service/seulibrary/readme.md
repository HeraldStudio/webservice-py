# library service

**演示页面请访问:**[http://121.248.63.105/herald_web_service/library/instruction/]('http://121.248.63.105/herald_web_service/library/instruction/')

**响应结果说明：**

* 正常返回结果使用json格式。
* 错误响应：
	* REQUEST_PARAMS_ERROR = "request_params_error"
	* REQUEST_POST_ERROR = "request_post data_error"
	* SERVER_ERROR = "server_error"
	* ACOUNT_ERROR = "username_or_password_error"
* 返回结果不做过多解释，可结合图书馆网站进行理解。

## 1. 图书搜索
* url：`http://121.248.63.105/herald_web_service/library/search_book/`
* 方法：GET
* 参数：
    * "strText"，搜索内容，必填。
    * "page"，搜索结果页码，选填，默认1
* 返回结果：
    * 搜索结果样例：
	
		```json
		[
			{
			"publisher": "机械工业出版社2012", 
			"lendable_num": "0", 
			"isbn": "TP311.56/888", 
			"title": "Python入门经典:以解决计算问题为导向的Python编程实践", 
			"author": "(美) William F. Punch, Richard Enbody著", 
			"marc_no": "0000868408", 
			"doctype": "中文图书", 
			"store_num": "3"
			},
		]
		```
    * 错误：`REQUEST_PARAMS_ERROR`、`SERVER_ERROR`

* 结果中可用项：
	* 'marc_no':查看书的详情时作为参数。


## 2. 查看某本书的详情
* url：`http://121.248.63.105/herald_web_service/library/book_detail/`
* 方法：GET
* 参数：
    * "marc_no"，书的某种编号，必填。
* 返回结果：
    * 搜索结果样例：
	
		```json
		{
			"stores": [
				{
					"call_no": "TP311.56/888", 
					"barcode": "2643096", 
					"room": "中文图书阅览室（4）", 
					"lendable": "借出-应还日期：2013-09-18", 
					"years": "2012.08 -", 
					"campus": "九龙湖校区"
				}, 
				{
					"call_no": "TP311.56/888", 
					"barcode": "2643097", 
					"room": "中文图书阅览室（4）", 
					"lendable": "借出-应还日期：2013-09-23", 
					"years": "2012.08 -", "campus": "九龙湖校区"
				}, 
				{
					"call_no": "TP311.56/888", 
					"barcode": "2643095", 
					"room": "中文保存本阅览室", 
					"lendable": "保留本", 
					"years": "2012.08 -", 
					"campus": "九龙湖校区"
				}
			], 
			"detail": {
				"学科主题:": "软件工具-程序设计", 
				"出版发行项:": "北京:机械工业出版社,2012", 
				"载体形态项:": "452页:图24cm", 
				"题名/责任者:": "Python入门经典:以解决计算问题为导向的Python编程实践/(美) William F. Punch, Richard Enbody著 张敏等译", 
				"统一题名:": "Practice of computing using Python", 
				"中图法分类号:": "TP311.56", 
				"出版发行附注:": "由Pearson Education授权机械工业出版社出版发行", 
				"个人次要责任者:": "张敏 译", 
				"责任者附注:": "责任者(Punch)规范汉译姓: 庞奇 ; 责任者(Enbody)汉译姓取自在版编目: 尹鲍德", 
				"个人责任者:": "尹鲍德 (Enbody, Richard) 著", 
				"版本附注:": "据2011年英文版译出", 
				"ISBN及定价:": "978-7-111-39413-6/CNY79.00", 
				"其它题名:": "以解决计算问题为导向的Python编程实践", 
				"丛编项:": "华章程序员书库"
			}
		}
		```
    * 错误：`REQUEST_PARAMS_ERROR`、`SERVER_ERROR`

* 结果中可用项：无

## 3. 查看借书
* url：`http://121.248.63.105/herald_web_service/library/rendered_books/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填。
* 返回结果：
    * 搜索结果样例：
	
		```json
		[
			{
				"render_date": "2013-06-05", 
				"due_date": "2013-10-03", 
				"adjunct": "无", 
				"place": "中文图书阅览室（4）", 
				"author": "(美) Doug Hellmann著", 
				"title": "Python标准库", 
				"barcode": "2612220", 
				"renew_time": "1"
			}
		]
		```
    * 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：
	* 'barcode':续借时作为参数。

## 4. 续借
* url：`http://121.248.63.105/herald_web_service/library/renew/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填；
    * "barcode"，某种编号，必填。
* 返回结果：
    * 搜索结果样例：
	
		```json
		{"result": false}
		```
	* 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：无

## 5. 查看已经预约的书：
* url：`http://121.248.63.105/herald_web_service/library/appointed_books/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填。
* 返回结果：
    * 搜索结果样例：
	
		```json
		[
			{
				"status": "申请中", 
				"call_no": "I712.45/488", 
				"appoint_date": "2013-09-05", 
				"place": "有丰文苑（九龙湖A500)", 
				"title": "追风筝的人", 
				"data": {"call_no": "I712.45/488", 
				"loca": "607 ", 
				"marc_no": "0000519601"
			},
		]
		```
    * 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：
	在取消预约时有用
	* 'call_no'，索书号
	* 'marc_no'，某种编号
	* 'loca'，馆藏地

## 6. 取消预约的书
* url：`http://121.248.63.105/herald_web_service/library/cancel_appoint/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填；
	* 'call_no'，索书号，必填；
	* 'marc_no'，某种编号，必填；
	* 'loca'，馆藏地，必填。
* 返回结果：
    * 结果样例：
	
		```json
		{"result": true}
		```
    * 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：无

## 7. 书的预约状况（区别于已经预约的书，是书详情页面里面出现的预约）
* url：`http://121.248.63.105/herald_web_service/library/appoint_info/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填；
	* 'marc_no'，某种编号，必填；
* 返回结果：
    * 结果样例：
	
		```json
		[
			{
				"call_no": "I712.45/488", 
				"lendable_num": "2", 
				"appoint_info": "您已经达到最大预约数！不得预约！", 
				"room_num": "607", 
				"room": "有丰文苑（九龙湖A500)", 
				"in_num": "0", 
				"appointable": "disabled", 
				"appoint_count": "0", 
				"take_place": ["90001", "00916", "00940"]
			}
		]
		```
    * 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：
	预约操作时有用
	* 'call_no'，索书号
	* 'room_num'，馆藏地编号
	* 'take_place'，取书地点
	* 潜在有用信息：书在可预约书列表中的序号。

## 8. 预约
* url：`http://121.248.63.105/herald_web_service/library/appoint_book/`
* 方法：POST
* 参数：
    * "username"，用户名，必填；
    * "password"，密码，必填；
	* 'call_no'，索书号，必填
	* 'room_num'，馆藏地编号，必填，
	* 'take_place'，取书地点，必填。
	* 'check'，第几本，必填（书预约状况中可预约的书列表的第几个，从html源码中的<check>标签得来）。
* 返回结果：
    * 结果样例：
	
		```json
		{"result": true}
		```
    * 错误：`REQUEST_POST_ERROR`、`SERVER_ERROR`、`ACOUNT_ERROR`

* 结果中可用项：无

## 其他说明
* 馆藏地编号和校区编号由图书馆代码得来，take_loca: 90001-九龙湖总借还处, 00916-丁家桥中文借书处, 00940-四牌楼总借还处。


