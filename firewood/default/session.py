# coding:utf-8

from firewood import fw
from mapletree.request import Request, VDict
from mapletree.response import Response


def request_session(req):
    return VDict(fw.signing.unsign(req.cookie('SESSION', default='')))


setattr(Request, 'session', _)


def response_session(rsp, data, expires=None, domain=None, secure=False):
    return rsp.cookie('SESSION',
                      fw.signing.sign(data),
                      expires,
                      domain,
                      '/',
                      secure)


setattr(Response, 'session', _)


def response_clear_session(rsp):
    return rsp.clear_cookie('SESSION')
