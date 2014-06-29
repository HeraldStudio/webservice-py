Herald Web API v 2.0
=============


##体育系

1. 获取跑操次数

  Request:

    ```
    URL:

    Method: POST

    Parameters:
      * cardnum - 一卡通号
      * pwd - 密码（可省略，缺省值为一卡通号）
    ```

  Response:

  1. 用户名密码正确直接返回跑操次数。
  2. 用户名密码错误返回 wrong card number or password
  3. 缺少用户名返回 empty card number
  4. 体育系服务器宕机时，如有缓存则返回缓存跑操次数，否则返回 time out

##一卡通

####1. 状态,余额

  Request:

    ```
    URL:

    Method: POST

    Parameters:
      * cardnum - 一卡通号
      * password - 密码（一卡通查询密码）
    ```

  Response:

  1. 用户名密码正确直接返回JSON:{'status':'一卡通状态', 'left':'余额'}。
  2. 用户名密码错误返回 wrong card number or password
  3. 一卡通服务器故障 server error
  
####2. 详单查询

  Request:

    ```
    URL:

    Method: POST

    Parameters:
      * cardnum - 一卡通号
      * password - 密码（一卡通查询密码）
      * timedelta - 时间间隔(天)
    ```

  Response:

  1. 用户名密码正确直接返回JSON:{{'time':'交易时间', 'type':'类型', 'system':'交易子系统', 'dealtype':'交易类型', 'money':'交易金额', 'left':'卡内余额', 'index':'序号', 'status':'状态'}}。
  2. 用户名密码错误返回 wrong card number or password
  3. 一卡通服务器故障 server error
  4. 查询一次需要4-5秒

##网络中心

####1. 网络套餐查询

  Request:

    ```
    URL:

    Method: POST

    Parameters:
      * cardnum - 一卡通号
      * password - 密码（统一身份认证密码）
      * type - 查询类型('a','b','web')
    ```

  Response:

  1. 用户名密码正确直接返回JSON:{'used':'已使用', 'left':'未使用', 'status':'状态'}。
  2. 用户名密码错误返回 wrong card number or password
  3. 未开通服务 disabled
