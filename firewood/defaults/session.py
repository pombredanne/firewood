# coding:utf-8

from datetime import datetime, timedelta
from firewood import fw
from firewood.temptoken import TokenExpired
from mapletree import rsp
from mapletree.defaults.request import Request
from mapletree.defaults.request.argcontainer import ArgContainer
from mapletree.helpers.signing import SigningException


class InvalidSession(Exception):
    pass


@fw.exception(InvalidSession)
def _(e):
    return rsp().code(401).json(message='unauthorized')


def get_session(req):
    try:
        data = fw.session_token.decode(req.cookie('SESSION', default=''))

    except (SigningException, TokenExpired) as e:
        raise InvalidSession(e)

    else:
        return ArgContainer(data)


def set_session(rsp, data, expires=30*24*60, domain=None, secure=False):
    return rsp.cookie('SESSION',
                      fw.session_token.encode(**data),
                      datetime.now() + timedelta(minutes=expires),
                      domain,
                      '/',
                      secure)


def clear_session(rsp):
    return rsp.clear_cookie('SESSION')


setattr(Request, 'session', property(get_session))
setattr(rsp, 'session', set_session)
setattr(rsp, 'clear_session', clear_session)
