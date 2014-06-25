# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com
from sqlalchemy.orm import scoped_session, sessionmaker
from mod.models.db import engine
from mod.pe.handler import PEHandler
import tornado.web
import tornado.ioloop


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', PEHandler)
        ]
        settings = dict(
            cookie_secret="7CA71A57B571B5AEAC5E64C6042415DE",
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class TestHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('HELLO')

if __name__ == '__main__':
    Application().listen(8000)
    tornado.ioloop.IOLoop.instance().start()
