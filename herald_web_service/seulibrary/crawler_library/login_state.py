
# -*- utf-8 -*-

'''Better record login result.

Author: Bing Liu
Date: 2013-08-30
'''

class LoginState:
    '''A data structure combining status(success or fail) and opener(containing cookie info).

    Attributes:
        status: a boolean data, if login successfully, it is true, else it will be false
        opener: builded by urllib2.build_opener() and it contains the cookie info.
    '''
    def __init__(self, st, op):
        '''
        Args:
            st: status, boolean type
            opener: the obj containing cookie info.
        '''

        self.status = st
        self.opener = op

    def get_status(self):
        return self.status

    def get_opener(self):
        return self.opener

    def __str__(self):
        return str(self.status)
