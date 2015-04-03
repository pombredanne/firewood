# coding:utf-8

from firewood import fw
from sqlew import Client as SqlewClient


class Client(SqlewClient):
    def exe(self, strong, fmt, **kwargs):
        return super(Client, self).exe(strong, self._compact(fmt), **kwargs)

    def _compact(self, fmt):
        return ' '.join([l.lstrip(' ') for l in fmt.splitlines()])


@fw.thread
def db():
    return Client(fw.config.dbclient,
                  **fw.config.dbinfo)
