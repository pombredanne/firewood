# coding:utf-8

from firewood import fw


@fw.get('/')
def _(req):
    return fw.rsp


@fw.post('/')
def _(req):
    return fw.rsp


@fw.put('/')
def _(req):
    return fw.rsp


@fw.delete('/')
def _(req):
    return fw.rsp


@fw.head('/')
def _(req):
    return fw.rsp


@fw.options('/')
def _(req):
    return fw.rsp


@fw.patch('/')
def _(req):
    return fw.rsp


@fw.get('/typeerror')
def _(req):
    raise TypeError()


@fw.get('/valueerror')
def _(req):
    raise ValueError()


@fw.get('/insufficient')
def _(req):
    a = req.params('a')


@fw.get('/validation')
def _(req):
    a = req.params.int_positive('a')


@fw.get('/error')
def _(req):
    fw.rsp.code(400).error()


@fw.exception(TypeError)
def _(e):
    raise TypeError()


@fw.config
def stage_value():
    return {'development': 100}


@fw.thread
def thread_value():
    return 100


@fw.post('/session')
def _(req):
    return fw.rsp.session({'id': 1})


@fw.get('/session')
def _(req):
    return fw.rsp.json(**req.session)


@fw.delete('/session')
def _(req):
    return fw.rsp.clear_session()
