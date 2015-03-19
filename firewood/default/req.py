# coding:utf-8

from mapletree import rsp
from mapletree.routetree import RequestTree


default_rtree = RequestTree()


@default_rtree.get('/')
def _(req):
    return rsp()
