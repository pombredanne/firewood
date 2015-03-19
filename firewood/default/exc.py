# coding:utf-8

import traceback
from mapletree import rsp
from mapletree.exceptions import (MethodNotAllowed,
                                  NotFound,
                                  InsufficientError,
                                  ValidationError,
                                  InvalidSignedMessage)
from mapletree.routetree import ExceptionTree


default_etree = ExceptionTree()


@default_etree(Exception)
def _(e):
    traceback.print_exc()
    return rsp().code(500).json(message='unknown error')


@default_etree(MethodNotAllowed)
def _(e):
    return rsp().code(405).json(message='method not allowed')


@default_etree(NotFound)
def _(e):
    return rsp().code(404).json(message='not found')


@default_etree(InsufficientError)
def _(e):
    msg = 'insufficient parameter `{}`'.format(e)
    return rsp().code(400).json(message=msg)


@default_etree(ValidationError)
def _(e):
    key, val, err = e
    msg = 'invalid parameter value `{}` for `{}`'.format(key, val)
    return rsp().code(400).json(message=msg)


@default_etree(InvalidSignedMessage)
def _(e):
    return rsp().code(401).json(message='unauthorized')
