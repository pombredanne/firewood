# coding:utf-8

from mapletree.defaults.request import validators
from mapletree.defaults.request.argcontainer import ArgContainer


def add_validator(attr):
    def _(ac, key, *args, **kwargs):
        default = kwargs.pop('default', ArgContainer._REQUIRED)
        return ac(key, attr, args, kwargs, default)

    setattr(ArgContainer, attr.__name__, _)


for name in dir(validators):
    if not name.startswith('_'):
        attr = getattr(validators, name)
        if hasattr(attr, '__call__'):
            if attr.__module__ == 'mapletree.defaults.request.validators':
                add_validator(attr)
