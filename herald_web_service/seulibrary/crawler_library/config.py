
# -*- utf-8 -*-

'''Config info such as urls.

Author: Bing Liu
Date: 2013-08-30
'''

import os


LOGIN_URL = 'http://www.lib.seu.edu.cn:8080/reader/redr_verify.php'

LOGIN_PAGE_URL = "http://www.lib.seu.edu.cn:8080/reader/login.php"

RENDER_BOOK_LIST_URL = 'http://www.lib.seu.edu.cn:8080/reader/book_lst.php'

RENEW_URL = 'http://www.lib.seu.edu.cn:8080/reader/ajax_renew.php?bar_code=%s&time=%s'

SEARCH_URL = 'http://www.lib.seu.edu.cn:8080/opac/'

BOOK_DETAIL_URL = 'http://www.lib.seu.edu.cn:8080/opac/item.php?marc_no='

BOOK_APPOINT_URL = "http://www.lib.seu.edu.cn:8080/opac/userpreg.php?marc_no="

APPOINT_URL = "http://www.lib.seu.edu.cn:8080/opac/userpreg_result.php?"

APPOINTED_URL = "http://www.lib.seu.edu.cn:8080/reader/preg.php"



TIME_OUT = 10

DEVELOP_MODE = False


import logging
import sys
logger = logging.getLogger("running.log")
formatter = logging.Formatter('%(levelname)-6s %(pathname)6s %(funcName)s line:%(lineno)-6s %(asctime)s  %(message)s', '%a, %d %b %Y %H:%M:%S',)
if DEVELOP_MODE:
    handler = logging.StreamHandler(sys.stderr)
else:
    handler = logging.FileHandler(os.path.join(os.getcwd(),"./seulibrary/running.log"))
handler.setFormatter(formatter)
logger.addHandler(handler)






