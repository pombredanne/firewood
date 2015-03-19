# coding:utf-8

from firewood import fw
from mapletree.request import Request, VDict
from mapletree.response import Response


def _(req):
    return VDict(fw.signing.unsign(req.cookie('SESSION', default='')))


setattr(Request, 'session', _)


def _(rsp, data, expires=None, domain=None, secure=False):
    return rsp.cookie('SESSION',
                      fw.signing.sign(data),
                      expires,
                      domain,
                      '/',
                      secure)


setattr(Response, 'session', _)
