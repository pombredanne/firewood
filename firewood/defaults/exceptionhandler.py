# coding:utf-8

from firewood import logger, fw
from mapletree import rsp
from mapletree.defaults.request.argcontainer import (InsufficientError,
                                                     ValidationError)
from mapletree.defaults.routings.requestrouting import (MethodNotAllowed,
                                                        NotFound)
from sqlew.exceptions import (QueryFormatError,
                              UnacceptableResultError)


@fw.exception(Exception)
def _(e):
    logger.tb()
    return fw.rsp.code(500).json(message='unknown error')


@fw.exception(rsp)
def _(e):
    return e


@fw.exception(MethodNotAllowed)
def _(e):
    return fw.rsp.code(405).json(message='method not allowed')


@fw.exception(NotFound)
def _(e):
    return fw.rsp.code(404).json(message='not found')


@fw.exception(InsufficientError)
def _(e):
    msg = 'insufficient parameter `{}`'.format(e)
    return fw.rsp.code(400).json(message=msg)


@fw.exception(ValidationError)
def _(e):
    key, val, err = e.args
    msg = 'invalid parameter value `{}` for `{}`'.format(key, val)
    return fw.rsp.code(400).json(message=msg)


@fw.exception(QueryFormatError)
def _(e):
    logger.tb()
    return fw.rsp.code(500).json(message='failed to bind values')


@fw.exception(UnacceptableResultError)
def _(e):
    logger.tb()
    return fw.rsp.code(400).json(message='bad access')
