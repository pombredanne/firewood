# coding:utf-8

from mapletree.defaults.request import validators
from mapletree.defaults.request.argcontainer import ArgContainer


for key in dir(validators):
    if not key.startswith('_'):
        attr = getattr(validators, key)
        if hasattr(attr, '__call__'):
            def _(ac, key, *args, **kwargs):
                default = kwargs.pop('default', ArgContainer._REQUIRED)
                return ac(key, attr, args, kwargs, default)

            setattr(ArgContainer, key, _)
