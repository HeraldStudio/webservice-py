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

