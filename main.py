# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com
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
import tornado.web
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=7005, help='run on the given port', type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/service/auth', AuthHandler),
            (r'/service/srtp', SRTPHandler),
            (r'/service/term', TermHandler),
            (r'/service/sidebar', SidebarHandler),
            (r'/service/curriculum', CurriculumHandler),
            (r'/service/gpa', GPAHandler),
            (r'/service/pe', PEHandler),
            (r'/service/simsimi', SIMSIMIHandler),
            (r'/service/nic', NICHandler)
        ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))


class TestHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('HELLO')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
