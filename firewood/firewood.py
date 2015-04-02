# coding:utf-8

import os
from mapletree import MapleTree, rsp, compat
from mapletree.helpers.stagelocal import StageLocal
from mapletree.helpers.threadlocal import ThreadLocal
from . import logger
from .temptoken import TempToken


class Firewood(MapleTree):
    def __init__(self):
        super(Firewood, self).__init__()
        self._autoloads.extend(['firewood.defaults'])

        self.stage_f = lambda: os.environ.get('STAGE', 'development')
        self._stagelocal = None
        self._threadlocal = None

    def __call__(self, environ, start_response):
        try:
            return super(Firewood, self).__call__(environ, start_response)

        except:
            logger.tb()
            start_response('500 Internal Server Error', [])
            return [compat.non_unicode_str('')]

    @property
    def config(self):
        if self._stagelocal is None:
            self._stagelocal = StageLocal()

        return self._stagelocal

    @property
    def thread(self):
        if self._threadlocal is None:
            self._threadlocal = ThreadLocal()

        return self._threadlocal

    @property
    def rsp(self):
        return rsp()

    def build(self):
        self.config.stage = self.stage_f()
        super(Firewood, self).build()

    def get(self, path):
        return self.req.get(path)

    def post(self, path):
        return self.req.post(path)

    def put(self, path):
        return self.req.put(path)

    def delete(self, path):
        return self.req.delete(path)

    def head(self, path):
        return self.req.head(path)

    def options(self, path):
        return self.req.options(path)

    def patch(self, path):
        return self.req.patch(path)

    def exception(self, exc_cls):
        return self.exc.route(exc_cls)
