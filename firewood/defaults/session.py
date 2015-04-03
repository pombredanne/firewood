# coding:utf-8

from datetime import datetime, timedelta
from firewood import fw
from mapletree import rsp
from mapletree.defaults.request.request import Request
from mapletree.defaults.request.argcontainer import ArgContainer
from mapletree.helpers.signing import SigningException
from mapletree.helpers.temptoken import TempToken, ExpiredToken


session_name = 'SESSION'
session_token = TempToken(fw.config.session_key, fw.config.session_life)


class InvalidSession(Exception):
    pass


@fw.exception(InvalidSession)
def _(e):
    return rsp().code(401).json(message='unauthorized')


def get_session(req):
    try:
        data = session_token.decode(req.cookie(session_name, default=''))

    except (SigningException, ExpiredToken) as e:
        raise InvalidSession(e)

    else:
        return ArgContainer(data)


def set_session(rsp,
                data,
                expires=fw.config.session_life,
                domain=None,
                secure=False):

    exp = datetime.now + timedelta(seconds=expires) if expires else None
    return rsp.cookie(session_name,
                      session_token.encode(**data),
                      exp,
                      domain,
                      '/',
                      secure)


def clear_session(rsp):
    return rsp.clear_cookie(session_name)


setattr(Request, 'session', property(get_session))
setattr(rsp, 'session', set_session)
setattr(rsp, 'clear_session', clear_session)
