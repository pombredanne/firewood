# coding:utf-8

from __future__ import print_function
import math
import traceback


def i(msg):
    log(' INFO      ', msg, 100)


def w(msg):
    log(' WARNING   ', msg, 100)


def e(msg):
    log(' ERROR     ', msg, 100)


def tb():
    log(' TRACEBACK ', traceback.format_exc(), 100)


def log(title, msg, width=None):
    title_prefix = '['
    title_suffix = '] '
    title_width = len(title_prefix) + len(title) + len(title_suffix)
    print(title_prefix + title + title_suffix, end='')

    for i, l in enumerate(_split_lines(str(msg), width)):
        if i == 0:
            print(l)

        else:
            print('{}{}'.format(' ' * title_width, l))


def _split_lines(msg, width_limit=None):
    if len(msg) == 0:
        yield ''

    elif width_limit is None:
        for l in msg.splitlines():
            yield l

    else:
        for l in msg.splitlines():
            if l <= width_limit:
                yield l

            else:
                line = ''
                for w in l.split(' '):
                    if len(line) + len(w) < width_limit:
                        line += w + ' '

                    else:
                        if len(w) <= width_limit:
                            yield line
                            line = w

                        else:
                            yield line

                            wl = len(w)
                            count = int(math.ceil(wl/float(width_limit-1)))

                            for i in range(0, count-1):
                                yield w[i*width_limit:(i+1)*width_limit] + '-'

                            line = w[(count-1)*width_limit:] + ' '

                yield line
