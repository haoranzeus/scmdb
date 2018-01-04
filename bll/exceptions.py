class SelfDefinedException(Exception):
    def __init__(self, message):
        self._code_client_prefix = "2302"
        self._code_server_prefix = "2102"
        self._code_normal_perfix = "2202"
        self.message = message

    def __str__(self):
        return repr(self.message)
    ''' Base self defined exception '''


# 客户端错误类
class QueryParameterError(SelfDefinedException):
    """
    查询参数错误
    """
    def __init__(self, message):
        super(QueryParameterError, self).__init__(message)
        self.code = self._code_client_prefix + "01"


class InsertParameterError(SelfDefinedException):
    """
    插入参数错误
    """
    def __init__(self, message):
        super(InsertParameterError, self).__init__(message)
        self.code = self._code_client_prefix + "02"


class UpdateParameterError(SelfDefinedException):
    """
    更新参数错误
    """
    def __init__(self, message):
        super(UpdateParameterError, self).__init__(message)
        self.code = self._code_client_prefix + "04"


class DeleteParameterError(SelfDefinedException):
    """
    删除参数错误
    """
    def __init__(self, message):
        super(DeleteParameterError, self).__init__(message)
        self.code = self._code_client_prefix + "04"
