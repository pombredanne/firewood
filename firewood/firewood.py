# coding:utf-8

import inspect
import os
import sys
from importlib import import_module
from mapletree import MapleTree, rsp
from mapletree.driver import Driver
from mapletree.request import Request
from mapletree.response import Response
from mapletree.routetree import ExceptionTree, RequestTree
from mapletree.signing import Signing
from . import logger


class Firewood(object):
    def __init__(self):
        self.mapletree = MapleTree()

        self.req_reusables = {'': set(['firewood.default.req'])}
        self.exc_reusables = set(['firewood.default.exc'])

        self.autoloads = set(['firewood.default.session', 'routes'])

        self.session_key = None
        self._signing = None

    @property
    def signing(self):
        if self._signing is None:
            if self.session_key is not None:
                self._signing = Signing(self.session_key)

            else:
                raise Exception('fw.session_key must be configured')

        return self._signing

    @property
    def rsp(self):
        return rsp()

    @property
    def config(self):
        return self.mapletree.config

    @property
    def thread(self):
        return self.mapletree.thread

    def __call__(self, environ, start_response):
        try:
            return self.mapletree(environ, start_response)

        except:
            logger.tb()
            start_response('500 Internal Server Error', [])
            return ''

    def run(self, background=False):
        target = os.path.dirname(os.path.abspath(sys.argv[0]))
        driver = Driver(self, 5000, target, 1)
        driver.verbose = False
        if background:
            driver.run_background()

        else:
            driver.run()

    def load_config(self, pkgname='config', stage=None):
        stage_f = stage or (lambda: os.environ.get('STAGE', 'development'))

        try:
            self.mapletree.config.load_package(pkgname)
            self.mapletree.config.stage = stage_f()

        except ImportError as e:
            fmt = 'Failed to load config package `{}`'
            logger.w(fmt.format(pkgname))
            logger.tb()

    def build(self):
        caller_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        if caller_name == '__main__' and not Driver.is_stub_proc():
            return

        logger.i('Start building app')
        self._build_reusables()
        self._build_autoloads()
        self._build_head_methods()
        self._build_options_methods()

    def _build_reusables(self):
        for prefix, seq in self.req_reusables.items():
            for mname in seq:
                try:
                    m = import_module(mname)
                    for k in dir(m):
                        attr = getattr(m, k)
                        if isinstance(attr, RequestTree):
                            self._build_reusables_request(prefix, attr)

                except ImportError:
                    fmt = 'Failed to merge request reusable `{}`'
                    logger.w(fmt, mname)
                    logger.tb()

        for mname in self.exc_reusables:
            try:
                m = import_module(mname)
                for k in dir(m):
                    attr = getattr(m, k)
                    if isinstance(attr, ExceptionTree):
                        self._build_reusables_exception(attr)

            except ImportError:
                fmt = 'Failed to merge exception reusable `{}`'
                logger.w(fmt, mname)
                logger.tb()

    def _build_reusables_request(self, prefix, rtree):
        self.mapletree.req.merge(rtree, prefix)
        for k, v in rtree.items():
            path = prefix + '/' + '/'.join(k)
            msg = 'Merged request endpoints `{}` for `{}`'.format(v, path)
            logger.i(msg)

    def _build_reusables_exception(self, etree):
        self.mapletree.exc.merge(etree)
        for k, v in etree.items():
            path = '/' + '/'.join(k)
            msg = 'Merged an exception endpoint `{}` for `{}`'.format(v, path)
            logger.i(msg)

    def _build_autoloads(self):
        for p in self.autoloads:
            try:
                self.mapletree.scan(p)

            except ImportError:
                logger.w('Failed to import package/module `{}`'.format(p))
                logger.tb()

    def _build_head_methods(self):
        for k, v in self.mapletree.req.items():
            if 'get' in v:
                def _(req):
                    return v['get'](req).body('')

                self.mapletree.req.head('/' + '/'.join(k))(_)

    def _build_options_methods(self):
        for k, v in self.mapletree.req.items():
            def _(req):
                return rsp().header('Allow', ','.join(v.keys()).upper())

            self.mapletree.req.options('/' + '/'.join(k))(_)

    def get(self, path=''):
        return self.req('get', path)

    def post(self, path=''):
        return self.req('post', path)

    def put(self, path=''):
        return self.req('put', path)

    def delete(self, path=''):
        return self.req('delete', path)

    def head(self, path=''):
        return self.req('head', path)

    def options(self, path=''):
        return self.req('options', path)

    def patch(self, path=''):
        return self.req('patch', path)

    def req(self, method, path):
        def _(f):
            fmt = 'Added a request endpoint for `{:8}: {}`'
            logger.i(fmt.format(method.upper(), path))
            return self.mapletree.req(method, path)(smart_response(f))
        return _

    def exc(self, exc_cls):
        def _(f):
            fmt = 'Added an exception endpoint for `{}`'
            logger.i(fmt.format(exc_cls))
            return self.mapletree.exc(exc_cls)(f)
        return _

    def validator(self, f):
        return Request.validator(f)


def smart_response(f):
    def _(req):
        r = f(req)

        if isinstance(r, Response):
            return r

        if r is None:
            return rsp()

        if isinstance(r, int):
            return rsp().code(r)

        if isinstance(r, (str, unicode)):
            return rsp().body(r)

        if isinstance(r, dict):
            return rsp().json(**r)

    return _
