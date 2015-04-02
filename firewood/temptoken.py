# coding:utf-8

import time
from mapletree.helpers.signing import Signing


class TempToken(object):
    def __init__(self, key, life=60*60):
        self._signing = Signing(key)
        self._life = life

    def encode(self, **kwargs):
        if self._life:
            kwargs['__expires__'] = int(time.time()) + self._life

        else:
            kwargs['__expires__'] = None

        return self._signing.sign(kwargs)

    def decode(self, token):
        data = self._signing.unsign(token)
        exp = data.pop('__expires__', 0)
        if exp is None or time.time() < exp:
            return data

        raise TokenExpired()


class TokenExpired(Exception):
    pass
