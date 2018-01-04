# coding=utf-8
"""
synopsis: flask app handles.
author: haoranzeus@gmail.com (zhanghaoran)
"""
import logging
from flask import request

from bll import basic_interface
from bll.exceptions import InsertParameterError
from flask_restful import Resource


_log = logging.getLogger(__name__)
_code_normal_prefix = "2202"

_code_success = _code_normal_prefix + "00"
_code_success_get = _code_normal_prefix + "01"
_code_success_add = _code_normal_prefix + "02"
_code_success_update = _code_normal_prefix + "03"
_code_success_unchage = _code_normal_prefix + "04"
_code_success_delete = _code_normal_prefix + "05"


def handle_exception(cls):
    def try_orgi_func(func, result, se, *args, **kwargs):
        try:
            res = func(se, *args, **kwargs)
        except InsertParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        else:
            if res is not None:
                result['result'] = res
            result['status'] = 'SUCCESS'
            _log.debug('result = %s', result)
            return result

    if hasattr(cls, 'get'):
        orig_get = cls.get

        def new_get(self, *args, **kwargs):
            result = {'status': 'SUCCESS', "result": {}}
            return try_orgi_func(orig_get, result, self, *args, **kwargs)
        cls.get = new_get

    if hasattr(cls, 'post'):
        orig_post = cls.post

        def new_post(self, *args, **kwargs):
            result = {'status': 'SUCCESS', "result": {}}
            return try_orgi_func(orig_post, result, self, *args, **kwargs)
        cls.post = new_post
    return cls


def _result_format(code=_code_success, msg='成功', data=None):
    """
    格式化返回数据
    """
    result = {
        'code': code,
        'msg': msg,
    }
    if data:
        result['data'] = data
    return result


@handle_exception
class idc_list(Resource):
    def post(self):
        data = basic_interface.api_idc_list(request.json)
        return _result_format(code=_code_success_get, msg='获取成功', data=data)
