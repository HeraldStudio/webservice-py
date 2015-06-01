# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com yml_bright@163.com
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.models.db import engine
from mod.curriculum.term_handler import TermHandler
from mod.curriculum.sidebar_handler import SidebarHandler
from mod.curriculum.curriculum_handler import CurriculumHandler
from mod.simsimi.handler import SIMSIMIHandler
from mod.gpa.gpa_handler import GPAHandler
from mod.pe.handler import PEHandler
from mod.srtp.srtp_handler import SRTPHandler
from mod.card.handler import CARDHandler
from mod.nic.handler import NICHandler
from mod.auth.handler import AuthHandler
from mod.lecture.handler import LectureHandler
from mod.library.listhandler import LibListHandler
from mod.library.renewhandler import LibRenewHandler
from mod.library.searchhandler import LibSearchHandler
from mod.pc.handler import PCHandler
from mod.jwc.handler import JWCHandler
from mod.schoolbus.handler import SchoolBusHandler
from mod.phylab.handler import PhylabHandler
from mod.emptyroom.handler import CommonQueryHandler, QuickQueryHandler
from mod.lecture.noticehandler import LectureNoticeHandler
from mod.user.handler import UserHandler
from mod.stadium.handler import StadiumHandler
import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=7005, help='run on the given port', type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/webserv2/auth', AuthHandler),
            (r'/webserv2/srtp', SRTPHandler),
            (r'/webserv2/term', TermHandler),
            (r'/webserv2/sidebar', SidebarHandler),
            (r'/webserv2/curriculum', CurriculumHandler),
            (r'/webserv2/gpa', GPAHandler),
            (r'/webserv2/pe', PEHandler),
            (r'/webserv2/simsimi', SIMSIMIHandler),
            (r'/webserv2/nic', NICHandler),
            (r'/webserv2/card', CARDHandler),
            (r'/webserv2/lecture', LectureHandler),
            (r'/webserv2/library', LibListHandler),
            (r'/webserv2/renew', LibRenewHandler),
            (r'/webserv2/search', LibSearchHandler),
            (r'/webserv2/phyLab',PhylabHandler),
            (r'/webserv2/pc', PCHandler),
            (r'/webserv2/jwc', JWCHandler),
            (r'/webserv2/schoolbus', SchoolBusHandler),
            (r'/webserv2/phylab', PhylabHandler),
            (r'/webserv2/lecturenotice', LectureNoticeHandler),
            (r'/webserv2/user', UserHandler),
            (r'/webserv2/query/([a-z]{3})/(\d{1,2})/(\d)/(\d{1,2})/(\d{1,2})', CommonQueryHandler),
            (r'/webserv2/query/([a-z]{3})/([a-z]{1,8})/(\d{1,2})/(\d{1,2})', QuickQueryHandler),
            (r'/webserv2/stadium',StadiumHandler),
        ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
