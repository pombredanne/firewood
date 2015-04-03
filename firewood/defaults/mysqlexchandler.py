# coding:utf-8

try:
    import mysql.connector

except ImportError:
    pass

else:
    from firewood import fw, logger
    from mysql.connector.errors import (Error,
                                        DataError,
                                        IntegrityError,
                                        ProgrammingError)

    @fw.exception(Error)
    def _(e):
        logger.tb()
        return fw.rsp.code(500).json(message='unknown db error')

    @fw.exception(DataError)
    def _(e):
        logger.tb()
        return fw.rsp.code(409).json(message='db data error')

    @fw.exception(IntegrityError)
    def _(e):
        logger.tb()
        return fw.rsp.code(409).json(message='db integrity error')

    @fw.exception(ProgrammingError)
    def _(e):
        logger.tb()
        return fw.rsp.code(500).json(message='bad sql')
