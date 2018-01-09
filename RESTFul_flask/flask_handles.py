# coding=utf-8
"""
synopsis: flask app handles.
author: haoranzeus@gmail.com (zhanghaoran)
"""
import logging
from flask import request

from bll import basic_interface
from bll.exceptions import ParameterError
from bll.exceptions import QueryParameterError
from bll.exceptions import InsertParameterError
from bll.exceptions import UpdateParameterError
from bll.exceptions import DeleteParameterError
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
        except ParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        except InsertParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        except QueryParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        except UpdateParameterError as e:
            result['result']['code'] = e.code
            result['result']['msg'] = e.message
            return result
        except DeleteParameterError as e:
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


# =====================================================================
# 机房增删查改
# =====================================================================
@handle_exception
class idc_list(Resource):
    def post(self):
        data = basic_interface.api_idc_list(request.json)
        return _result_format(code=_code_success_get, msg='获取成功', data=data)


@handle_exception
class idc_add(Resource):
    def post(self):
        basic_interface.api_idc_add(request.json)
        return _result_format(code=_code_success_add, msg='插入成功')


@handle_exception
class idc_del(Resource):
    def post(self):
        basic_interface.api_idc_del(request.json)
        return _result_format(code=_code_success_delete, msg='删除成功')


@handle_exception
class idc_update(Resource):
    def post(self):
        basic_interface.api_idc_update(request.json)
        return _result_format(code=_code_success_update, msg='更新成功')


@handle_exception
class rack_add(Resource):
    def post(self):
        basic_interface.api_rack_add(request.json)
        return _result_format(code=_code_success_add, msg='插入成功')


@handle_exception
class rack_del(Resource):
    def post(self):
        basic_interface.api_rack_del(request.json)
        return _result_format(code=_code_success_delete, msg='删除成功')


@handle_exception
class rack_list(Resource):
    def post(self):
        data = basic_interface.api_rack_list(request.json)
        return _result_format(code=_code_success_get, msg='获取成功', data=data)


@handle_exception
class rack_update(Resource):
    def post(self):
        basic_interface.api_rack_update(request.json)
        return _result_format(code=_code_success_update, msg='更新成功')


@handle_exception
class server_add(Resource):
    def post(self):
        basic_interface.api_server_add(request.json)
        return _result_format(code=_code_success_add, msg='插入成功')


@handle_exception
class server_del(Resource):
    def post(self):
        basic_interface.api_server_del(request.json)
        return _result_format(code=_code_success_delete, msg='删除成功')


@handle_exception
class server_list(Resource):
    def post(self):
        data = basic_interface.api_server_list(request.json)
        return _result_format(code=_code_success_get, msg='获取成功', data=data)


@handle_exception
class server_update(Resource):
    def post(self):
        basic_interface.api_server_update(request.json)
        return _result_format(code=_code_success_update, msg='更新成功')


@handle_exception
class vm_add(Resource):
    def post(self):
        basic_interface.api_vm_add(request.json)
        return _result_format(code=_code_success_add, msg='插入成功')


@handle_exception
class vm_del(Resource):
    def post(self):
        basic_interface.api_vm_del(request.json)
        return _result_format(code=_code_success_delete, msg='删除成功')


@handle_exception
class vm_list(Resource):
    def post(self):
        data = basic_interface.api_vm_list(request.json)
        return _result_format(code=_code_success_get, msg='获取成功', data=data)


@handle_exception
class vm_update(Resource):
    def post(self):
        basic_interface.api_vm_update(request.json)
        return _result_format(code=_code_success_update, msg='更新成功')
