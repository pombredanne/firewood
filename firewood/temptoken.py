# coding:utf-8

import time
from mapletree.helpers.signing import Signing


class TempToken(object):
    def __init__(self, key, life=60*60):
        self._signing = Signing(key)
        self._life = life

    def encode(self, **kwargs):
        kwargs['__expires__'] = int(time.time()) + self._life
        return self._signing.sign(kwargs)

    def decode(self, token):
        data = self._signing.unsign(token)
        exp = data.pop('__expires__', 0)
        if time.time() < exp:
            return data

        raise TokenExpired()


class TokenExpired(Exception):
    pass
